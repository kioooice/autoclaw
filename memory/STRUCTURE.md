# Memory System v2.0

基于 MemoryOS 论文改进的三层记忆架构。

## 核心理念

> **不是所有记忆都同等重要**
> 短期 → 中期 → 长期，需要经过"热度评估"

## 目录结构

```
memory/
├── working/              # 短期记忆 - 当前会话（自动清理）
│   └── session.json      # 会话临时数据
│
├── episodic/             # 中期记忆 - 近期热点
│   ├── hot/              # 高频访问（最近 7 天 + 多次引用）
│   │   └── *.md
│   ├── warm/             # 中频访问（最近 30 天）
│   │   └── *.md
│   └── heat.json         # 热度评分记录
│
├── profile/              # 长期记忆 - 用户画像（持久化）
│   ├── facts.md          # 客观事实
│   └── preferences.md    # 用户偏好
│
├── insights/             # 心智模型 - 反思洞察（持久化）
│   └── insights.md
│
├── world/                # [兼容旧版] 世界事实
│   └── facts.md
│
├── experiences/          # [兼容旧版] 每日经历
│   └── *.md
│
├── archive/              # 归档 - 过期信息
│   └── *.md
│
├── STRUCTURE.md          # 本说明文件
├── AGENT-SYNC.md         # 分身同步协议
└── MEMORY.md             # 索引文件
```

## 三层记忆架构（MemoryOS 论文）

### Layer 1: Working Memory（短期记忆）

| 特性 | 说明 |
|------|------|
| 存储位置 | `working/session.json` |
| 生命周期 | 当前会话 |
| 淘汰策略 | 会话结束自动清理 |
| 内容 | 当前对话上下文、临时状态 |

### Layer 2: Episodic Memory（中期记忆）

| 特性 | 说明 |
|------|------|
| 存储位置 | `episodic/hot/` 或 `episodic/warm/` |
| 生命周期 | 7-30 天 |
| 淘汰策略 | 热度评估 + 时间衰减 |
| 内容 | 近期项目、正在进行的任务 |

**热度评分公式**：
```
heat_score = access_count × 0.3
           + importance × 0.4
           + recency × 0.2
           + user_explicit × 0.1
```

**晋升条件**：
- `warm → hot`: heat_score > 0.6 且 7 天内有访问
- `hot → profile`: heat_score > 0.8 且用户明确标记重要

**降级条件**：
- `hot → warm`: 7 天无访问
- `warm → archive`: 30 天无访问

### Layer 3: Profile Memory（长期记忆）

| 特性 | 说明 |
|------|------|
| 存储位置 | `profile/` |
| 生命周期 | 永久（除非用户删除） |
| 淘汰策略 | 手动清理或标记过时 |
| 内容 | 用户画像、核心偏好、关键事实 |

---

## 操作规则

### RETAIN（存储）- 带筛选机制

```
信息进入
    ↓
是否重要？ ─否→ 写入 experiences/YYYY-MM-DD.md（原始记录）
    ↓是
是否长期有效？
    ↓是          ↓否
写入 profile/   写入 episodic/warm/
```

**重要性判断标准**：
1. 用户明确说"记住这个"
2. 涉及用户核心偏好
3. 项目关键信息
4. 反复出现的内容

### RECALL（检索）- 分层检索

```
查询请求
    ↓
1. profile/           ← 最高优先
    ↓ 未找到
2. episodic/hot/      ← 近期热点
    ↓ 未找到
3. episodic/warm/     ← 近期内容
    ↓ 未找到
4. insights/          ← 洞察规律
    ↓ 未找到
5. experiences/近7天  ← 原始记录
```

### REFLECT（反思）- 定期执行

**触发条件**：
- Heartbeat 检查（每 2-3 天）
- 用户请求
- episodic/warm/ 文件超过 20 个

**反思流程**：
1. 读取 episodic/ 所有文件
2. 计算热度评分
3. 高热度 → 晋升到 profile/
4. 低热度 → 降级到 archive/
5. 提炼规律 → 写入 insights/

---

## 热度评估系统

### 评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| access_count | 0.3 | 被引用次数 |
| importance | 0.4 | 重要性标记（0-1） |
| recency | 0.2 | 时间衰减（越近越高） |
| user_explicit | 0.1 | 用户明确标记 |

### heat.json 格式

```json
{
  "items": [
    {
      "id": "cli-anything-project",
      "path": "episodic/warm/cli-anything.md",
      "access_count": 3,
      "importance": 0.8,
      "last_access": "2026-03-14T13:00:00Z",
      "user_explicit": true,
      "heat_score": 0.89
    }
  ],
  "last_reflect": "2026-03-14T13:00:00Z"
}
```

---

## 迁移指南

### 从旧架构迁移

| 旧位置 | 新位置 | 条件 |
|--------|--------|------|
| world/facts.md | profile/facts.md | 直接迁移 |
| - | profile/preferences.md | 从 facts.md 提取偏好 |
| experiences/*.md | episodic/warm/ | 近 7 天 |
| experiences/*.md | archive/ | 超过 30 天 |

### 兼容性

旧目录保留，新会话优先使用新架构：
- `world/facts.md` → 仍可读写，但建议迁移到 `profile/`
- `experiences/` → 仍记录日常，但热点内容会晋升到 `episodic/`

---

## 自动化脚本

### 热度评估脚本

位置：`scripts/evaluate-heat.ps1`

功能：
1. 读取 episodic/ 所有文件
2. 计算热度评分
3. 更新 heat.json
4. 执行晋升/降级

### 归档脚本

位置：`scripts/archive-experiences.ps1`

功能：
1. 归档 30 天前的 experiences
2. 归档低热度的 episodic 内容
3. 清理过期的 working 数据

---

## 最佳实践

### 写入时

1. **先判断重要性**：不重要的写 experiences，重要的写 profile
2. **添加元数据**：在文件头标注 `[importance: high]` 等
3. **避免重复**：写入前检索是否已存在

### 检索时

1. **分层检索**：先 profile → episodic → experiences
2. **使用 memory_search**：指定范围
3. **记录访问**：更新 heat.json

### 反思时

1. **定期执行**：每 2-3 天
2. **提炼洞察**：不只移动文件，要提炼规律
3. **清理冗余**：合并重复、删除过时

---

Created: 2026-03-14
Based on: MemoryOS (EMNLP 2025)