# C:\recruitment-ai\send_to_telegram.ps1

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$token = $env:TELEGRAM_BOT_TOKEN
$chatId = $env:TELEGRAM_CHAT_ID
$candidates = Get-Content "C:\recruitment-ai\candidates.json" | ConvertFrom-Json

Write-Host "Sending to Telegram..." -ForegroundColor Cyan

# Build message
$msg = "AI RECRUITER - FOUND $($candidates.Count) CANDIDATES`n`n"
foreach ($c in $candidates) {
    $msg += "• $($c.login)`n  $($c.html_url)`n`n"
}

# Send to Telegram
$url = "https://api.telegram.org/bot$token/sendMessage"
$body = @{
    chat_id = $chatId
    text = $msg
    parse_mode = "HTML"
} | ConvertTo-Json

try {
    $r = Invoke-RestMethod -Uri $url -Method Post -ContentType "application/json" -Body $body
    Write-Host "? SUCCESS! Message sent to Telegram" -ForegroundColor Green
    Write-Host "Check: @recruitmentmaksim_bot" -ForegroundColor Yellow
}
catch {
    Write-Host "? ERROR: $($_.Exception.Message)" -ForegroundColor Red
}
