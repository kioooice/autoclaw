# MEMORY.md - 长期记忆索引

这是我的长期记忆中枢。每次主会话启动时会自动加载。

## 记忆系统架构 v3.0

融合 **MemoryOS 论文** + **OpenViking 分层加载**：

```
memory/
├── profile/           → 长期记忆（用户画像）
│   ├── facts.md       → 客观事实
│   ├── facts.L0.md    → L0 摘要（~100 tokens）
│   ├── preferences.md → 用户偏好
│   ├── preferences.L0.md
│   ├── entities/      → 人/项目等实体
│   └── events/        → 事件/决策
├── episodic/          → 中期记忆（热度管理）
│   ├── hot/           → 高频访问（7天内）
│   └── warm/          → 中频访问（30天内）
│       └── {topic}/
│           ├── .L0.md → 快速筛选
│           ├── .L1.md → 内容概览
│           └── *.md   → L2 详情
├── insights/          → 心智模型
│   ├── insights.md    → 可复用模式（patterns）
│   ├── insights.L0.md
│   └── cases/         → 问题+解决方案
├── experiences/       → 原始记录（每日）
└── archive/           → 归档
```

## 启动加载流程

**优先读 L0，按需加载详情**：

```
1. profile/facts.L0.md        (~100 tokens)
2. profile/preferences.L0.md  (~100 tokens)
3. insights/insights.L0.md    (~100 tokens)
4. episodic/warm/*.L0.md      (扫描近期项目)
5. 按需读取 L1/L2
```

## L0/L1/L2 分层

| Layer | Token | 用途 |
|-------|-------|------|
| L0 | ~100 | 快速筛选、向量搜索 |
| L1 | ~1k | 理解范围、构建上下文 |
| L2 | 无限制 | 详情、按需加载 |

## 6 类记忆分类

| 类别 | 归属 | 位置 | 可合并 |
|------|------|------|--------|
| profile | user | profile/facts.md | ✅ |
| preferences | user | profile/preferences.md | ✅ |
| entities | user | profile/entities/ | ✅ |
| events | user | profile/events/ | ❌ |
| cases | agent | insights/cases/ | ❌ |
| patterns | agent | insights/insights.md | ✅ |

## 自迭代流程（SESSION COMMIT）

每 2-3 天或用户请求时执行：

```
experiences/*.md → 提取记忆 → 6 类分类 → 去重合并 → 更新 L0 摘要
```

详见 `HEARTBEAT.md`

---

## 当前上下文

### 用户信息
- 时区：GMT+8（Asia/Shanghai）
- GitHub：https://github.com/kioooice
- **多电脑接力使用**：需要在不同电脑间同步工作状态和记忆

### 近期热点（episodic/hot/）
*暂无*

### 近期项目（episodic/warm/）
*暂无*

### 已归档实体（profile/entities/）
- InfoCollector 项目（暂停，改用 Obsidian）

### 已记录事件（profile/events/）
- 2026-03-14：Obsidian 配置完成
- 2026-03-18：阿里百炼模型配置更新、Vibe Coding 教程整理
- 2026-03-19：记忆系统 v3.0 重构
- 2026-03-20：Context Hub 技能安装、重复回复问题解决

### 已记录案例（insights/cases/）
- memory_search 不可用解决方案
- Windows Gateway restart 失败解决方案
- 重复回复问题排查（OpenClaw 版本 bug）

### 已安装工具
| 工具 | 用途 |
|------|------|
| Skillhub | 技能商店 CLI |
| mcporter | MCP 服务转发 |
| skill-seekers | 文档→AI Skills |
| agent-reach | AI Agent 互联网能力 |

### 🔄 分身同步（重要）

| 时机 | 操作 |
|------|------|
| 启动时 | 读 L0 摘要 → 按需加载 L1/L2 |
| 运行中 | 重要信息写入 memory/ 目录 |
| 结束时 | `git add . && git commit -m "sync" && git push` |
| 换电脑 | `git pull` 先同步 |

---

*创建于 2026-03-13*
*v2.0 于 2026-03-14，基于 MemoryOS 论文*
*v3.0 于 2026-03-19，融合 OpenViking L0/L1/L2 + 6类记忆 + 自迭代*