# ====================================================
# INTELLIGENT CANDIDATE ROUTING
# ====================================================

Write-Host "?? INTELLIGENT CANDIDATE ROUTING" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

$config = Get-Content "C:\recruitment-ai\enterprise_config.json" | ConvertFrom-Json
$candidates = Get-Content "C:\recruitment-ai\candidates_filtered_safe.json" | ConvertFrom-Json

$routing = @{}

# Для каждой компании — ищем подходящих кандидатов
foreach ($company in $config.companies) {
    $matched = 0
    Write-Host "?? Matching for $($company.name)..." -ForegroundColor Yellow
    
    foreach ($candidate in $candidates) {
        # 1. Проверяем город
        $cityMatch = $company.cities | Where-Object { $candidate.location -like "*$_*" }
        
        # 2. Проверяем скилы
        $skillMatch = $false
        foreach ($requiredSkill in $company.skills) {
            if ($candidate.bio -like "*$requiredSkill*" -or $candidate.login -like "*$requiredSkill*") {
                $skillMatch = $true
            }
        }
        
        # 3. Проверяем score
        $scoreMatch = $candidate.AI_Score -ge $company.min_score
        
        if ($cityMatch -and $skillMatch -and $scoreMatch) {
            $routing[$company.id] += @($candidate)
            $matched++
        }
    }
    
    Write-Host "   ? $matched кандидатов подходят для $($company.name)" -ForegroundColor Green
}

Write-Host ""
Write-Host "?? ROUTING SUMMARY:" -ForegroundColor Yellow
$totalRevenue = 0
foreach ($company in $config.companies) {
    $count = ($routing[$company.id] | Measure-Object).Count
    if ($count -gt 0) {
        $revenue = $count * $company.bonus * 0.5
        $totalRevenue += $revenue
        Write-Host "   $($company.name): $count кандидатов = $([Math]::Round($revenue / 1000))k?" -ForegroundColor Cyan
    }
}

Write-Host ""
Write-Host "?? TOTAL MONTHLY POTENTIAL: $([Math]::Round($totalRevenue / 1000))k ?" -ForegroundColor Green
Write-Host "?? TOTAL ANNUAL POTENTIAL: $([Math]::Round($totalRevenue * 12 / 1000000))M ?" -ForegroundColor Green
Write-Host ""

# Сохраняем маршрутизацию
$routing | ConvertTo-Json | Set-Content -Path "C:\recruitment-ai\routing_results.json"
Write-Host "? Routing results saved!" -ForegroundColor Green
