@echo off
REM VEERBOT - Quick Start Script
:menu
cls
echo.
echo ======================================================
echo          VEERBOT - Quick Start Menu
echo ======================================================
echo.
echo 1. Start Bot Server (main.exe)
echo 2. Open Web Interface (index.html)
echo 3. Start Python Client
echo 4. Start bot + Open Web Interface
echo 5. View README Setup Instructions
echo 6. Compile main.cpp (if modified)
echo 0. Exit
echo.
set /p choice="Select option (0-6): "

if "%choice%"=="1" goto start_bot
if "%choice%"=="2" goto open_web
if "%choice%"=="3" goto python_client
if "%choice%"=="4" goto bot_and_web
if "%choice%"=="5" goto view_readme
if "%choice%"=="6" goto compile
if "%choice%"=="0" goto end
goto menu

:start_bot
echo.
echo Starting Bot Server...
echo.
main.exe
pause
goto menu

:open_web
echo.
echo Opening Web Interface...
echo.
start index.html
echo Web interface opened in default browser!
pause
goto menu

:python_client
echo.
echo Starting Python Client...
echo.
python python_client.py
pause
goto menu

:bot_and_web
echo.
echo Starting Bot Server...
main.exe --verbose
timeout /t 2 /nobreak
start index.html
echo. Bot server started and web interface opened!
pause
goto menu

:view_readme
echo.
type README_SETUP.txt
pause
goto menu

:compile
echo.
echo Compiling C++ code...
echo.
g++ -o main.exe main.cpp -lws2_32
if %errorlevel%==0 (
    echo Compilation successful!
) else (
    echo Compilation failed!
)
pause
goto menu

:end
echo.
echo Goodbye!
echo.
exit /b 0
