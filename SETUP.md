# 新电脑快速配置

## 方法 1：自动配置（推荐）

克隆仓库后运行：

```powershell
git clone https://github.com/kioooice/autoclaw.git
cd autoclaw
.\scripts\setup-new-pc.ps1
```

脚本会自动：
- ✅ 检查 Git 配置
- ✅ 安装 Skillhub CLI
- ✅ 配置 MATON_API_KEY（需要你输入）
- ✅ 创建每周自动更新任务

## 方法 2：手动配置

### 1. 安装 Skillhub

```powershell
# Windows PowerShell
curl -fsSL https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/latest.tar.gz -o latest.tar.gz
tar -xzf latest.tar.gz
# 然后运行 scripts/setup-new-pc.ps1
```

### 2. 设置环境变量

```powershell
$env:MATON_API_KEY = "your-api-key"
[Environment]::SetEnvironmentVariable("MATON_API_KEY", "your-api-key", "User")
```

### 3. 添加 PATH

```powershell
$binDir = "$env:USERPROFILE\.local\bin"
$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
[Environment]::SetEnvironmentVariable("PATH", "$binDir;$userPath", "User")
```

## 已配置内容

| 内容 | 说明 |
|------|------|
| 记忆系统 | `memory/` 三层架构 |
| Agency Agents | 19 个技能（工程/设计/社媒/产品） |
| Skillhub CLI | 技能商店（中国加速） |
| api-gateway | 100+ API 网关 |
| 自动更新 | 每周一 10:00 |

## 注意事项

- `MATON_API_KEY` 需要在每台电脑手动设置
- 首次使用需要到 https://maton.ai/settings 授权第三方 API

---

*创建于 2026-03-13*