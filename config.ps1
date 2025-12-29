# C:\recruitment-ai\config.ps1

$global:Config = @{
    GoogleCredsPath = "C:\recruitment-ai\google_creds.json"
    SheetName = "Mismatch_Recruitment_DB"
    
    HHApiUrl = "https://api.hh.ru"
    HHSearchKeywords = @(
        "python developer",
        "frontend react",
        "������� �����������"
    )
    
    GitHubToken = $env:GITHUB_TOKEN
    GitHubApiUrl = "https://api.github.com"
    
    TelegramToken = $env:TELEGRAM_BOT_TOKEN
    LogPath = "C:\recruitment-ai\logs\scraper_$(Get-Date -Format 'yyyy-MM-dd').log"
}

function Write-Log {
    param($Message, $Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    Write-Host $logMessage
    Add-Content -Path $Config.LogPath -Value $logMessage
}
