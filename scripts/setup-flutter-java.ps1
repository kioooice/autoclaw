# Flutter + JDK 17 环境配置脚本
# 请以管理员身份运行此脚本

Write-Output "=== Flutter + JDK 17 环境配置 ==="

# 1. 添加 Flutter 到系统 Path
Write-Output ""
Write-Output "[1] 添加 Flutter 到系统 Path..."
$flutterBin = "D:\01-DevTools\flutter\flutter\bin"

if (Test-Path $flutterBin) {
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    if ($currentPath -notlike "*$flutterBin*") {
        $newPath = $currentPath.TrimEnd(";") + ";" + $flutterBin
        [Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
        Write-Output "    ✓ Flutter 已添加到系统 Path: $flutterBin"
    } else {
        Write-Output "    ✓ Flutter 已在 Path 中"
    }
} else {
    Write-Output "    ✗ Flutter 目录不存在: $flutterBin"
}

# 2. 检查 Java 是否已安装
Write-Output ""
Write-Output "[2] 检查 Java 环境..."
$javaCmd = Get-Command java -ErrorAction SilentlyContinue
if ($javaCmd) {
    Write-Output "    ✓ Java 已安装: $($javaCmd.Source)"
} else {
    Write-Output "    ✗ Java 未安装"
    Write-Output ""
    Write-Output "请选择安装方式："
    Write-Output "  - 方案 A: winget install Microsoft.OpenJDK.17"
    Write-Output "  - 方案 B: 手动下载 https://adoptium.net/temurin/releases/?version=17"
    Write-Output ""
    Write-Output "安装完成后，请再次运行此脚本设置 JAVA_HOME"
    exit 0
}

# 3. 设置 JAVA_HOME（如果 Java 已安装）
Write-Output ""
Write-Output "[3] 设置 JAVA_HOME..."

# 尝试自动检测 JDK 路径
$jdkPaths = @(
    "C:\Program Files\Eclipse Adoptium\jdk-*",
    "C:\Program Files\Microsoft\jdk-*",
    "C:\Program Files\Java\jdk-*",
    "C:\Program Files\Oracle\Java\jdk-*"
)

$jdkPath = $null
foreach ($pattern in $jdkPaths) {
    $found = Get-ChildItem $pattern -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($found) {
        $jdkPath = $found.FullName
        break
    }
}

if ($jdkPath) {
    Write-Output "    检测到 JDK 路径: $jdkPath"
    
    [Environment]::SetEnvironmentVariable("JAVA_HOME", $jdkPath, "Machine")
    Write-Output "    ✓ JAVA_HOME 已设置"
    
    # 添加 %JAVA_HOME%\bin 到 Path
    $javaBin = $jdkPath + "\bin"
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
    if ($currentPath -notlike "*$javaBin*") {
        $newPath = $currentPath.TrimEnd(";") + ";" + $javaBin
        [Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
        Write-Output "    ✓ %JAVA_HOME%\bin 已添加到 Path"
    } else {
        Write-Output "    ✓ %JAVA_HOME%\bin 已在 Path 中"
    }
} else {
    Write-Output "    ✗ 无法自动检测 JDK 路径"
    Write-Output "    请手动设置："
    Write-Output "    $jdkPath = 'C:\Program Files\Eclipse Adoptium\jdk-17.x.x-hotspot'"
    Write-Output "    [Environment]::SetEnvironmentVariable('JAVA_HOME', $jdkPath, 'Machine')"
}

Write-Output ""
Write-Output "=== 配置完成 ==="
Write-Output "请重新打开 PowerShell/终端 使环境变量生效"
Write-Output ""
Write-Output "验证命令："
Write-Output "  flutter --version"
Write-Output "  java -version"
Write-Output "  echo $JAVA_HOME"