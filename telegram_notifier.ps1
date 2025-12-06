# ====================================================
# TELEGRAM NOTIFIER - Отправка результатов в Telegram
# ====================================================

param(
    [string]$botToken = "YOUR_BOT_TOKEN",
    [string]$chatId = "YOUR_CHAT_ID"
)

Write-Host "?? TELEGRAM NOTIFIER" -ForegroundColor Cyan
Write-Host "==================" -ForegroundColor Cyan

# Загружаем результаты
$candidatesFile = "C:\recruitment-ai\candidates_ai_scored.json"

if (Test-Path $candidatesFile) {
    $candidates = Get-Content $candidatesFile -Raw | ConvertFrom-Json
    $count = $candidates.Count
    $totalBonus = $count * 120000
    
    # Формируем сообщение
    $message = @"
?? AI Recruiter Daily Report

?? Candidates Found: $count
?? Potential Bonus: $($totalBonus / 1000)k ? (50% realistic)
?? Annual Income: $($totalBonus * 12 / 2 / 1000000)M ?

Top Candidates:
$(($candidates | Select-Object -First 3 | ForEach-Object { "? $($_.login) (Score: $($_.AI_Score)/100)" }) -join "`n")

?? View all: https://github.com/maksimmishakov/lamoda-ai-recruiter

#recruitment #lamoda #ai
"@
    
    Write-Host "Message prepared:" -ForegroundColor Green
    Write-Host $message
    
    # Отправляем в Telegram (если токены заполнены)
    if ($botToken -ne "YOUR_BOT_TOKEN" -and $chatId -ne "YOUR_CHAT_ID") {
        $telegramUrl = "https://api.telegram.org/bot$botToken/sendMessage"
        
        $body = @{
            chat_id = $chatId
            text = $message
            parse_mode = "HTML"
        } | ConvertTo-Json
        
        try {
            $response = Invoke-RestMethod -Uri $telegramUrl -Method Post -ContentType "application/json" -Body $body
            Write-Host "? Message sent to Telegram!" -ForegroundColor Green
        } catch {
            Write-Host "? Failed to send: $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host ""
        Write-Host "?? To enable Telegram notifications:" -ForegroundColor Yellow
        Write-Host "1. Create Telegram bot: https://t.me/BotFather"
        Write-Host "2. Get your chat ID: https://t.me/userinfobot"
        Write-Host "3. Update this script with your tokens"
        Write-Host ""
    }
}
