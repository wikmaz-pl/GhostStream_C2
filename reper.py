import os

def fix_deploy_script_v3():
    print("🚀 Instalowanie Pancernej Łatki v3 dla GitHub Publishera...")
    
    bat_content = """@echo off
setlocal EnableDelayedExpansion
chcp 65001 >nul
color 0B
echo ========================================================
echo 🚀 WIKMAZ SMART GITHUB PUBLISHER [RELEASE DEPLOY]
echo ========================================================
echo.

set /p repo_name="🔗 Podaj nazwe projektu [np. GhostStream_C2]: "
set repo_url=https://github.com/wikmaz-pl/!repo_name!.git

:: Dynamiczny tag wersji do Release
set tag_ver=v1.0.!RANDOM!

echo.
echo ⚙️ Konfiguracja lokalna i czyszczenie...
git init
git config user.name "biherolive-beep"
git config user.email "admin@softhause.wikmaz.pl"
git add .
git commit -m "🚀 Auto-Deploy + Release [!tag_ver!]"
git branch -M main

rem Usuwamy stare polaczenia, aby uniknac konfliktow
git remote remove origin 2>nul
git remote add origin !repo_url!

echo.
echo 🔍 Sprawdzam obecnosc GitHub CLI [gh.exe]...
gh --version >nul 2>&1

IF !ERRORLEVEL! EQU 0 (
    echo ⚡ WYKRYTO GITHUB CLI! 
    echo 1. Tworze/Aktualizuje repozytorium przez API...
    gh repo create wikmaz-pl/!repo_name! --public --source=. --remote=origin --push 2>nul
    
    rem Zapasowe wypchniecie kodu, jesli repo juz istnieje
    git push -u origin main -f
    
    echo 2. Tworzenie oficjalnego WIKMAZ RELEASE [!tag_ver!]...
    
    IF EXIST "GhostStream_C2_Release.zip" (
        gh release create !tag_ver! GhostStream_C2_Release.zip --title "GhostStream C2 Release !tag_ver!" --notes "Automated executable release package."
        echo.
        echo ✅ POSZLO! Kod na GitHubie, a plik ZIP w zakladce Releases!
    ) ELSE (
        echo.
        echo ❌ BLAD SYSTEMOWY: Nie znaleziono pliku GhostStream_C2_Release.zip!
        echo Najpierw uruchom '1_Compile_to_EXE.bat', aby stworzyc paczke!
    )
    
    pause
    exit
) ELSE (
    echo ⚠️ Brak GitHub CLI [gh.exe] w systemie.
    echo 🔄 Probuje automatycznie zainstalowac narzedzie uzywajac Winget...
    winget install --id GitHub.cli -e --accept-source-agreements --accept-package-agreements >nul 2>&1
    
    gh --version >nul 2>&1
    IF !ERRORLEVEL! EQU 0 (
        echo ✅ Udalo sie zainstalowac GitHub CLI! Odpal ten skrypt ponownie.
        pause
        exit
    ) ELSE (
        echo ❌ Nie udalo sie zainstalowac w tle. Przechodzimy w tryb reczny...
        echo 1. Zostanie otwarta przegladarka. Utworz repozytorium !repo_name!
        echo 2. Wroc tutaj i wcisnij ENTER.
        start https://github.com/organizations/wikmaz-pl/repositories/new
        pause
        git push -u origin main -f
        echo ✅ Kod wyslany, ale plik ZIP musisz dodac do zakladki Releases recznie!
        pause
    )
)
"""
    
    with open('2_Deploy_to_GitHub_Smart.bat', 'w', encoding='utf-8') as f:
        f.write(bat_content)
        
    print("✅ Gotowe! Plik '2_Deploy_to_GitHub_Smart.bat' zaktualizowany.")
    print("👉 Możesz go teraz bezpiecznie uruchomić.")

if __name__ == "__main__":
    fix_deploy_script_v3()