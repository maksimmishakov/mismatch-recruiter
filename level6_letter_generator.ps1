# ====================================================
# LEVEL 6: ГЕНЕРАТОР ПЕРСОНАЛЬНЫХ ПИСЕМ
# ====================================================

$InputFile = "C:\recruitment-ai\candidates_ai_scored.json"
$OutputFile = "C:\recruitment-ai\letter_drafts.txt"
$MinScore = 70

Write-Host "MailBox GENERATOR..." -ForegroundColor Cyan

# Загружаем кандидатов
$candidates = Get-Content -Path $InputFile -Raw | ConvertFrom-Json
$approved = $candidates | Where-Object { $_.AI_Score -ge $MinScore }

Write-Host "Approved candidates: $($approved.Count)" -ForegroundColor Yellow

# Шаблоны (на английском чтобы избежать проблем)
$greetings = @(
    "Hi, {0}!",
    "Hello, {0}!",
    "Hey, {0}!"
)

$openings = @(
    "I noticed your GitHub profile - impressive work!",
    "Your projects caught my attention.",
    "I saw your contributions and they look great.",
    "Your code quality is excellent."
)

$propositions = @(
    "We have interesting projects that match your skills. Would you be interested to chat?",
    "We're looking for talented developers like you. Got a moment to discuss?",
    "There's an opportunity that might interest you. Let me know if you want details.",
    "I think you could be a great fit for our team. Interested?"
)

$closings = @(
    "Happy to discuss more. Let me know!",
    "Looking forward to hearing from you!",
    "Feel free to reach out anytime.",
    "Let's talk soon!"
)

# Генерируем письма
$letterText = ""
$count = 0

foreach ($candidate in $approved) {
    $name = $candidate.login
    $url = $candidate.html_url
    $score = $candidate.AI_Score
    
    # Выбираем случайные части
    $greeting = $greetings[(Get-Random -Maximum $greetings.Count)] -f $name
    $opening = $openings[(Get-Random -Maximum $openings.Count)]
    $proposition = $propositions[(Get-Random -Maximum $propositions.Count)]
    $closing = $closings[(Get-Random -Maximum $closings.Count)]
    
    # Собираем письмо
    $letter = @"
=====================================
LETTER #$($count + 1)
Candidate: $name
Score: $score/100
GitHub: $url
=====================================

$greeting

$opening

$proposition

Feel free to check my profile if you'd like: [YOUR_NAME]

$closing

Best regards,
[YOUR_NAME]

---

"@

    $letterText += $letter
    $count++
    
    Write-Host "OK - Letter for $name (Score: $score)" -ForegroundColor Green
}

# Сохраняем
$letterText | Set-Content -Path $OutputFile -Encoding UTF8

Write-Host ""
Write-Host "SUCCESS! Generated $count letters" -ForegroundColor Green
Write-Host "File: $OutputFile" -ForegroundColor Cyan
Write-Host ""
Write-Host "First letter preview:" -ForegroundColor Yellow
Write-Host ($letterText.Split("---")[0]) -ForegroundColor White
