# ========================================
# ТЕСТ Локального AI (Ollama)
# ========================================

Write-Host "?? Тестирование локального AI (Llama3)..." -ForegroundColor Cyan

# Формируем запрос к локальному серверу Ollama
$url = "http://localhost:11434/api/generate"

$body = @{
    model = "llama3" # Указываем, какой "мозг" использовать
    prompt = "Оцени резюме для Python разработчика: 5 лет опыта, Django, Docker, Москва. Напиши краткий вердикт."
    stream = $false # Получить ответ целиком, а не по частям
} | ConvertTo-Json

$headers = @{
    "Content-Type" = "application/json"
}

try {
    Write-Host "?? Отправляю запрос к локальному AI..." -ForegroundColor Yellow
    
    $response = Invoke-RestMethod -Uri $url -Method POST -Headers $headers -Body $body -ErrorAction Stop
    
    Write-Host "? УСПЕХ! Локальный AI работает из скрипта!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Ответ от AI:" -ForegroundColor Cyan
    Write-Host $response.response -ForegroundColor White # У Ollama ответ в поле "response"
    
} catch {
    Write-Host "? ОШИБКА!" -ForegroundColor Red
    Write-Host "Убедись, что Ollama запущена (команда: ollama serve)"
    Write-Host $_.Exception.Message
}
