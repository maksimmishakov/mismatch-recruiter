. C:\recruitment-ai\config.ps1

Write-Log "START"

$token = $env:GITHUB_TOKEN

if ($token) {
    $h = @{"Authorization"="token $token";"User-Agent"="Bot"}
    $url = "https://api.github.com/search/users?q=language:python+stars:%3E50&per_page=5"
    
    try {
        $r = Invoke-RestMethod -Uri $url -Headers $h -TimeoutSec 10
        $c = $r.items.Count
        Write-Log "OK: $c profiles"
    }
    catch {
        Write-Log "ERROR: $_"
    }
}
else {
    Write-Log "NO TOKEN"
}

Write-Log "END"
