# 向量记忆系统 & 自学习系统

## 快速开始

### 向量记忆系统

```bash
# 建立索引
python scripts/vector_memory_v2.py index

# 搜索
python scripts/vector_memory_v2.py search "查询内容"

# 查看状态
python scripts/vector_memory_v2.py status
```

### 自学习系统

```bash
# 学习成功模式
python scripts/self_learning.py learn "模式内容" success

# 学习失败教训
python scripts/self_learning.py learn "错误模式" failure

# 查看已学模式
python scripts/self_learning.py patterns

# 保护重要模式
python scripts/self_learning.py protect <id>

# 整合学习成果
python scripts/self_learning.py consolidate

# 查看统计
python scripts/self_learning.py stats

# 导出模式
python scripts/self_learning.py export
```

### 自动学习

```bash
# 从近 7 天经历中自动学习
python scripts/auto_learn.py --days 7

# 预览模式（不实际记录）
python scripts/auto_learn.py --days 7 --dry-run

# 会话结束钩子（学习 + 索引 + 整合）
python scripts/session_end_hook.py
```

## 自动提取内容

自动学习会从经历文件中提取：

| 类型 | 关键词 |
|------|--------|
| **解决方案** | 设置、安装、配置、解决 |
| **问题诊断** | 原因、根因、因为、由于 |
| **最佳实践** | 建议、推荐、注意、教训 |
| **成功标记** | ✅、完成、解决 |
| **失败标记** | ❌、失败、错误 |

## 文件位置

```
memory/
├── .vectors/
│   ├── memory.db      # 向量数据库
│   └── learning.db    # 自学习数据库
├── insights/
│   └── patterns.json  # 导出的模式
└── ...
```

## 在对话中使用

### 搜索记忆

当需要查找相关信息时：

```
python scripts/vector_memory_v2.py search "用户的偏好"
python scripts/vector_memory_v2.py search "最近的错误"
```

### 记录学习

当完成任务后，记录学到的经验：

```bash
# 成功的模式
python scripts/self_learning.py learn "解决方案描述" success

# 失败的教训
python scripts/self_learning.py learn "错误原因描述" failure
```

## EWC++ 防遗忘机制

- **成功**：重要性 +0.05，EWC 权重 +0.1
- **失败**：重要性 -0.025，EWC 权重 -0.05
- **受保护**：衰减速度减半
- **长期未用**：自动衰减

## 下一步优化

1. **自动索引**：在 HEARTBEAT 中自动调用 `vector_memory_v2.py index`
2. **自动学习**：在对话结束时自动调用 `self_learning.py learn`
3. **集成到 AGENTS.md**：在启动时显示自学习统计

---

*创建于 2026-03-25*