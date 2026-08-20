import os

def build_github_publisher():
    print("🚀 Generowanie dedykowanego skryptu GitHub dla organizacji wikmaz-pl...")
    
    # Skrypt zostanie utworzony w aktualnym folderze (lub w folderze projektu, jeśli zmienisz ścieżkę)
    bat_content = """@echo off
chcp 65001 >nul
color 0B
echo ========================================================
echo 🚀 WIKMAZ GITHUB AUTO-PUBLISHER (ORGANIZATION DEPLOY)
echo ========================================================
echo.
echo Wypychanie z konta: biherolive-beep
echo Docelowa organizacja: https://github.com/wikmaz-pl/
echo.

set /p repo_name="🔗 Podaj TYLKO nazwe repozytorium (np. GhostStream_C2): "
set repo_url=https://github.com/wikmaz-pl/%repo_name%.git

echo.
echo ⚙️ Skladam link: %repo_url%
echo ⚙️ Inicjalizacja narzedzi Git...

git init
git add .
git commit -m "🚀 Auto-Deploy do Organizacji Wikmaz"
git branch -M main

:: Usuwamy stary origin, jeśli istnieje, żeby uniknąć błędu "remote origin already exists"
git remote remove origin 2>nul
git remote add origin %repo_url%

echo.
echo 📡 Wysylanie kodu na serwery GitHub (Organizacja wikmaz-pl)...
git push -u origin main -f

echo.
echo ✅ POSZLO! Twoj kod jest oficjalnie na GitHubie.
pause
"""
    
    # Zapis pliku
    with open('2_Wyslij_Na_GitHub_Org.bat', 'w', encoding='utf-8') as f:
        f.write(bat_content)
        
    print("✅ Gotowe! Utworzono plik '2_Wyslij_Na_GitHub_Org.bat'.")

if __name__ == "__main__":
    build_github_publisher()