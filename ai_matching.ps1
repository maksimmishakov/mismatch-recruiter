# C:\recruitment-ai\ai_matching.ps1

[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$apiKey = $env:YANDEX_API_KEY
$folderId = $env:YANDEX_FOLDER_ID

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "   AI MATCHING with Yandex GPT"
Write-Host "=====================================" -ForegroundColor Cyan

if (-not $apiKey -or -not $folderId) {
    Write-Host "ERROR: Missing YANDEX_API_KEY or YANDEX_FOLDER_ID" -ForegroundColor Red
    exit
}

# 1. Load candidates
$candidates = Get-Content "C:\recruitment-ai\candidates.json" | ConvertFrom-Json
Write-Host "Candidates: $($candidates.Count)" -ForegroundColor Green

# 2. Build prompt for Yandex GPT
$prompt = "You are a recruitment AI. Analyze these GitHub developers:`n`n"
foreach ($c in $candidates) {
    $prompt += "- $($c.login): $($c.html_url)`n"
}
$prompt += "`nFor each developer, rate match score (0-100) for Python Developer role.`nProvide JSON output with {name, score, reason}."

Write-Host "Sending to Yandex GPT..." -ForegroundColor Yellow

# 3. Call Yandex GPT API
$headers = @{
    "Authorization" = "Bearer $apiKey"
    "Content-Type" = "application/json"
}

$body = @{
    modelUri = "gpt://$folderId/yandexgpt/latest"
    completionOptions = @{
        stream = $false
        temperature = 0.5
        maxTokens = 2000
    }
    messages = @(
        @{
            role = "user"
            text = $prompt
        }
    )
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod `
        -Uri "https://llm.api.cloud.yandex.net/foundationModels/v1/completion" `
        -Method Post `
        -Headers $headers `
        -Body $body `
        -TimeoutSec 30
    
    $result = $response.result.alternatives[0].message.text
    
    Write-Host "GPT Response:" -ForegroundColor Green
    Write-Host $result
    
    # Save results
    $result | Out-File "C:\recruitment-ai\ai_results.txt"
    Write-Host "Saved: C:\recruitment-ai\ai_results.txt" -ForegroundColor Yellow
}
catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "   DONE!"
Write-Host "=====================================" -ForegroundColor Cyan
