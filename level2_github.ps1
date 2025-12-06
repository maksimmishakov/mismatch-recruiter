# LEVEL 2: GitHub Extended Search

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$token = $env:GITHUB_TOKEN
$h = @{"Authorization"="token $token";"User-Agent"="Bot"}

Write-Host "LEVEL 2.2: GitHub Search (Extended)" -ForegroundColor Cyan

$queries = @(
    "language:python location:Moscow stars:>100",
    "language:python followers:>50 location:Russia",
    "language:python created:>2022-01-01 location:Moscow"
)

$allGH = @()
$count = 0

foreach ($q in $queries) {
    Write-Host "  Query: $q" -ForegroundColor Yellow
    
    try {
        $url = "https://api.github.com/search/users?q=$([Uri]::EscapeDataString($q))&per_page=35&sort=followers"
        $r = Invoke-RestMethod -Uri $url -Headers $h -TimeoutSec 10
        
        if ($r.items -and $r.items.Count -gt 0) {
            foreach ($user in $r.items) {
                $allGH += @{
                    source = "GitHub"
                    username = $user.login
                    profile_url = $user.html_url
                    followers = $user.followers
                    repos = $user.public_repos
                    avatar = $user.avatar_url
                }
            }
            Write-Host "    ? Found: $($r.items.Count)" -ForegroundColor Green
        }
    }
    catch {
        Write-Host "    ?? Error" -ForegroundColor Yellow
    }
    
    Start-Sleep -Seconds 2
}

$allGH | ConvertTo-Json -Depth 3 | Out-File "C:\recruitment-ai\data_github.json"
Write-Host "? GitHub Total: $($allGH.Count) profiles saved" -ForegroundColor Green
