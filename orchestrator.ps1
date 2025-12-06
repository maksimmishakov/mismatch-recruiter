# ====================================================
# ORCHESTRATOR - ГЛАВНОЕ УПРАВЛЕНИЕ (для Lamoda)
# ====================================================

param(
    [string]$action = "status"  # status, run, schedule, dashboard
)

Write-Host "?? LAMODA RECRUITMENT ORCHESTRATOR" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Загружаем конфиг
$config = Get-Content "C:\recruitment-ai\config.json" | ConvertFrom-Json

function Show-Status {
    Write-Host "?? ТЕКУЩИЙ СТАТУС:" -ForegroundColor Yellow
    Write-Host ""
    
    # Проверяем файлы
    $candidatesFile = "C:\recruitment-ai\candidates_ai_scored.json"
    $lettersFile = "C:\recruitment-ai\letter_drafts.txt"
    
    if (Test-Path $candidatesFile) {
        $count = (Get-Content $candidatesFile | ConvertFrom-Json).Count
        Write-Host "? Кандидатов найдено: $count" -ForegroundColor Green
    } else {
        Write-Host "? Кандидатов не найдено" -ForegroundColor Red
    }
    
    if (Test-Path $lettersFile) {
        $size = (Get-Item $lettersFile).Length
        Write-Host "? Писем подготовлено: $([Math]::Round($size/1024))KB" -ForegroundColor Green
    } else {
        Write-Host "? Писем не подготовлено" -ForegroundColor Red
    }
    
    Write-Host ""
    Write-Host "?? КОНФИГ:" -ForegroundColor Yellow
    Write-Host "  Ключевые слова: $($config.lamoda_search.keywords -join ', ')"
    Write-Host "  Локация: $($config.lamoda_search.locations -join ', ')"
    Write-Host "  Лимит в день: $($config.lamoda_search.daily_limit)"
    Write-Host "  Запуск в: $($config.automation.run_time)"
    Write-Host ""
}

function Run-Full-Cycle {
    Write-Host "?? ЗАПУСК ПОЛНОГО ЦИКЛА:" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "1?? Поиск на GitHub..." -ForegroundColor Cyan
    & "C:\recruitment-ai\level2_github.ps1"
    
    Write-Host ""
    Write-Host "2?? Фильтрация через AI..." -ForegroundColor Cyan
    & "C:\recruitment-ai\level5_simple_filter.ps1"
    
    Write-Host ""
    Write-Host "3?? Генерация писем..." -ForegroundColor Cyan
    & "C:\recruitment-ai\level6_letter_generator.ps1"
    
    Write-Host ""
    Write-Host "? ЦИКЛ ЗАВЕРШЕН!" -ForegroundColor Green
    
    # Отправляем уведомление
    $candidates = Get-Content "C:\recruitment-ai\candidates_ai_scored.json" -Raw | ConvertFrom-Json
    Write-Host "?? Результат: $($candidates.Count) кандидатов готовы к рекомендации" -ForegroundColor Cyan
}

function Show-Dashboard {
    Clear-Host
    Write-Host "г========================================¬" -ForegroundColor Cyan
    Write-Host "¦  LAMODA RECRUITMENT DASHBOARD          ¦" -ForegroundColor Cyan
    Write-Host "L========================================-" -ForegroundColor Cyan
    Write-Host ""
    
    Show-Status
    
    Write-Host ""
    Write-Host "?? КОМАНДЫ:" -ForegroundColor Yellow
    Write-Host "  .\orchestrator.ps1 status     - Показать статус"
    Write-Host "  .\orchestrator.ps1 run        - Запустить поиск сейчас"
    Write-Host "  .\orchestrator.ps1 schedule   - Настроить расписание"
    Write-Host "  .\orchestrator.ps1 dashboard  - Эта панель"
    Write-Host ""
}

# Обработка команд
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
        Write-Host "?? НАСТРОЙКА РАСПИСАНИЯ:" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Расписание уже установлено в Task Scheduler"
        Write-Host "Запуск каждый день в: $($config.automation.run_time)"
        Write-Host ""
        Write-Host "Для изменения времени отредактируй config.json"
    }
    default {
        Show-Dashboard
    }
}
