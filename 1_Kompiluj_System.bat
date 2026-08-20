@echo off
color 0A
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' ( echo 🛡️ Zadam uprawnien Administratora... && echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs" && echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs" && "%temp%\getadmin.vbs" && del "%temp%\getadmin.vbs" && exit /B )
pushd "%CD%" && CD /D "%~dp0"
echo 🚀 WIKMAZ GHOSTSTREAM C2 - PANCERNY KOMPILATOR 🚀

echo [KROK 1] Tworzenie sterylnego laboratorium...
py -3.11 -m venv venv_ghost
call venv_ghost\Scripts\activate.bat

echo [KROK 2] Instalacja zaleznosci...
python -m pip install --upgrade pip >nul
python -m pip install pyinstaller flask >nul

echo [KROK 3] Budowanie niezaleznego pliku EXE z nowa marka...
python -m PyInstaller --onefile --add-data "templates_public;templates_public" --add-data "templates_nexus;templates_nexus" --name "Wikmaz_GhostStream_C2" launcher.py

echo [KROK 4] Pakowanie operacyjne (Release)...
mkdir Release 2>nul
copy dist\Wikmaz_GhostStream_C2.exe Release\ >nul
deactivate
rmdir /S /Q venv_ghost && rmdir /S /Q build && rmdir /S /Q dist && del Wikmaz_GhostStream_C2.spec 2>nul

echo ✅ Gotowe! Plik 'Wikmaz_GhostStream_C2.exe' znajduje sie w folderze Release. 
pause
