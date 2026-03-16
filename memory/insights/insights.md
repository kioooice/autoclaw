# Insights

心智模型库。存储从经历中反思提炼出的规律、原则、最佳实践。

## 格式规范

每条洞察包含：
- 核心观点
- 来源（哪个经历/对话）
- 适用场景

---

## 工作原则

### 记忆系统设计原则（2026-03-13）

**来源**：学习 Hindsight 项目后本地化实现

1. **记忆分层**：World（事实）→ Experiences（经历）→ Insights（洞察）
   - 事实是静态知识，经历是动态事件，洞察是提炼的规律
   - 不同类型存不同地方，便于精准检索

2. **存储只是开始，反思才是学习**
   - Retain 只是写入，Reflect 才能提炼
   - 定期反思比实时存储更重要

3. **多策略召回优于单一向量搜索**
   - 语义相似 + 关键词精确 + 图关系 + 时间过滤
   - 检索时用多种方式"打捞"记忆

**适用场景**：任何需要持续学习的 Agent 系统

---

## 沟通风格

<!-- 从用户反馈中学习到的沟通偏好 -->

## 最佳实践

<!-- 验证有效的做事方法 -->

### 技能自主创建与改进（2026-03-13）

**来源**：Hermes Agent 核心机制

**原则**：
1. **完成复杂任务后** → 自动提炼可复用模式 → 创建技能文件
2. **使用技能时** → 记录效果 → 定期改进技能

**技能存放位置**：`skills/auto-generated/`

**适用场景**：任何多步骤、涉及工具组合的问题解决过程

## 踩坑记录

<!-- 需要避免的错误 -->

### Git 强制推送场景（2026-03-13）

**来源**：同步到 GitHub 仓库时遇到历史冲突

**现象**：`git push` 报错 "Updates were rejected because the remote contains work that you do not have locally"

**原因**：本地和远程仓库是独立创建的，commit 历史没有共同起点

**解决方案**：
1. **强制推送**（本地是最新状态时）：`git push --force`
2. **合并历史**（需要保留远程内容时）：`git pull --rebase` 或 `git pull --allow-unrelated-histories`

**预防方法**：
- 克隆仓库后再工作，不要本地新建仓库再连接远程
- 或本地新建后，先 `git pull --allow-unrelated-histories` 再提交

**适用场景**：任何 Git 推送被拒绝的场景

---

## 技术发现

### memory_search 当前不可用（2026-03-13）

**来源**：测试记忆系统检索功能

**现象**：`memory_search` 返回 `"provider": "none"`，即使 FTS 模式也返回空结果

**原因**：OpenClaw 的 memory_search 需要 `memory-lancedb` 扩展，需要配置：

```json
// openclaw.json 中添加：
{
  "memory": {
    "provider": "memory-lancedb",
    "config": {
      "embedding": {
        "apiKey": "sk-xxx",  // OpenAI API Key
        "model": "text-embedding-3-small"
      },
      "autoCapture": true,
      "autoRecall": true
    }
  }
}
```

**当前状态**：未配置（用户无 OpenAI API Key，暂不启用语义搜索）

**替代方案**：
- 直接用 `read` 读取 MEMORY.md 和 memory/ 下的文件
- 启动会话时主动加载 MEMORY.md 和近 2-3 天的日志

**适用场景**：任何使用 OpenClaw memory_search 的场景

---

*更新规则：新洞察追加，冲突时更新或标注版本演进*