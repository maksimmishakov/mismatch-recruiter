# C:\recruitment-ai\START_FULL_CYCLE.ps1

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   ?? STARTING AI RECRUITER ??"
Write-Host "==========================================" -ForegroundColor Cyan

# 1. Ищем кандидатов
Write-Host "`n[STEP 1] Searching GitHub..." -ForegroundColor Yellow
.\run_bot.ps1

# 2. Создаем отчет
Write-Host "`n[STEP 2] Generating Report..." -ForegroundColor Yellow
.\final_report.ps1

# 3. Отправляем в Telegram
Write-Host "`n[STEP 3] Sending to Telegram..." -ForegroundColor Yellow
.\send_to_telegram.ps1

Write-Host "`n? CYCLE COMPLETE! Check your Telegram." -ForegroundColor Green
Start-Sleep -Seconds 5
