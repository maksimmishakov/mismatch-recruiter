# ====================================================
# ORCHESTRATOR - ������� �Mismatch��� (��� mismatch)
# ====================================================

param(
    [string]$action = "status"  # status, run, schedule, dashboard
)

Write-Host "?? Mismatch RECRUITMENT ORCHESTRATOR" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# ��������� ������
$config = Get-Content "C:\recruitment-ai\config.json" | ConvertFrom-Json

function Show-Status {
    Write-Host "?? ������� ������:" -ForegroundColor Yellow
    Write-Host ""
    
    # ��������� �����
    $candidatesFile = "C:\recruitment-ai\candidates_ai_scored.json"
    $lettersFile = "C:\recruitment-ai\letter_drafts.txt"
    
    if (Test-Path $candidatesFile) {
        $count = (Get-Content $candidatesFile | ConvertFrom-Json).Count
        Write-Host "? ���������� �������: $count" -ForegroundColor Green
    } else {
        Write-Host "? ���������� �� �������" -ForegroundColor Red
    }
    
    if (Test-Path $lettersFile) {
        $size = (Get-Item $lettersFile).Length
        Write-Host "? ����� ������������: $([Math]::Round($size/1024))KB" -ForegroundColor Green
    } else {
        Write-Host "? ����� �� ������������" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "?? ������:" -ForegroundColor Yellow
    Write-Host "  �������� �Mismatch$($config.mismatch_search.keywords -join ', ')"
    Write-Host "  �������Mismatchonfig.mismatch_search.locations -join ', ')"
    Write-Host "  ����� � ��Mismatch$config.mismatch_search.daily_limit)"
    Write-Host "  ������ �: $($config.automation.run_time)"
    Write-Host ""
}

function Run-Full-Cycle {
    Write-Host "?? ������ ������� �����:" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "1?? ����� �� GitHub..." -ForegroundColor Cyan
    & "C:\recruitment-ai\level2_github.ps1"
    
    Write-Host ""
    Write-Host "2?? ���������� ����� AI..." -ForegroundColor Cyan
    & "C:\recruitment-ai\level5_simple_filter.ps1"
    
    Write-Host ""
    Write-Host "3?? ��������� �����..." -ForegroundColor Cyan
    & "C:\recruitment-ai\level6_letter_generator.ps1"
    
    Write-Host ""
    Write-Host "? ���� ��������!" -ForegroundColor Green
    
    # ���������� �����������
    $candidates = Get-Content "C:\recruitment-ai\candidates_ai_scored.json" -Raw | ConvertFrom-Json
    Write-Host "?? ���������: $($candidates.Count) ���������� ������ � ������������" -ForegroundColor Cyan
}

function Show-Dashboard {
    Clear-Host
    Write-Host "�========================================�" -ForegroundColor Cyan
    Write-Host "�MismatchDA RECRUITMENT DASHBOARD          �" -ForegroundColor Cyan
    Write-Host "L========================================-" -ForegroundColor Cyan
    Write-Host ""
    
    Show-Status
    
    Write-Host ""
    Write-Host "?? �������:" -ForegroundColor Yellow
    Write-Host "  .\orchestrator.ps1 status     - �������� ������"
    Write-Host "  .\orchestrator.ps1 run        - ��������� ����� ������"
    Write-Host "  .\orchestrator.ps1 schedule   - ��������� ����������"
    Write-Host "  .\orchestrator.ps1 dashboard  - ��� ������"
    Write-Host ""
}

# ��������� ������
switch ($action) {
    "status" {
        Show-Status
    }
    "run" {
        Run-Full-Cycle
    }
    "dashboard" {
        Show-Dashboard
    }
    "schedule" {
        Write-Host "?? ��������� ����������:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "���������� ��� ����������� � Task Scheduler"
        Write-Host "������ ������ ���� �: $($config.automation.run_time)"
        Write-Host ""
        Write-Host "��� ��������� ������� ������������ config.json"
    }
    default {
        Show-Dashboard
    }
}
