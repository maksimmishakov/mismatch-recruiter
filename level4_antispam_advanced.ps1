# ====================================================
# ADVANCED ANTI-SPAM SYSTEM
# ====================================================

Write-Host "??? ANTI-SPAM PROTECTION SYSTEM" -ForegroundColor Cyan
Write-Host "===============================" -ForegroundColor Cyan
Write-Host ""

# Загружаем конфиг
$config = Get-Content "C:\recruitment-ai\enterprise_config.json" | ConvertFrom-Json
$candidates = Get-Content "C:\recruitment-ai\candidates_ai_scored.json" | ConvertFrom-Json

$filtered = @()
$spamCount = 0
$duplicateCount = 0
$validCount = 0

foreach ($candidate in $candidates) {
    $isSpam = $false
    $reason = ""
    
    # 1. Проверка черного списка
    if (Test-Path "C:\recruitment-ai\blacklist.json") {
        $blacklist = Get-Content "C:\recruitment-ai\blacklist.json" | ConvertFrom-Json
        if ($blacklist -contains $candidate.login) {
            $isSpam = $true
            $reason = "BLACKLISTED"
        }
    }
    
    # 2. Проверка коммитов
    if ($candidate.public_repos -lt $config.anti_spam.min_repos) {
        $isSpam = $true
        $reason = "LOW_REPO_COUNT"
    }
    
    # 3. Проверка фолловеров
    if ($candidate.followers -lt $config.anti_spam.min_followers) {
        $isSpam = $true
        $reason = "LOW_FOLLOWERS"
    }
    
    # 4. Проверка banned keywords
    foreach ($keyword in $config.anti_spam.banned_keywords) {
        if ($candidate.login -like "*$keyword*" -or $candidate.bio -like "*$keyword*") {
            $isSpam = $true
            $reason = "BANNED_KEYWORD: $keyword"
        }
    }
    
    # 5. Проверка скора
    if ($candidate.AI_Score -lt 70) {
        $isSpam = $true
        $reason = "LOW_SCORE"
    }
    
    if ($isSpam) {
        $spamCount++
        Write-Host "? SPAM: $($candidate.login) - $reason" -ForegroundColor Red
    } else {
        $filtered += $candidate
        $validCount++
        Write-Host "? VALID: $($candidate.login) (Score: $($candidate.AI_Score))" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "?? SPAM FILTER RESULTS:" -ForegroundColor Yellow
Write-Host "   Valid candidates: $validCount" -ForegroundColor Green
Write-Host "   Spam detected: $spamCount" -ForegroundColor Red
Write-Host "   Filter rate: $([Math]::Round(($spamCount / ($validCount + $spamCount)) * 100))%" -ForegroundColor Yellow
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Сохраняем очищенную базу
$filtered | ConvertTo-Json | Set-Content -Path "C:\recruitment-ai\candidates_filtered_safe.json"

Write-Host "? Safe candidates saved to: candidates_filtered_safe.json" -ForegroundColor Green
