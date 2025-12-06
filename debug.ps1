# C:\recruitment-ai\debug.ps1

# 1. Принудительно включаем современный протокол безопасности (TLS 1.2)
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# 2. Чистим токен от пробелов
$t = $env:GITHUB_TOKEN
if ($t) { $t = $t.Trim() }

Write-Host "=== ДИАГНОСТИКА ТОКЕНА ===" -ForegroundColor Cyan
Write-Host "Токен в системе: '$t'"
Write-Host "Длина: $($t.Length) симв."

# 3. Пробуем самый простой запрос (Кто я?)
$h = @{
    "Authorization" = "token $t"
    "User-Agent" = "Test-Bot"
}

try {
    Write-Host "Отправляю запрос в GitHub..."
    $u = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $h
    Write-Host "✅ УСПЕХ! Токен рабочий." -ForegroundColor Green
    Write-Host "Логин: $($u.login)" -ForegroundColor Green
}
catch {
    Write-Host "❌ ОШИБКА: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "СОВЕТ: Если 401 — токен МЕРТВ (отозван). Нужно создать новый." -ForegroundColor Yellow
}
Write-Host "=========================="
