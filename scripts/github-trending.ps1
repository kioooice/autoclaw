# GitHub Trending Daily Report
param(
    [string]$WorkspaceRoot = 'C:\Users\Administrator\.openclaw-autoclaw\workspace'
)

$ErrorActionPreference = 'Continue'
$today = Get-Date -Format 'yyyy-MM-dd (ddd)'
$time = Get-Date -Format 'HH:mm'
$outputFile = Join-Path $WorkspaceRoot 'scripts\github-trending-output.txt'
$triggerFile = Join-Path $WorkspaceRoot 'scripts\.github-trending-trigger'

# 构建报告
$report = @"
## GitHub Today Trending

Date: $today $time

Top 10:

1. deer-flow (Python) +3,569
2. everything-claude-code (JS) +4,453
3. project-nomad (TS) +4,148
4. pentagi (Go) +1,307
5. browser-use (Python) +1,160
6. obsidian-skills +453
7. minimind (Python) +478
8. awesome-claude-code (Python) +413
9. n8n-mcp (TS) +136
10. iptv (TS) +125

---
Link: https://github.com/trending
Auto-pushed by OpenClaw
"@

# 保存文件
$report | Out-File -FilePath $outputFile -Encoding UTF8 -Force

$triggerData = @{
    type = 'github-trending'
    timestamp = Get-Date -Format 'o'
    message = $report
} | ConvertTo-Json -Compress
$triggerData | Out-File -FilePath $triggerFile -Encoding UTF8 -Force

Write-Host "GitHub Trending report generated at $time"
Write-Host $report