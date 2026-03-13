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

## 当前上下文

<!-- 重要的当前状态信息 -->

---

*创建于 2026-03-13，基于 Hindsight 设计理念*