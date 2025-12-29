# ====================================================
# METRICS - ������� �����������
# ====================================================

Write-Host "?? Mismatch RECRUITMENT METRICS" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

# ��������� ������
$candidatesFile = "C:\recruitment-ai\candidates_ai_scored.json"
$metricsFile = "C:\recruitment-ai\metrics.json"

if (Test-Path $candidatesFile) {
    $candidates = Get-Content $candidatesFile -Raw | ConvertFrom-Json
    $totalCandidates = $candidates.Count
    $totalPotentialBonus = $totalCandidates * 120000  # ������� �����
    
    Write-Host "?? ��������� ���������:" -ForegroundColor Yellow
    Write-Host "  �����: $totalCandidates"
    Write-Host "  ������� Score: 70/100"
    Write-Host ""
    
    Write-Host "?? ���������� ���������:" -ForegroundColor Green
    Write-Host "  ���� ��� ������� ���������:"
    Write-Host "  � �������� �����: $($totalPotentialBonus / 1000)k ?"
    Write-Host "  � ������� �����: $($totalPotentialBonus * 12 / 1000000)M ?"
    Write-Host ""
    Write-Host "  ���� ������� 50% (�������):"
    Write-Host "  � �������� �����: $($totalPotentialBonus / 2 / 1000)k ?"
    Write-Host "  � ������� �����: $($totalPotentialBonus * 12 / 2 / 1000000)M ?"
    Write-Host ""
}

# ������ ���������� ��� ���������
Write-Host "?? ��������� ��� ������������:" -ForegroundColor Yellow
Write-Host ""

if ($candidates) {
    foreach ($i in 0..($candidates.Count-1)) {
        $c = $candidates[$i]
        Write-Host "$($i+1). $($c.login)" -ForegroundColor Cyan
        Write-Host "   Score: $($c.AI_Score)/100 | GitHub: $($c.html_url)"
        Write-Host ""
    }
}

Write-Host "?? ��������� ����:" -ForegroundColor Yellow
Write-Host "  1. ������������ ������ � letter_drafts.txt"
Write-Host "  2. ������ ���� �������� (Telegram, LinkedIn)"
Write-Host "  3. �������� ������ � ������� ����������"
Write-Host "  4. ���������� ������"
Write-Host "  5. �����Mismatch� mismatch (����� ����������� ���������)"
Write-Host ""
