# HEARTBEAT.md

心跳任务清单。每次心跳时检查。

## 启动时加载（必读）

优先读取 L0 摘要，按需加载详情：

```
1. profile/facts.L0.md
2. profile/preferences.L0.md
3. insights/insights.L0.md
4. episodic/warm/*.L0.md（快速扫描近期项目）
5. 按需读取 L1/L2 详情
```

---

## 周期任务

### 每次心跳（必查）

- [ ] 检查是否有待处理的反思任务
- [ ] 检查 memory/experiences/ 是否有需要提炼的内容
- [ ] **自动学习**：如果当天未执行，运行 `python scripts/auto_learn.py --days 1`

### 定期任务（每 2-3 天）

- [ ] 执行 SESSION COMMIT：自迭代流程（见下方）
- [ ] 清理过时的 profile/facts
- [ ] 合并重复的日常日志
- [ ] **更新向量索引**：`python scripts/vector_memory_v2.py index`
- [ ] **整合学习成果**：`python scripts/self_learning.py consolidate`

### 每周任务

- [ ] 运行归档脚本：`powershell scripts/archive-experiences.ps1`
- [ ] 检查 archive/ 目录，清理过老的归档文件（超过 90 天）
- [ ] **导出学习模式**：`python scripts/self_learning.py export`

---

## 自迭代流程（SESSION COMMIT）

类似 OpenViking 的 commit() 机制，定期提取长期记忆。

### 触发条件

- 每 2-3 天执行一次
- 或用户明确要求"反思"/"总结"/"记住这个"

### 执行步骤

```
1. 读取近期 memory/experiences/*.md（最近 3-7 天）
2. 提取记忆，按 6 类分类：
   - profile     → memory/profile/facts.md
   - preferences → memory/profile/preferences.md
   - entities    → memory/profile/entities/{name}.md
   - events      → memory/profile/events/{date}-{name}.md
   - cases       → memory/insights/cases/{name}.md
   - patterns    → memory/insights/insights.md
3. 去重判断：
   - 是否已存在相似记忆？
   - 是 → 合并或跳过
   - 否 → 创建新文件
4. 更新 L0 摘要（如有变动）
5. 清理已处理的 experiences
```

### 6 类记忆说明

| 类别 | 归属 | 说明 | 可合并 |
|------|------|------|--------|
| profile | user | 用户身份/属性 | ✅ |
| preferences | user | 用户偏好 | ✅ |
| entities | user | 人/项目等实体 | ✅ |
| events | user | 事件/决策 | ❌ |
| cases | agent | 问题+解决方案 | ❌ |
| patterns | agent | 可复用模式 | ✅ |

---

## L0/L1/L2 分层检索

### 检索优先级

```
1. L0 摘要（~100 tokens）→ 快速筛选
2. L1 概览（~1k tokens）→ 理解范围
3. L2 详情（无限制）→ 按需加载
```

### 写入规则

- 新增重要文件 → 同时创建 .L0.md 和 .L1.md
- 更新现有文件 → 同步更新摘要

---

*保持此文件精简，避免 token 浪费*
*更新于 2026-03-19，新增 L0/L1/L2 分层 + 自迭代流程*