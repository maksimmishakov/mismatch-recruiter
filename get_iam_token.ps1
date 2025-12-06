# ========================================
# ПОЛУЧИТЬ IAM TOKEN ДЛЯ YandexGPT
# ========================================

$API_KEY = "YCOXr8veG8zGNO0uWS3u63TSlo1l2kH-bgUbzJT"

Write-Host "?? Получаю IAM Token..." -ForegroundColor Cyan

$url = "https://auth.api.cloud.yandex.net/v1/tokens"

$body = @{
    yandexPassportOauthToken = $API_KEY
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
}

try {
    $response = Invoke-RestMethod -Uri $url -Method POST -Headers $headers -Body $body -ErrorAction Stop
    
    $iam_token = $response.iamToken
    
    Write-Host "? IAM Token получен!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Твой IAM Token (используй его ниже):" -ForegroundColor Cyan
    Write-Host $iam_token -ForegroundColor Yellow
    
    # Сохраняем в переменную окружения (чтоб не потерять)
    [Environment]::SetEnvironmentVariable("YC_IAM_TOKEN", $iam_token, "User")
    Write-Host ""
    Write-Host "?? Сохранен в переменную окружения YC_IAM_TOKEN" -ForegroundColor Green
    
} catch {
    Write-Host "? ОШИБКА!" -ForegroundColor Red
    Write-Host $_.Exception.Message
}
