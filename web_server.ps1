# ====================================================
# WEB SERVER - STANDALONE VERSION
# ====================================================

$port = 5000
$url = "http://localhost:$port/"

Write-Host "?? SERVER STARTED: $url" -ForegroundColor Green

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($url)
$listener.Start()

# ВСТРОЕННЫЙ HTML (чтобы точно заработало)
$htmlContent = @"
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>AI Recruiter</title>
    <style>
        body { background: #2c3e50; color: white; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background: white; color: #333; padding: 40px; border-radius: 10px; width: 400px; text-align: center; box-shadow: 0 10px 20px rgba(0,0,0,0.3); }
        h1 { margin: 0 0 20px; color: #3498db; }
        button { background: #e74c3c; color: white; border: none; padding: 15px 30px; font-size: 18px; border-radius: 5px; cursor: pointer; width: 100%; }
        button:hover { background: #c0392b; }
        #log { margin-top: 20px; font-size: 14px; color: #7f8c8d; text-align: left; background: #ecf0f1; padding: 10px; border-radius: 5px; height: 100px; overflow-y: auto; display: none; }
    </style>
</head>
<body>
    <div class="box">
        <h1>?? AI Recruiter</h1>
        <p>System ready. Click to start search.</p>
        <button onclick="run()">?? START SEARCH</button>
        <div id="log"></div>
    </div>

    <script>
        async function run() {
            const log = document.getElementById('log');
            log.style.display = 'block';
            log.innerHTML = '? Sending request...<br>';
            
            try {
                const res = await fetch('/run-analysis', { method: 'POST', body: JSON.stringify({keyword: 'Python'}) });
                const data = await res.json();
                log.innerHTML += '? Done!<br>';
                log.innerHTML += 'Found: ' + data.count + ' candidates';
            } catch (e) {
                log.innerHTML += '? Error: ' + e;
            }
        }
    </script>
</body>
</html>
"@

while ($true) {
    try {
        $ctx = $listener.GetContext()
        $req = $ctx.Request
        $res = $ctx.Response
        
        Write-Host "Request: $($req.HttpMethod) $($req.Url.LocalPath)" -ForegroundColor Yellow
        
        # Главная страница
        if ($req.Url.LocalPath -eq "/") {
            $buffer = [System.Text.Encoding]::UTF8.GetBytes($htmlContent)
            $res.ContentType = "text/html; charset=utf-8"
            $res.ContentLength64 = $buffer.Length
            $res.OutputStream.Write($buffer, 0, $buffer.Length)
            $res.Close()
            continue
        }
        
        # API
        if ($req.Url.LocalPath -eq "/run-analysis") {
            $json = @{ success = $true; count = 5; message = "Test OK" } | ConvertTo-Json
            $buffer = [System.Text.Encoding]::UTF8.GetBytes($json)
            $res.ContentType = "application/json"
            $res.ContentLength64 = $buffer.Length
            $res.OutputStream.Write($buffer, 0, $buffer.Length)
            $res.Close()
            continue
        }
        
        $res.StatusCode = 404
        $res.Close()
        
    } catch {
        Write-Host "Error" -ForegroundColor Red
    }
}
