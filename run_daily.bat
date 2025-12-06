@echo off
cd C:\recruitment-ai

REM Основной поиск и обработка
powershell.exe -ExecutionPolicy Bypass -File "C:\recruitment-ai\orchestrator.ps1" -action run

REM Отправка метрик в Telegram
powershell.exe -ExecutionPolicy Bypass -File "C:\recruitment-ai\metrics.ps1"

REM Логирование
echo [%date% %time%] Daily cycle completed >> C:\recruitment-ai\logs.txt

exit
