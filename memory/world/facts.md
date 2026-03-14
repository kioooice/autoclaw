# World Facts

持久化的世界知识库。存储客观事实、用户偏好、项目信息等。

## 格式规范

每条事实用 `-` 开头，可包含标签便于检索：

```
- [标签1] [标签2] 事实内容
```

---

## 用户信息

- [用户] [时区] 时区：GMT+8（Asia/Shanghai）
- [用户] [GitHub] GitHub: https://github.com/kioooice
- [用户] [工作流] **多电脑接力使用**：需要在不同电脑间同步工作状态和记忆

## 偏好设置

- [偏好] [工作流] **先规划后执行**：确定方案后，先写完整规划，用户确认后再执行。适用于所有对话和所有分身。
- [偏好] [沟通] 简洁直接，不废话
- [偏好] [开发] **优先找现成项目**：开发任何东西前，先搜索 GitHub/开源社区是否有现成项目，没有再自己开发。避免重复造轮子。
- [偏好] [浏览器] 使用 **Edge** 浏览器

## 项目知识

### OpenClaw Skills 仓库
- [项目] [GitHub] OpenClaw Skills 仓库：https://github.com/kioooice/autoclaw
- [项目] [技能] 已安装 19 个 Agency Agents（工程 7、设计 3、社媒/内容 6、产品/策略 3）

### Agency Agents 源
- [项目] [技能] Agency Agents 源：https://github.com/msitarzewski/agency-agents
- [项目] [技能] Horizon 新闻聚合源：https://github.com/Thysrael/Horizon
- [项目] [技能] agency-horizon-news 已转换安装

## 工具与环境

### 已安装工具
- [工具] [AI] skill-seekers：文档/GitHub/PDF/视频 → AI Skills（https://github.com/yusufkaraaslan/Skill_Seekers）
- [工具] [AI] agent-reach：AI Agent 互联网能力（https://github.com/Panniantong/Agent-Reach）
- [工具] [MCP] mcporter：MCP 服务转发工具
- [工具] [技能商店] Skillhub：技能商店 CLI，`skillhub search/install/list/upgrade`（中国加速）

### Skillhub
- [工具] 安装位置：`~/.skillhub/` + `~/.local/bin/skillhub`
- [工具] 命令：`skillhub search <关键词>`、`skillhub install <slug>`、`skillhub upgrade`
- [工具] 索引源：https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/skills.json

### api-gateway
- [工具] Maton API Gateway，连接 100+ 第三方 API
- [工具] 需要 `MATON_API_KEY` 环境变量（已配置）
- [工具] 管理面板：https://maton.ai/settings

### Cron 任务
- [自动化] 每周技能自动更新：周一 10:00 (Asia/Shanghai)
- [自动化] OpenClaw cron：`~/.openclaw/cron/jobs.json`
- [自动化] Windows 任务计划：`Skillhub-Daily-Upgrade`（每周一 10:00）

### Skill 工作流机制
- [技能] [工作流] Skill 本身支持单对话工作流自动化
- [技能] [工作流] 通过 SKILL.md 定义：触发条件、步骤、工具、注意事项
- [技能] [工作流] 触发后 Agent 自动按流程执行多步骤任务
- [技能] [工作流] 自定义工作流目录：`skills/auto-generated/`
- [技能] [工作流] 示例：Code Skill（Planning→Implement→Verify→Test）、seo-content-writer

### 待推送项目
- [待办] agency-horizon-news 尚未推送到 GitHub

---

*更新规则：新事实追加到对应分类末尾，过时事实标记删除而非移除*