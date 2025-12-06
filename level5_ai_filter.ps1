# ====================================================
# LEVEL 5: AI ФИЛЬТРАЦИЯ (ВЕРСИЯ 3.0 - SMARTER)
# ====================================================

$InputFile = "C:\recruitment-ai\candidates.json"
$OutputFile = "C:\recruitment-ai\candidates_ai_scored.json"
$MinScore = 60
$AiModel = "llama3"
$MaxCandidatesToCheck = 5

Write-Host "?? ЗАПУСК AI ФИЛЬТРАЦИИ (ВЕРСИЯ 3.0)..." -ForegroundColor Cyan

# 1. Загружаем данные
$candidates = Get-Content -Path $InputFile -Raw | ConvertFrom-Json
$candidatesToCheck = $candidates | Select-Object -First $MaxCandidatesToCheck
$results = @()

foreach ($candidate in $candidatesToCheck) {
    $name = $candidate.login
    $url = $candidate.html_url
    # Если есть описание профиля - берем его (если нет - пусто)
    $bio = if ($candidate.bio) { $candidate.bio } else { "Нет описания" }
    
    Write-Host "?? $name... " -NoNewline

    # --- ПРОМПТ 3.0 (ЖЕСТКИЙ) ---
    $prompt = @"
Ты рекрутер. Оцени профиль разработчика по шкале 0-100.
Login: $name
Bio: $bio
URL: $url

Правила оценки:
- Если имя похоже на спам или бота (random chars) -> 0-20
- Если обычный ник -> 50-70
- Если есть понятное Bio -> 70-90

ТВОЙ ОТВЕТ ДОЛЖЕН СОДЕРЖАТЬ ТОЛЬКО ОДНО ЧИСЛО.
НЕ ПИШИ НИКАКОГО ТЕКСТА.
"@

    # --- ЗАПРОС ---
    $apiUrl = "http://localhost:11434/api/generate"
    $body = @{
        model = $AiModel
        prompt = $prompt
        stream = $false
    } | ConvertTo-Json

    try {
        $response = Invoke-RestMethod -Uri $apiUrl -Method POST -Body $body -ErrorAction Stop
        $aiRawText = $response.response
        
        # Очищаем ответ от всего кроме цифр
        $cleanScore = $aiRawText -replace "[^0-9]", "" 
        
        # Если нашлось число
        if ($cleanScore -match "^\d+$") {
            $score = [int]$cleanScore
            
            # Обрезаем (если AI выдал 143 из-за глюка)
            if ($score -gt 100) { $score = $score % 100 } 
            
            # Цвет
            $color = if ($score -ge $MinScore) { "Green" } else { "Red" }
            Write-Host "[$score/100]" -ForegroundColor $color
            
            # Сохраняем
            $candidate | Add-Member -MemberType NoteProperty -Name "AI_Score" -Value $score -Force
            $results += $candidate
        } else {
            Write-Host "[???] (Ответ AI: '$aiRawText')" -ForegroundColor Yellow
        }

    } catch {
        Write-Host "? Ошибка" -ForegroundColor Red
    }
}

# Сохраняем
$results | ConvertTo-Json -Depth 3 | Set-Content -Path $OutputFile -Encoding UTF8
Write-Host "`n? Готово! Файл: $OutputFile" -ForegroundColor Cyan
