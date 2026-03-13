# skillhub-upgrade.ps1
# 每周自动更新技能（周一 10:00）

$env:PYTHONPATH = "$env:USERPROFILE\.skillhub"
$skillhub = "$env:USERPROFILE\.local\bin\skillhub.cmd"

Write-Host "=== Skillhub Daily Upgrade ==="
Write-Host "Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

# 运行升级
& $skillhub upgrade

Write-Host "=== Done ==="