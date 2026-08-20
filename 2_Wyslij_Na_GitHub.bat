@echo off
chcp 65001 >nul
color 0B
echo ========================================================
echo 🚀 WIKMAZ GITHUB AUTO-PUBLISHER (ONE-CLICK DEPLOY)
echo ========================================================
echo.
echo Ten skrypt automatycznie wysle kod z tego folderu na GitHuba.
echo Bezpieczenstwo: Ukryty plik .gitignore zablokuje wyslanie
echo Twoich baz danych, filmow, logow i plikow wykonywalnych .exe.
echo Na swiatlo dzienne wyjdzie TYLKO czysty, profesjonalny kod.
echo.

set /p repo="🔗 Wklej link do pustego repozytorium (np. https://github.com/wikmaz-pl/Repo.git): "

echo.
echo ⚙️ Inicjalizacja narzedzi Git...
git init
git add .
git commit -m "🚀 Auto-Deploy Wikmaz GhostStream C2"
git branch -M main
git remote add origin %repo%

echo.
echo 📡 Wysylanie kodu na serwery GitHub...
git push -u origin main -f

echo.
echo ✅ POSZLO! Twoj kod jest oficjalnie na GitHubie.
pause
