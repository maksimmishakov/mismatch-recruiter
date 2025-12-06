# C:\recruitment-ai\scrapers\github_scraper.ps1

. C:\recruitment-ai\config.ps1

function Get-GitHubProfiles {
    param([string[]]$SearchQueries = @("language:python stars:>50"))
    
    $allProfiles = @()
    $token = $env:GITHUB_TOKEN
    
    if (-not $token) {
        Write-Log "❌ GitHub token пуст!" "ERROR"
        return $allProfiles
    }
    
    $headers = @{
        "Authorization" = "token $token"
        "Accept" = "application/vnd.github.v3+json"
        "User-Agent" = "PS-Recruiter"
    }
    
    foreach ($query in $SearchQueries) {
        Write-Log "  🔍 GitHub: $query"
        
        try {
            $url = "https://api.github.com/search/users?q=$([Uri]::EscapeDataString($query))&per_page=10"
            $response = Invoke-RestMethod -Uri $url -Headers $headers -TimeoutSec 15
            
            if ($response.items.Count -gt 0) {
                foreach ($user in $response.items) {
                    $allProfiles += @{
                        source = "GitHub"
                        username = $user.login
                        followers = $user.followers
                        profile_url = $user.html_url
                    }
                }
                Write-Log "    ✓ Найдено $($response.items.Count)"
            }
        } catch {
            Write-Log "    ❌ $($_.Exception.Message)" "ERROR"
        }
        
        Start-Sleep -Seconds 2
    }
    
    return $allProfiles
}
