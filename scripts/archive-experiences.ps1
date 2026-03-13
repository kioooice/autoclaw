# archive-experiences.ps1
# 归档 30 天前的 experiences 文件

param(
    [int]$Days = 30
)

$workspace = $env:USERPROFILE + "\.openclaw-autoclaw\workspace"
$experiencesDir = "$workspace\memory\experiences"
$archiveDir = "$experiencesDir\archive"
$thresholdDays = $Days

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