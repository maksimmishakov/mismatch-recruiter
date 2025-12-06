# ========================================
# ТЕСТ YandexGPT API
# ========================================

$API_KEY = "YCOXr8veG8zGNO0uWS3u63TSlo1l2kH-bgUbzJT"
$FOLDER_ID = "b1gl37qg99ijsedu73rh"

Write-Host "?? Тестирование YandexGPT..." -ForegroundColor Cyan

# Формируем запрос к YandexGPT
$url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

$body = @{
    modelUri = "gpt://$FOLDER_ID/yandexgpt/latest"
    completionOptions = @{
        stream = $false
        temperature = 0.5
        maxTokens = 100
    }
    messages = @(
        @{
            role = "user"
            text = "Привет! Кратко представься."
        }
    )
} | ConvertTo-Json -Depth 5

$headers = @{
    "Authorization" = "Api-Key $API_KEY"
    "Content-Type" = "application/json"
}

try {
    Write-Host "?? Отправляю запрос к YandexGPT..." -ForegroundColor Yellow
    
    $response = Invoke-RestMethod -Uri $url -Method POST -Headers $headers -Body $body -ErrorAction Stop
    
    Write-Host "? УСПЕХ! YandexGPT работает!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Ответ от AI:" -ForegroundColor Cyan
    Write-Host $response.result.message.text -ForegroundColor White
    
} catch {
    Write-Host "? ОШИБКА!" -ForegroundColor Red
    Write-Host $_.Exception.Message
    Write-Host ""
    Write-Host "Тело ошибки:" -ForegroundColor Red
    Write-Host $_.ErrorDetails.Message
}
