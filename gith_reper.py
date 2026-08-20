import os

def update_github_publisher():
    print("🚀 Aktualizacja Auto-Publishera o Auto-Tożsamość Git...")
    
    bat_content = """@echo off
chcp 65001 >nul
color 0B
echo ========================================================
echo 🚀 WIKMAZ GITHUB AUTO-PUBLISHER (AUTO-IDENTITY)
echo ========================================================
echo.

set /p repo_name="🔗 Podaj TYLKO nazwe repozytorium (np. GhostStream): "
set repo_url=https://github.com/wikmaz-pl/%repo_name%.git

echo.
echo ⚙️ Skladam link: %repo_url%
echo ⚙️ Inicjalizacja narzedzi Git...

git init

:: TARCZA: Konfiguracja Twojej tozsamosci Git TYLKO dla tego folderu!
git config user.name "biherolive-beep"
git config user.email "admin@softhause.wikmaz.pl"

git add .
git commit -m "🚀 Auto-Deploy do Organizacji Wikmaz"
git branch -M main

:: Usuwamy stare polaczenia, by uniknac konfliktow
git remote remove origin 2>nul
git remote add origin %repo_url%

echo.
echo 📡 Wysylanie kodu na serwery GitHub... 
echo ⚠️ UWAGA: Za chwile system moze otworzyc okno przegladarki!
echo 👉 Kliknij tam "Sign in with your browser" i uzyj konta Google.
echo.

git push -u origin main -f

echo.
echo ✅ POSZLO! Twoj kod jest oficjalnie na GitHubie.
pause
"""
    
    with open('2_Wyslij_Na_GitHub_Org.bat', 'w', encoding='utf-8') as f:
        f.write(bat_content)
        
    print("✅ Gotowe! Zaktualizowano plik '2_Wyslij_Na_GitHub_Org.bat'.")

if __name__ == "__main__":
    update_github_publisher()