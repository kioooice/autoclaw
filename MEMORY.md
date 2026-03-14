# MEMORY.md - 长期记忆索引

这是我的长期记忆中枢。每次主会话启动时会自动加载。

## 记忆系统架构 v2.0

基于 **MemoryOS 论文（EMNLP 2025）** 改进的三层架构：

```
memory/
├── working/           → 短期记忆（会话级，自动清理）
├── episodic/          → 中期记忆（热度管理）
│   ├── hot/           → 高频访问（7天内）
│   └── warm/          → 中频访问（30天内）
├── profile/           → 长期记忆（持久化）
│   ├── facts.md       → 客观事实
│   └── preferences.md → 用户偏好
├── insights/          → 心智模型（反思洞察）
└── archive/           → 归档（过期信息）
```

详细结构见 `memory/STRUCTURE.md`

## 每次会话必做

1. 读取 `memory/STRUCTURE.md` 了解系统
2. 读取 `profile/facts.md` + `profile/preferences.md`
3. 检查 `episodic/hot/` 有无近期热点
4. 需要时用 `memory_search` 检索

## 记忆操作

### RETAIN（存储）- 带筛选

```
重要信息 → profile/（长期）
近期项目 → episodic/warm/（中期）
日常记录 → experiences/（原始）
```

### RECALL（检索）- 分层

```
1. profile/         ← 最高优先
2. episodic/hot/    ← 近期热点
3. episodic/warm/   ← 近期内容
4. insights/        ← 洞察规律
5. experiences/     ← 原始记录
```

### REFLECT（反思）- 定期

1. 计算热度评分
2. 高热度 → 晋升 profile
3. 低热度 → 降级 archive
4. 提炼洞察 → insights

---

## 当前上下文

### 用户信息
- 时区：GMT+8（Asia/Shanghai）
- GitHub：https://github.com/kioooice
- **多电脑接力使用**：需要在不同电脑间同步工作状态和记忆

### 近期热点（episodic/hot/）
*暂无*

### 近期项目（episodic/warm/）
- CLI-Anything 项目研究（2026-03-14）

### 已安装工具
| 工具 | 用途 |
|------|------|
| Skillhub | 技能商店 CLI |
| mcporter | MCP 服务转发 |
| skill-seekers | 文档→AI Skills |
| agent-reach | AI Agent 互联网能力 |

### Skill 工作流机制
- Skill 支持单对话工作流自动化
- 通过 SKILL.md 定义步骤、工具、注意事项
- 自定义工作流目录：`skills/auto-generated/`

### 🔄 分身同步（重要）

| 时机 | 操作 |
|------|------|
| 启动时 | 读取 MEMORY.md + profile/ + insights + 近期 episodic |
| 运行中 | 重要信息写入 memory/ 目录 |
| 结束时 | `git add . && git commit -m "sync" && git push` |
| 换电脑 | `git pull` 先同步 |

---

*创建于 2026-03-13，v2.0 升级于 2026-03-14，基于 MemoryOS 论文*