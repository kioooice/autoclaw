# 同步 Agency Agents Skills 到 GitHub

## 当前状态
- **已转换**: 11个 skills
- **位置**: `C:\Users\Administrator\.openclaw-autoclaw\workspace\skills\`

## 方案1: 手动上传 (推荐)

### 步骤1: 打包文件
```powershell
# 在PowerShell中运行
Compress-Archive -Path "C:\Users\Administrator\.openclaw-autoclaw\workspace\skills\agency-*" -DestinationPath "C:\Users\Administrator\Desktop\agency-agents-skills.zip"
```

### 步骤2: 上传到GitHub
1. 访问 https://github.com/kioooice/autoclaw
2. 点击 "Add file" → "Upload files"
3. 上传 `agency-agents-skills.zip`
4. 或者解压后上传整个 `skills/` 文件夹

## 方案2: 安装Git后自动同步

### 安装Git
```powershell
# 下载Git安装程序
Invoke-WebRequest -Uri "https://github.com/git-for-windows/git/releases/download/v2.45.0.windows.1/Git-2.45.0-64-bit.exe" -OutFile "$env:TEMP\git-installer.exe"

# 运行安装程序
Start-Process -FilePath "$env:TEMP\git-installer.exe" -ArgumentList "/VERYSILENT /NORESTART" -Wait
```

### 配置Git并推送
```bash
# 配置Git
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 克隆仓库
git clone https://github.com/kioooice/autoclaw.git
cd autoclaw

# 复制skills
cp -r C:\Users\Administrator\.openclaw-autoclaw\workspace\skills\agency-* .

# 提交并推送
git add .
git commit -m "Add 11 Agency Agents skills for OpenClaw"
git push origin main
```

## 方案3: 使用GitHub Desktop

1. 下载 GitHub Desktop: https://desktop.github.com/
2. 登录你的GitHub账号
3. Clone `kioooice/autoclaw` 仓库
4. 复制 `agency-*` 文件夹到仓库目录
5. 提交并推送

## 📁 需要同步的文件

```
skills/
├── agency-frontend-dev/SKILL.md
├── agency-backend-architect/SKILL.md
├── agency-ai-engineer/SKILL.md
├── agency-devops-automator/SKILL.md
├── agency-content-creator/SKILL.md
├── agency-growth-hacker/SKILL.md
├── agency-zhihu-strategist/SKILL.md
├── agency-xiaohongshu-specialist/SKILL.md
├── agency-bilibili-strategist/SKILL.md
├── agency-ui-designer/SKILL.md
├── agency-sprint-prioritizer/SKILL.md
├── README.md
├── AGENTS-LIST.md
├── CONTENT-AGENTS.md
└── install-agency-agents.bat
```

## 🔧 安装方法 (目标机器)

```bash
# 克隆仓库
git clone https://github.com/kioooice/autoclaw.git
cd autoclaw

# 复制到OpenClaw skills目录
# Windows:
copy /Y "skills\agency-*" "%USERPROFILE%\.agents\skills\"

# 或运行安装脚本
install-agency-agents.bat
```

## 📊 已转换Skills清单

| # | 技能 | 部门 | 描述 |
|:---:|:---|:---|:---|
| 1 | agency-frontend-dev | Engineering | 前端开发专家 |
| 2 | agency-backend-architect | Engineering | 后端架构师 |
| 3 | agency-ai-engineer | Engineering | AI工程师 |
| 4 | agency-devops-automator | Engineering | DevOps自动化 |
| 5 | agency-content-creator | Marketing | 内容创作专家 |
| 6 | agency-growth-hacker | Marketing | 增长黑客 |
| 7 | agency-zhihu-strategist | Marketing | 知乎策略师 |
| 8 | agency-xiaohongshu-specialist | Marketing | 小红书专家 |
| 9 | agency-bilibili-strategist | Marketing | B站策略师 |
| 10 | agency-ui-designer | Design | UI设计师 |
| 11 | agency-sprint-prioritizer | Product | 冲刺规划专家 |

---

**建议**: 先用方案1手动上传，同时我可以帮你继续转换微信公众号和抖音策略师skill。
