@echo off
chcp 65001 > nul
echo Запуск resume-parser-ai...

cd /d "%~dp0"
call venv\Scripts\activate.bat
python main.py

pause