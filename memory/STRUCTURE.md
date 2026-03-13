# Memory System Structure

仿照 Hindsight 的仿生记忆模型，用本地文件实现持续学习。

## 目录结构

```
memory/
├── world/              # 世界事实 - 客观知识
│   ├── facts.md        # 持久化事实库
│   └── YYYY-MM-DD.md   # 日期事实
├── experiences/        # 经历 - 发生在我身上的事
│   └── YYYY-MM-DD.md   # 每日经历
├── insights/           # 心智模型 - 反思后的理解
│   └── insights.md     # 持久化洞察
├── STRUCTURE.md        # 本说明文件
└── YYYY-MM-DD.md       # 日常日志（原始记录）
```

## 三层记忆模型

### 1. World（世界事实）
- 客观知识、用户偏好、项目信息
- 持久化存储，跨会话保留
- 写入条件：用户明确告知的事实

### 2. Experiences（经历）
- 我做了什么、发生了什么
- 按日期记录
- 写入条件：完成重要任务、学到新东西

### 3. Insights（心智模型）
- 反思后形成的规律、原则、最佳实践
- 持久化存储
- 写入条件：从经历中提炼出可复用的知识

## 操作规则

### RETAIN（存储）
- 对话中识别到重要信息 → 写入对应目录
- 用户说"记住这个"、"以后这样" → world/facts.md
- 完成重要任务 → experiences/
- 发现规律/教训 → insights/insights.md

### RECALL（检索）
- 每次对话开始时自动检索相关记忆
- 使用 memory_search 工具查询
- 优先级：insights > world/facts > experiences

### REFLECT（反思）
- 每隔几天或用户要求时执行
- 审视 experiences，提炼 insights
- 更新心智模型

## 自动化触发

1. **对话中**：识别重要信息即时写入
2. **Heartbeat**：定期检查是否需要反思
3. **用户请求**："反思一下"、"总结最近"

## 衰减与清理机制

### Experiences（经历）
- 按日期存储，超过 30 天的自动归档到 `experiences/archive/`
- 归档文件不参与日常检索，除非显式指定

### World/Facts（事实）
- 定期审视，过时的事实标记 `~~删除线~~`
- 合并重复条目
- 单文件超过 500 行时考虑拆分（按主题）

### Insights（洞察）
- 这是**最精炼**的部分，应该保持精简
- 新洞察覆盖旧洞察时，删除旧的
- 单文件控制在 200 行以内

### MEMORY.md（索引）
- 只保留**当前最重要的**摘要
- 不堆砌细节，细节在具体文件里
- 定期精简，删除不再相关的内容

### 检索优先级

```
insights/insights.md  ← 最高优先，精炼的规律
    ↓
memory/world/facts.md ← 重要事实
    ↓
memory/experiences/近7天.md ← 近期经历
    ↓
memory/experiences/archive/ ← 仅在需要时查询
```

---
Created: 2026-03-13