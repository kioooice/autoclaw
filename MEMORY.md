# MEMORY.md - 长期记忆

这是我的长期记忆中枢。每次主会话启动时会自动加载。

## 记忆系统架构

采用**仿生记忆模型**（灵感来自 Hindsight）：

```
memory/
├── world/           → World（世界事实）：客观知识、用户偏好
├── experiences/     → Experiences（经历）：我发生了什么
├── insights/        → Mental Models（心智模型）：反思后的理解
└── STRUCTURE.md     → 系统说明
```

详细结构见 `memory/STRUCTURE.md`

## 每次会话必做

1. 读取 `memory/STRUCTURE.md` 了解系统
2. 用 `memory_search` 检索相关记忆
3. 需要时读取具体文件

## 记忆操作

### RETAIN（存储）

识别到重要信息时自动写入：
- 用户偏好 → `memory/world/facts.md`
- 项目知识 → `memory/world/facts.md`
- 经历事件 → `memory/experiences/YYYY-MM-DD.md`
- 提炼洞察 → `memory/insights/insights.md`

### RECALL（检索）

对话中通过 `memory_search` 检索：
- 搜索词要具体，涵盖多个可能的关键词
- 检索后用 `memory_get` 精读相关片段

### REFLECT（反思）

定期执行（Heartbeat 或用户请求）：
1. 审视近期 experiences
2. 提炼可复用的规律
3. 更新 insights
4. 清理过时的 world/facts

### SKILL CREATION（技能创建）

**触发条件**：完成复杂任务后（多步骤、涉及工具组合、解决问题）

**流程**：
1. 识别任务中的可复用模式
2. 提炼为结构化技能（步骤、工具、注意事项）
3. 写入 `skills/auto-generated/技能名.md`
4. 下次类似任务时优先使用该技能

**技能改进**：
- 使用技能时记录效果（成功/失败/改进点）
- 定期更新技能文件，纳入改进

### 技能文件格式

```markdown
# 技能名

## 触发条件
- 什么时候应该使用这个技能

## 步骤
1. ...
2. ...

## 工具
- 工具1：用途
- 工具2：用途

## 注意事项
- ...

## 改进记录
- YYYY-MM-DD：改进内容
```

## 当前上下文

### 用户信息
- 时区：GMT+8（Asia/Shanghai）
- GitHub：https://github.com/kioooice
- **多电脑接力使用**：需要在不同电脑间同步工作状态和记忆

### 已安装工具
| 工具 | 用途 | 源 |
|------|------|-----|
| skill-seekers | 文档/GitHub/PDF/视频 → AI Skills | https://github.com/yusufkaraaslan/Skill_Seekers |
| agent-reach | AI Agent 互联网能力 | https://github.com/Panniantong/Agent-Reach |
| mcporter | MCP 服务转发 | - |
| **Skillhub** | 技能商店 CLI（中国加速） | `skillhub search/install/list` |
| **api-gateway** | 100+ API 统一网关 | Maton.ai |

### Agency Agents
已安装 19 个技能：工程 7、设计 3、社媒/内容 6、产品/策略 3
源：https://github.com/msitarzewski/agency-agents

### 自动生成技能
- `skills/auto-generated/memory-system-setup.md` — 记忆系统搭建流程

### 待办
- agency-horizon-news 尚未推送到 GitHub
- 论文格式完善（摘要、关键词、目录、参考文献）

### 🔄 分身同步（重要）

**所有分身共享同一个 `memory/` 目录，通过 Git 同步。**

| 时机 | 操作 |
|------|------|
| 启动时 | 读取 MEMORY.md + world/facts.md + insights + 近3天日志 |
| 运行中 | 重要信息写入 memory/ 目录（不是心理笔记） |
| 结束时 | `git add . && git commit -m "sync" && git push` |
| 换电脑 | `git pull` 先同步 |

详细协议：`memory/AGENT-SYNC.md`

### 已知问题
- memory_search 搜索后端未启用（provider: none），暂不可用
- **解决方案**：在 openclaw.json 中配置 memory-lancedb 扩展（需要 OpenAI API Key）

### 归档脚本
- `scripts/archive-experiences.ps1` - 归档 30 天前的 experiences
- 用法：`powershell scripts/archive-experiences.ps1`

### 自动更新
- **Cron 任务**：每周一 10:00 (Asia/Shanghai)
- **Windows 任务计划**：`Skillhub-Daily-Upgrade`（每周一 10:00）
- 下次运行：2026/3/16 10:00:00

---

*创建于 2026-03-13，基于 Hindsight 设计理念*