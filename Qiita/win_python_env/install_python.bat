@echo off
powershell -ExecutionPolicy Bypass ./install_python.ps1
timeout 10 /NOBREAK
powershell -ExecutionPolicy Bypass ./setup_venv.ps1

