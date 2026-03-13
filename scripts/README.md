# Memory Maintenance Scripts

记忆系统维护脚本。

## archive-experiences.ps1

自动归档 30 天前的 experiences。

```powershell
# archive-experiences.ps1
# 用法: .\scripts\archive-experiences.ps1

$workspace = $env:USERPROFILE + "\.openclaw-autoclaw\workspace"
$experiencesDir = "$workspace\memory\experiences"
$archiveDir = "$experiencesDir\archive"
$thresholdDays = 30

# 创建归档目录
if (-not (Test-Path $archiveDir)) {
    New-Item -ItemType Directory -Path $archiveDir -Force | Out-Null
    Write-Host "Created archive directory: $archiveDir"
}

# 获取当前日期
$now = Get-Date
$threshold = $now.AddDays(-$thresholdDays)

# 查找需要归档的文件
$filesToArchive = Get-ChildItem -Path $experiencesDir -Filter "*.md" -File | Where-Object {
    $_.Name -match "^\d{4}-\d{2}-\d{2}\.md$"
}

$archived = 0
foreach ($file in $filesToArchive) {
    # 从文件名解析日期
    if ($file.Name -match "^(\d{4})-(\d{2})-(\d{2})\.md$") {
        $fileDate = [DateTime]::new([int]$matches[1], [int]$matches[2], [int]$matches[3])
        
        if ($fileDate -lt $threshold) {
            $destPath = "$archiveDir\$($file.Name)"
            Move-Item -Path $file.FullName -Destination $destPath -Force
            Write-Host "Archived: $($file.Name)"
            $archived++
        }
    }
}

Write-Host "`nSummary: Archived $archived file(s) older than $thresholdDays days"
```

## reflect.ps1

执行反思流程，提炼 insights。

```powershell
# reflect.ps1
# 用法: .\scripts\reflect.ps1

$workspace = $env:USERPROFILE + "\.openclaw-autoclaw\workspace"
$experiencesDir = "$workspace\memory\experiences"
$insightsFile = "$workspace\memory\insights\insights.md"

Write-Host "=== Memory Reflection ==="
Write-Host "Analyzing recent experiences..."

# 列出近 7 天的 experiences
$recentFiles = Get-ChildItem -Path $experiencesDir -Filter "*.md" -File | Where-Object {
    $_.Name -match "^\d{4}-\d{2}-\d{2}\.md$"
} | Sort-Object Name -Descending | Select-Object -First 7

Write-Host "`nRecent experiences to review:"
foreach ($f in $recentFiles) {
    Write-Host "  - $($f.Name)"
}

Write-Host "`n=== Reflection Checklist ==="
Write-Host "1. Read each experience file"
Write-Host "2. Identify patterns and lessons"
Write-Host "3. Update insights/insights.md"
Write-Host "4. Mark processed experiences"
Write-Host "`nRun this manually during Heartbeat or when requested."
```

---

## Cron / Heartbeat 集成

在 HEARTBEAT.md 中添加：

```markdown
### 每周执行

- [ ] 运行 `powershell scripts/archive-experiences.ps1` 归档旧 experiences
- [ ] 运行反思流程，更新 insights
```

---

*Created: 2026-03-13*