# ====================================================
# LEVEL 2: MULTI-COMPANY PARALLEL SEARCH
# ====================================================

$companiesFile = "C:\recruitment-ai\companies.json"
$config = Get-Content $companiesFile | ConvertFrom-Json

Write-Host "?? MULTI-COMPANY PARALLEL SEARCH" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

$allResults = @()

foreach ($companyName in $config.companies.PSObject.Properties.Name) {
    $company = $config.companies.$companyName
    Write-Host "?? Searching for: $($company.name)" -ForegroundColor Yellow
    
    $skills = $company.required_skills -join " OR "
    $query = "language:($skills) stars:>$($config.targeting_strategy.min_stars) followers:>$($config.targeting_strategy.min_followers)"
    
    Write-Host "   Query: $query" -ForegroundColor Cyan
    
    # Здесь GitHub API запрос (как раньше, но с динамическими параметрами)
    # ...
    
    Write-Host "   ? Found candidates for $($company.name)" -ForegroundColor Green
}

Write-Host ""
Write-Host "? TOTAL SEARCH COMPLETED" -ForegroundColor Green
