@echo off
chcp 65001 >nul
color 0B
echo ========================================================
echo 🚀 WIKMAZ SMART GITHUB PUBLISHER (ORGANIZATION DEPLOY)
echo ========================================================
echo.
echo Wypychanie z konta: biherolive-beep
echo Docelowa organizacja: wikmaz-pl
echo.

set /p repo_name="🔗 Podaj nazwe projektu (np. GhostStream_C2): "
set repo_url=https://github.com/wikmaz-pl/%repo_name%.git

echo.
echo ⚙️ Konfiguracja lokalna...
git init
git config user.name "biherolive-beep"
git config user.email "admin@softhause.wikmaz.pl"
git add .
git commit -m "🚀 Auto-Deploy do Organizacji Wikmaz"
git branch -M main
git remote remove origin 2>nul
git remote add origin %repo_url%

echo.
echo 🔍 Sprawdzam obecnosc GitHub CLI (gh.exe)...
gh --version >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo ⚡ WYKRYTO GITHUB CLI! Tworze repozytorium automatycznie przez API...
    gh repo create wikmaz-pl/%repo_name% --public --source=. --remote=origin --push
    echo.
    echo ✅ POSZLO! W pelni zautomatyzowany deploy zakonczony.
    pause
    exit
) ELSE (
    echo ⚠️ Brak GitHub CLI. Przechodzimy w tryb Smart Browser Hook.
    echo.
    echo 1. Za sekunde system otworzy Twoja przegladarke.
    echo 2. Wpisz tam nazwe '%repo_name%' i kliknij "Create repository".
    echo 3. GDY TO ZROBISZ, wroc do tego okna i wcisnij dowolny klawisz!
    echo.
    
    :: Otwiera dokladna strone tworzenia repozytorium w Twojej organizacji!
    start https://github.com/organizations/wikmaz-pl/repositories/new
    
    pause
    
    echo.
    echo 📡 Wysylanie kodu na serwery GitHub...
    git push -u origin main -f
    
    echo.
    echo ✅ POSZLO! Twoj kod jest oficjalnie na GitHubie.
    pause
)
