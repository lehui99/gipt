@echo off
start ss.bat
ping -n 10 127.0.0.1
python gipt.py config.json
pause