@echo off
cd /d "%~dp0"
echo Desktop: http://localhost:8765/prototype/
echo For mobile: use this computer's Wi-Fi IPv4 address in place of localhost.
echo Keep this window open while using the prototype.
set "RM_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%RM_PYTHON%" (
  "%RM_PYTHON%" -m http.server 8765 --bind 0.0.0.0
) else (
  python -m http.server 8765 --bind 0.0.0.0
)
pause
