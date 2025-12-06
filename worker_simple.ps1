. C:\recruitment-ai\config.ps1

Write-Log "=========================================="
Write-Log "START SCRAPING"
Write-Log "=========================================="

Write-Log "GitHub Search..."
$token = $env:GITHUB_TOKEN

if ($token) {
    $headers = @{
        Authorization = "token $token"
        Accept = "application/vnd.github.v3+json"
        User-Agent = "PS-Bot"
    }
    
    try {
        $url = "https://api.github.com/search/users?q=language:python+stars:%3E50&per_page=5"
        $response = Invoke-RestMethod -Uri $url -Headers $headers -TimeoutSec 10
        
        $count = $response.items.Count
        Write-Log "GitHub: $count profiles found"
        Write-Host "GitHub: $count" -ForegroundColor Green
    }
    catch {
        Write-Log "GitHub Error: $($_.Exception.Message)"
        Write-Host "GitHub Error" -ForegroundColor Red
    }
}
else {
    Write-Log "GitHub Token missing"
    Write-Host "No token" -ForegroundColor Red
}

Write-Log "=========================================="
Write-Log "DONE"
Write-Log "=========================================="
