# TrendRadar Force Majeure Monitor
# ======================================

$ProjectDir = "C:\Users\CHAOFAN\Desktop\Workspace\Pyproject\News\TrendRadar"
$VenvPython = "C:\Users\CHAOFAN\Desktop\Workspace\Pyproject\News\.venv\Scripts\python.exe"
$PollingInterval = 600  # 10 minutes in seconds
$LockFile = "$ProjectDir\.monitor.lock"

# 单例检查：防止重复运行
if (Test-Path $LockFile) {
    try {
        $lockContent = Get-Content $LockFile -ErrorAction Stop
        $lockPid = [int]$lockContent
        $existingProcess = Get-Process -Id $lockPid -ErrorAction SilentlyContinue

        if ($existingProcess) {
            Write-Host "[INFO] Monitor is already running (PID: $lockPid)" -ForegroundColor Yellow
            Write-Host "[INFO] Exiting to avoid duplicate instances..." -ForegroundColor Yellow
            exit 0
        } else {
            Write-Host "[WARN] Stale lock file found, cleaning up..." -ForegroundColor Yellow
            Remove-Item $LockFile -Force
        }
    } catch {
        Remove-Item $LockFile -Force -ErrorAction SilentlyContinue
    }
}

# 创建锁文件
$CurrentPid = $PID
Set-Content -Path $LockFile -Value $CurrentPid

# 注册清理函数（脚本退出时删除锁文件）
$Cleanup = {
    if (Test-Path $LockFile) {
        Remove-Item $LockFile -Force -ErrorAction SilentlyContinue
    }
}
Register-EngineEvent -SourceIdentifier PowerShell.Exiting -Action $Cleanup -ErrorAction SilentlyContinue

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "TrendRadar Force Majeure Monitor" -ForegroundColor Cyan
Write-Host "Polling: 10 minutes" -ForegroundColor Cyan
Write-Host "Push Window: 08:00-21:00" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[START] Monitor started (PID: $CurrentPid)" -ForegroundColor Green

cd $ProjectDir

try {
    while ($true) {
        Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Starting monitor..." -ForegroundColor Green

        # Set UTF-8 encoding
        $env:PYTHONIOENCODING = "utf-8"

        # Run TrendRadar
        & $VenvPython -m trendradar

        Write-Host "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] Monitor complete, waiting 10 minutes..." -ForegroundColor Yellow
        Write-Host ""

        # Wait 10 minutes
        Start-Sleep -Seconds $PollingInterval
    }
} finally {
    # 清理锁文件
    if (Test-Path $LockFile) {
        Remove-Item $LockFile -Force -ErrorAction SilentlyContinue
    }
    Write-Host "[STOP] Monitor stopped" -ForegroundColor Red
}
