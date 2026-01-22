@echo off
echo Deteniendo servidores Python existentes...
for /f "tokens=2" %%i in ('tasklist /FI "IMAGENAME eq python.exe" /FO LIST ^| findstr PID:') do (
    taskkill /PID %%i /F
)

echo Iniciando servidor para dispositivos locales...
python -m http.server 8000 --bind 0.0.0.0

pause