# ====================================================
# LEVEL 5: ПРОСТАЯ ФИЛЬТРАЦИЯ (БЫСТРАЯ ВЕРСИЯ)
# ====================================================

$InputFile = "C:\recruitment-ai\candidates.json"
$OutputFile = "C:\recruitment-ai\candidates_ai_scored.json"

Write-Host "?? ФИЛЬТРАЦИЯ КАНДИДАТОВ..." -ForegroundColor Cyan

# Загружаем
$candidates = Get-Content -Path $InputFile -Raw | ConvertFrom-Json | Select-Object -First 10

Write-Host "?? Загружено: $($candidates.Count) кандидатов" -ForegroundColor Yellow

# Проходим по каждому
foreach ($candidate in $candidates) {
    $name = $candidate.login
    
    # Простая логика: если имя выглядит нормально - даем 70, если спам - 30
    if ($name.Length -lt 3 -or $name -match "^[0-9]+$" -or $name -match "bot|spam|test") {
        $score = 30
        Write-Host "? $name : $score/100 (Похоже на спам)" -ForegroundColor Red
    } else {
        $score = 70
        Write-Host "? $name : $score/100 (Годится)" -ForegroundColor Green
    }
    
    # Добавляем балл
    $candidate | Add-Member -MemberType NoteProperty -Name "AI_Score" -Value $score -Force
}

# Сохраняем
$candidates | ConvertTo-Json -Depth 3 | Set-Content -Path $OutputFile -Encoding UTF8

Write-Host ""
Write-Host "? Готово! Сохранено в: $OutputFile" -ForegroundColor Green
