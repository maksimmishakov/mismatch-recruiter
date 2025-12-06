# C:\recruitment-ai\worker.ps1
# Главный воркер - собирает резюме и логирует

. C:\recruitment-ai\config.ps1
. C:\recruitment-ai\scrapers\hh_scraper.ps1
. C:\recruitment-ai\scrapers\github_scraper.ps1

Write-Log "=========================================="
Write-Log "🚀 НАЧАЛО ЦИКЛА СКРЕЙПИНГА"
Write-Log "=========================================="

# GitHub
Write-Log "[1/2] Скрейп GitHub..."
$githubData = Get-GitHubProfiles -SearchQueries @("language:python stars:>50 location:Moscow")
Write-Log "✓ GitHub: $($githubData.Count) профилей`n"

# HH
Write-Log "[2/2] Скрейп HH.ru..."
$hhData = Get-HHResumes -Keywords @("python developer", "старший разработчик")
Write-Log "✓ HH: $($hhData.Count) резюме`n"

# Объединяем
$allData = @()
$allData += $githubData
$allData += $hhData

Write-Log "📊 Всего собрано: $($allData.Count) кандидатов"

# Сохраняем
$backupPath = "C:\recruitment-ai\backups\resumes_$(Get-Date -Format 'yyyy-MM-dd_HHmmss').json"
mkdir "C:\recruitment-ai\backups" -ErrorAction SilentlyContinue | Out-Null

if ($allData.Count -gt 0) {
    $allData | ConvertTo-Json | Out-File $backupPath -Encoding UTF8
    Write-Log "💾 Сохранено: $backupPath"
} else {
    Write-Log "⚠️ Нет данных для сохранения"
}

Write-Log "=========================================="
Write-Log "✅ ЦИКЛ ЗАВЕРШЁН"
Write-Log "=========================================="

Write-Host "`n"
Write-Host "ИТОГИ:" -ForegroundColor Green
Write-Host "  GitHub:  $($githubData.Count) профилей"
Write-Host "  HH.ru:   $($hhData.Count) резюме"
Write-Host "  ВСЕГО:   $($allData.Count) кандидатов" -ForegroundColor Cyan
