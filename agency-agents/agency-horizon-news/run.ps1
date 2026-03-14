# Horizon News Runner
# PowerShell script to run Horizon News agency

param(
    [string]$Action = "generate",
    [string]$Date = "today"
)

Write-Host "🚀 Horizon News - AI Tech News Curator" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Horizon is installed
$horizonPath = "$env:USERPROFILE\Horizon"
$horizonInstalled = Test-Path $horizonPath

if (-not $horizonInstalled) {
    Write-Host "⚠️  Horizon 未安装。正在克隆仓库..." -ForegroundColor Yellow
    
    # Clone the repository
    try {
        git clone https://github.com/Thysrael/Horizon.git $horizonPath
        Write-Host "✅ Horizon 仓库已克隆到 $horizonPath" -ForegroundColor Green
    } catch {
        Write-Host "❌ 克隆失败: $_" -ForegroundColor Red
        exit 1
    }
}

# Navigate to Horizon directory
Set-Location $horizonPath

# Check for Python/uv
$uvInstalled = Get-Command uv -ErrorAction SilentlyContinue
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue

if ($uvInstalled) {
    Write-Host "📦 使用 uv 运行 Horizon..." -ForegroundColor Cyan
    try {
        uv sync
        uv run horizon generate --date $Date
    } catch {
        Write-Host "❌ 运行失败: $_" -ForegroundColor Red
        exit 1
    }
} elseif ($pythonInstalled) {
    Write-Host "🐍 使用 Python 运行 Horizon..." -ForegroundColor Cyan
    try {
        pip install -e . -q
        python -m horizon generate --date $Date
    } catch {
        Write-Host "❌ 运行失败: $_" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "❌ 未找到 Python 或 uv。请先安装 Python。" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ Horizon News 运行完成！" -ForegroundColor Green
Write-Host "📄 输出文件位置: $horizonPath\output\" -ForegroundColor Gray
