# Agency Agents for OpenClaw

> 将 [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents) 转换为 OpenClaw Skills

---

## 📦 已转换的技能

| 技能 | 描述 | 来源 |
|:---|:---|:---|
| **agency-frontend-dev** | 前端开发专家 - React/Vue/Angular、性能优化、无障碍 | Engineering |
| **agency-content-creator** | 内容创作专家 - 多平台内容策略、品牌故事 | Marketing |
| **agency-sprint-prioritizer** | 冲刺规划专家 - 敏捷规划、优先级排序、资源分配 | Product |

---

## 🚀 安装方法

### Windows (自动安装)

双击运行 `install-agency-agents.bat`

### 手动安装

将技能文件夹复制到 OpenClaw skills 目录：

```bash
# Windows
copy /Y "skills\agency-frontend-dev" "%USERPROFILE%\.agents\skills\"
copy /Y "skills\agency-content-creator" "%USERPROFILE%\.agents\skills\"
copy /Y "skills\agency-sprint-prioritizer" "%USERPROFILE%\.agents\skills\"
```

---

## 🎯 使用方法

安装后，在 OpenClaw 对话中使用：

```
"激活前端开发专家，帮我优化这个 React 组件的性能"
"激活内容创作专家，制定一个季度的内容日历"
"激活冲刺规划专家，用 RICE 框架评估这些功能"
```

---

## 📝 转换说明

### 转换内容
- ✅ Agent 人格定义（角色、性格、记忆）
- ✅ 核心能力和专业技能
- ✅ 工作流程和交付物模板
- ✅ 成功指标和评估标准
- ✅ 沟通风格和语气

### 适配修改
- 添加 OpenClaw skill 头部元数据
- 添加 `tools` 声明（web_fetch, read, write 等）
- 翻译关键概念为中文
- 添加使用示例

---

## 🔮 未来扩展

可继续转换的 Agent：

**Engineering (5个)**
- Backend Architect (后端架构师)
- AI Engineer (AI工程师)
- DevOps Automator (DevOps自动化)
- Security Engineer (安全工程师)
- Rapid Prototyper (快速原型)

**Marketing (8个)**
- Growth Hacker (增长黑客)
- Reddit Community Builder (Reddit社区)
- Xiaohongshu Specialist (小红书专家)
- Zhihu Strategist (知乎策略师)
- ...

**Design (6个)**
- UI Designer (UI设计师)
- UX Researcher (UX研究员)
- Whimsy Injector (趣味注入师)
- ...

**Paid Media (7个)**
- PPC Campaign Strategist (PPC策略师)
- Paid Social Strategist (付费社交)
- ...

---

## 📄 许可证

与原项目一致：MIT License

---

## 🙏 致谢

- 原始项目: [msitarzewski/agency-agents](https://github.com/msitarzewski/agency-agents)
- 今日 GitHub Trending #1 (27k+ stars)
