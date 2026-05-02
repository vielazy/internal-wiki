param(
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
    [string]$TaskName = "AI Coding Wiki - 2h Cycle"
)

$ErrorActionPreference = "Stop"

$scriptPath = Join-Path $RepoRoot "scripts\run_cycle.ps1"
if (-not (Test-Path $scriptPath)) {
    throw "Không tìm thấy script: $scriptPath"
}

$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1)
$trigger.Repetition = New-ScheduledTaskTriggerRepetition -Interval (New-TimeSpan -Hours 2) -Duration ([TimeSpan]::MaxValue)

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -StartWhenAvailable -WakeToRun
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel LeastPrivilege

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings -Principal $principal -Force | Out-Null
Write-Host "Đã tạo Scheduled Task: $TaskName"
Write-Host "Task sẽ chạy mỗi 2 giờ và gọi: $scriptPath"
