[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$t = $env:GITHUB_TOKEN
if ($t) { $t = $t.Trim() }

Write-Host "TOKEN TEST" -ForegroundColor Cyan
Write-Host "Token: $t"
Write-Host "Length: $($t.Length)"

$h = @{"Authorization"="token $t";"User-Agent"="Bot"}

try {
    $u = Invoke-RestMethod -Uri "https://api.github.com/user" -Headers $h
    Write-Host "SUCCESS" -ForegroundColor Green
    Write-Host "Login: $($u.login)"
}
catch {
    Write-Host "FAIL: $($_.Exception.Message)" -ForegroundColor Red
}
