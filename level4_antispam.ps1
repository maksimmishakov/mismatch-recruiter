# ANTI-SPAM Module

$sentDatabase = "C:\recruitment-ai\sent_contacts.csv"
$maxPerHour = 50
$lastSentTime = @{}

function Check-AlreadySent {
    param($username)
    
    if (Test-Path $sentDatabase) {
        $sent = Import-Csv $sentDatabase
        return $username -in $sent.username
    }
    return $false
}

function Log-AsSent {
    param($username)
    
    $entry = @{
        username = $username
        timestamp = Get-Date
        source = "GitHub"
    }
    
    $entry | Export-Csv $sentDatabase -Append -NoTypeInformation
}

function Rate-Limit {
    $currentHour = (Get-Date).Hour
    $sentThisHour = @(Import-Csv $sentDatabase -ErrorAction SilentlyContinue | 
        Where-Object { [datetime]$_.timestamp -gt (Get-Date).AddHours(-1) }).Count
    
    if ($sentThisHour -ge $maxPerHour) {
        $delay = Get-Random -Minimum 30 -Maximum 120
        Write-Host "Rate limit reached. Waiting $delay seconds..."
        Start-Sleep -Seconds $delay
    }
}

Write-Host "? Anti-Spam module loaded"
