# 新电脑快速配置脚本
# 用法：在 PowerShell 中运行 .\setup-new-pc.ps1

param(
    [switch]$SkipGit,
    [switch]$SkipSkillhub,
    [switch]$SkipEnv
)

$ErrorActionPreference = "Continue"

Write-Host @"
========================================
  OpenClaw Workspace 新电脑配置
========================================
"@ -ForegroundColor Cyan

# 1. Git 配置
if (-not $SkipGit) {
    Write-Host "`n[1/4] 检查 Git 配置..." -ForegroundColor Yellow
    
    $gitName = git config --global user.name 2>$null
    $gitEmail = git config --global user.email 2>$null
    
    if (-not $gitName) {
        $name = Read-Host "请输入 Git 用户名"
        git config --global user.name $name
    } else {
        Write-Host "  Git 用户名: $gitName" -ForegroundColor Green
    }
    
    if (-not $gitEmail) {
        $email = Read-Host "请输入 Git 邮箱"
        git config --global user.email $email
    } else {
        Write-Host "  Git 邮箱: $gitEmail" -ForegroundColor Green
    }
    
    Write-Host "  Git 配置完成" -ForegroundColor Green
}

# 2. Skillhub 安装
if (-not $SkipSkillhub) {
    Write-Host "`n[2/4] 检查 Skillhub..." -ForegroundColor Yellow
    
    $skillhubPath = "$env:USERPROFILE\.local\bin\skillhub.cmd"
    
    if (Test-Path $skillhubPath) {
        Write-Host "  Skillhub 已安装" -ForegroundColor Green
    } else {
        Write-Host "  正在安装 Skillhub..." -ForegroundColor Yellow
        
        # 创建目录
        $installBase = "$env:USERPROFILE\.skillhub"
        $binDir = "$env:USERPROFILE\.local\bin"
        New-Item -ItemType Directory -Path $installBase -Force | Out-Null
        New-Item -ItemType Directory -Path $binDir -Force | Out-Null
        
        # 下载最新版本
        $tmpDir = "$env:TEMP\skillhub-install"
        New-Item -ItemType Directory -Path $tmpDir -Force | Out-Null
        
        Invoke-WebRequest -Uri "https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/latest.tar.gz" -OutFile "$tmpDir\latest.tar.gz"
        
        # 解压
        cd $tmpDir
        tar -xzf latest.tar.gz
        
        # 复制文件
        Copy-Item "$tmpDir\cli\skills_store_cli.py" "$installBase\" -Force
        Copy-Item "$tmpDir\cli\skills_upgrade.py" "$installBase\" -Force
        Copy-Item "$tmpDir\cli\version.json" "$installBase\" -Force
        Copy-Item "$tmpDir\cli\metadata.json" "$installBase\" -Force
        
        # 创建 wrapper
        $wrapperContent = @"
@echo off
set PYTHONPATH=%USERPROFILE%\.skillhub
set CLI=%USERPROFILE%\.skillhub\skills_store_cli.py
python "%CLI%" %*
"@
        $wrapperContent | Out-File -FilePath "$binDir\skillhub.cmd" -Encoding ascii -Force
        
        # 添加到 PATH
        $userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        if ($userPath -notlike "*$binDir*") {
            [Environment]::SetEnvironmentVariable("PATH", "$binDir;$userPath", "User")
        }
        
        # 清理
        cd $PSScriptRoot
        Remove-Item $tmpDir -Recurse -Force
        
        Write-Host "  Skillhub 安装完成" -ForegroundColor Green
    }
}

# 3. 环境变量
if (-not $SkipEnv) {
    Write-Host "`n[3/4] 检查环境变量..." -ForegroundColor Yellow
    
    $matonKey = [Environment]::GetEnvironmentVariable("MATON_API_KEY", "User")
    
    if ($matonKey) {
        Write-Host "  MATON_API_KEY 已配置" -ForegroundColor Green
    } else {
        Write-Host "  MATON_API_KEY 未配置" -ForegroundColor Red
        $key = Read-Host "请输入 MATON_API_KEY（回车跳过）"
        if ($key) {
            [Environment]::SetEnvironmentVariable("MATON_API_KEY", $key, "User")
            $env:MATON_API_KEY = $key
            Write-Host "  MATON_API_KEY 已设置" -ForegroundColor Green
        }
    }
}

# 4. Windows 任务计划（每周自动更新技能）
Write-Host "`n[4/4] 配置自动更新任务..." -ForegroundColor Yellow

$taskName = "Skillhub-Weekly-Upgrade"
$scriptPath = "$PSScriptRoot\skillhub-upgrade.ps1"

if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
    Write-Host "  任务计划已存在" -ForegroundColor Green
} else {
    $trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At "10:00 AM"
    $action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -File `"$scriptPath`""
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Force | Out-Null
    Write-Host "  任务计划创建完成（每周一 10:00）" -ForegroundColor Green
}

# 完成
Write-Host @"

========================================
  配置完成！
========================================

下一步：
1. 重启 PowerShell 使 PATH 生效
2. 运行 'skillhub list' 验证安装
3. 开始使用 OpenClaw

仓库地址：https://github.com/kioooice/autoclaw

"@ -ForegroundColor Cyan