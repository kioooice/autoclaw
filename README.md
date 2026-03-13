# OpenClaw Workspace

个人 AI Agent 工作空间，支持多电脑接力使用。

## 快速开始

**新电脑配置：**

```powershell
git clone https://github.com/kioooice/autoclaw.git
cd autoclaw
.\scripts\setup-new-pc.ps1
```

详细说明见 [SETUP.md](SETUP.md)

## 目录结构

```
├── memory/              # 记忆系统（三层架构）
│   ├── world/           # 世界事实、用户偏好
│   ├── experiences/     # 每日经历
│   └── insights/        # 提炼的洞察
├── skills/              # 技能库
│   ├── auto-generated/  # 自动生成的技能
│   ├── agency-*/        # Agency Agents
│   └── api-gateway/     # 100+ API 网关
├── scripts/             # 维护脚本
│   ├── setup-new-pc.ps1 # 新电脑配置
│   └── skillhub-upgrade.ps1 # 技能更新
├── MEMORY.md            # 长期记忆索引
├── AGENTS.md            # Agent 行为规范
└── SETUP.md             # 新电脑配置指南
```

## 已安装工具

| 工具 | 用途 |
|------|------|
| Skillhub | 技能商店 CLI（中国加速） |
| api-gateway | 100+ API 统一网关 |
| Agency Agents | 19 个专业技能 |

## 环境变量

- `MATON_API_KEY` - api-gateway 所需，在 https://maton.ai/settings 获取

---

*同步自多台电脑*