# C:\recruitment-ai\scrapers\hh_scraper.ps1

. C:\recruitment-ai\config.ps1

function Get-HHResumes {
    param([string[]]$Keywords = @("python developer"))
    
    $allResumes = @()
    $headers = @{
        "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    foreach ($keyword in $Keywords) {
        Write-Log "  🔍 HH: $keyword"
        
        try {
            $url = "https://api.hh.ru/resumes?text=$([Uri]::EscapeDataString($keyword))&area=1&per_page=5"
            $response = Invoke-RestMethod -Uri $url -Headers $headers -TimeoutSec 15
            
            if ($response.items.Count -gt 0) {
                foreach ($item in $response.items) {
                    $allResumes += @{
                        source = "HH"
                        id = $item.id
                        name = $item.first_name
                        title = $item.title
                    }
                }
                Write-Log "    ✓ Найдено $($response.items.Count)"
            }
        } catch {
            Write-Log "    ⚠️ Пропуск" "ERROR"
        }
        
        Start-Sleep -Seconds 2
    }
    
    return $allResumes
}
