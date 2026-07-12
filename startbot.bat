@echo off
cd /d "%~dp0"
set "PATH=C:\msys64\mingw64\bin;%PATH%"
echo Bot ishga tushirilmoqda...
"C:\Users\becar\miniconda3\python.exe" -m bot.main
if errorlevel 1 (
    echo.
    echo Bot xato bilan to'xtadi. Yuqoridagi xabarni tekshiring.
    pause
)
