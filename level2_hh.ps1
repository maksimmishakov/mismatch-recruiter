# LEVEL 2: HH.ru Extended Search

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

Write-Host "LEVEL 2.1: HH.ru Search (Extended)" -ForegroundColor Cyan

$keywords = @(
    "python developer",
    "python senior", 
    "backend developer",
    "full stack python",
    "django developer"
)

$allHH = @()

foreach ($kw in $keywords) {
    Write-Host "  Searching: $kw" -ForegroundColor Yellow
    
    try {
        $url = "https://api.hh.ru/resumes?text=$([Uri]::EscapeDataString($kw))&area=1&per_page=15&order_by=publication_time"
        $r = Invoke-RestMethod -Uri $url -TimeoutSec 10
        
        if ($r.items -and $r.items.Count -gt 0) {
            foreach ($item in $r.items) {
                $allHH += @{
                    source = "HH.ru"
                    id = $item.id
                    name = $item.first_name
                    title = $item.title
                    salary = if($item.salary) { "$($item.salary.from)-$($item.salary.to) RUB" } else { "Not specified" }
                    area = $item.area.name
                    updated = $item.updated_at
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

$allHH | ConvertTo-Json -Depth 3 | Out-File "C:\recruitment-ai\data_hh.json"
Write-Host "? HH.ru Total: $($allHH.Count) resumes saved" -ForegroundColor Green
