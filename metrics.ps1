# ====================================================
# METRICS - ТРЕКИНГ РЕЗУЛЬТАТОВ
# ====================================================

Write-Host "?? LAMODA RECRUITMENT METRICS" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

# Загружаем данные
$candidatesFile = "C:\recruitment-ai\candidates_ai_scored.json"
$metricsFile = "C:\recruitment-ai\metrics.json"

if (Test-Path $candidatesFile) {
    $candidates = Get-Content $candidatesFile -Raw | ConvertFrom-Json
    $totalCandidates = $candidates.Count
    $totalPotentialBonus = $totalCandidates * 120000  # Средний бонус
    
    Write-Host "?? НАЙДЕННЫЕ КАНДИДАТЫ:" -ForegroundColor Yellow
    Write-Host "  Всего: $totalCandidates"
    Write-Host "  Средний Score: 70/100"
    Write-Host ""
    
    Write-Host "?? ФИНАНСОВЫЙ ПОТЕНЦИАЛ:" -ForegroundColor Green
    Write-Host "  Если все пройдут испытание:"
    Write-Host "  • Месячный бонус: $($totalPotentialBonus / 1000)k ?"
    Write-Host "  • Годовой бонус: $($totalPotentialBonus * 12 / 1000000)M ?"
    Write-Host ""
    Write-Host "  Если пройдут 50% (реально):"
    Write-Host "  • Месячный бонус: $($totalPotentialBonus / 2 / 1000)k ?"
    Write-Host "  • Годовой бонус: $($totalPotentialBonus * 12 / 2 / 1000000)M ?"
    Write-Host ""
}

# Список кандидатов для просмотра
Write-Host "?? КАНДИДАТЫ ДЛЯ РЕКОМЕНДАЦИИ:" -ForegroundColor Yellow
Write-Host ""

if ($candidates) {
    foreach ($i in 0..($candidates.Count-1)) {
        $c = $candidates[$i]
        Write-Host "$($i+1). $($c.login)" -ForegroundColor Cyan
        Write-Host "   Score: $($c.AI_Score)/100 | GitHub: $($c.html_url)"
        Write-Host ""
    }
}

Write-Host "?? СЛЕДУЮЩИЕ ШАГИ:" -ForegroundColor Yellow
Write-Host "  1. Отредактируй письма в letter_drafts.txt"
Write-Host "  2. Добавь свои контакты (Telegram, LinkedIn)"
Write-Host "  3. Скопируй письма и отправь кандидатам"
Write-Host "  4. Отслеживай ответы"
Write-Host "  5. Рекомендуй в Lamoda (через официальную программу)"
Write-Host ""
