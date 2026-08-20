@echo off
chcp 65001 >nul
color 0B
echo ========================================================
echo 🚀 WIKMAZ SMART GITHUB PUBLISHER (RELEASE DEPLOY)
echo ========================================================
echo.

set /p repo_name="🔗 Podaj nazwe projektu (np. GhostStream_C2): "
set repo_url=https://github.com/wikmaz-pl/%repo_name%.git

echo.
echo ⚙️ Konfiguracja lokalna i czyszczenie...
git init
git config user.name "biherolive-beep"
git config user.email "admin@softhause.wikmaz.pl"
git add .
git commit -m "🚀 Auto-Deploy + Zaktualizowane README"
git branch -M main
git remote remove origin 2>nul
git remote add origin %repo_url%

echo.
echo 🔍 Sprawdzam obecnosc GitHub CLI (gh.exe)...
gh --version >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    echo ⚡ WYKRYTO GITHUB CLI! 
    echo 1. Tworze/Aktualizuje repozytorium...
    gh repo create wikmaz-pl/%repo_name% --public --source=. --remote=origin --push 2>nul
    
    :: Wypychanie normalnego kodu, jeśli repozytorium juz istnieje
    git push -u origin main -f
    
    echo 2. Tworzenie oficjalnego WIKMAZ RELEASE z paczka ZIP...
    :: Dynamiczny tag wersji zapobiega konfliktom (uzywamy v1.0.RANDOM)
    set "tag_ver=v1.0.%RANDOM%"
    gh release create %tag_ver% GhostStream_C2_Release.zip --title "GhostStream C2 Release" --notes "Automated executable release package."
    
    echo.
    echo ✅ POSZLO! Kod na GitHubie, a plik ZIP w zakladce Releases!
    pause
    exit
) ELSE (
    echo ⚠️ Brak GitHub CLI (gh). Wymagane do automatycznego Release'u!
    echo Przechodzimy w tryb reczny...
    start https://github.com/organizations/wikmaz-pl/repositories/new
    pause
    git push -u origin main -f
    echo ✅ Kod wyslany, ale plik ZIP musisz dodac do 'Releases' recznie!
    pause
)
