[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$apiKey = $env:YANDEX_API_KEY
$folderId = $env:YANDEX_FOLDER_ID

Write-Host "AI MATCHING" -ForegroundColor Cyan

$candidates = Get-Content "C:\recruitment-ai\candidates.json" | ConvertFrom-Json
Write-Host "Loaded: $($candidates.Count) candidates"

$prompt = "Rate these GitHub developers for Python role: "
foreach ($c in $candidates) {
    $prompt += "$($c.login) "
}
$prompt += ". Give scores 0-100."

$headers = @{
    "Authorization" = "Api-Key $apiKey"
    "Content-Type" = "application/json"
}

$body = @{
    modelUri = "gpt://$folderId/yandexgpt/latest"
    messages = @(@{role="user"; text=$prompt})
} | ConvertTo-Json -Depth 5

try {
    Write-Host "Calling Yandex GPT..."
    $r = Invoke-RestMethod `
        -Uri "https://llm.api.cloud.yandex.net/foundationModels/v1/completion" `
        -Method Post `
        -Headers $headers `
        -Body $body `
        -TimeoutSec 30
    
    $text = $r.result.alternatives[0].message.text
    Write-Host "SUCCESS!" -ForegroundColor Green
    Write-Host $text
    
    $text | Out-File "C:\recruitment-ai\ai_results.txt"
}
catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Hint: Check if API key format is correct" -ForegroundColor Yellow
}
