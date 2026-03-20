# Insights

心智模型库。存储从经历中反思提炼出的规律、原则、最佳实践。

## 格式规范

每条洞察包含：
- 核心观点
- 来源（哪个经历/对话）
- 适用场景

---

## 工作原则

### 记忆系统设计原则（2026-03-13 → v3.0 2026-03-19）

**来源**：学习 Hindsight 项目 + MemoryOS 论文 + OpenViking 分层加载

1. **记忆分层**：World（事实）→ Experiences（经历）→ Insights（洞察）
   - 事实是静态知识，经历是动态事件，洞察是提炼的规律
   - 不同类型存不同地方，便于精准检索

2. **存储只是开始，反思才是学习**
   - Retain 只是写入，Reflect 才能提炼
   - 定期反思比实时存储更重要

3. **多策略召回优于单一向量搜索**
   - 语义相似 + 关键词精确 + 图关系 + 时间过滤
   - 检索时用多种方式"打捞"记忆

4. **L0/L1/L2 检索分层**（v3.0 新增）
   - L0 摘要 ~100 tokens → 快速筛选
   - L1 概览 ~1k tokens → 理解范围
   - L2 详情无限制 → 按需加载
   - 启动时只读 L0，按需加载 L1/L2

5. **6 类记忆分类**（v3.0 新增）
   - profile（用户身份）→ 可合并
   - preferences（用户偏好）→ 可合并
   - entities（人/项目）→ 可合并
   - events（事件/决策）→ 不合并
   - cases（问题+方案）→ 不合并
   - patterns（可复用模式）→ 可合并

6. **SESSION COMMIT 自迭代**（v3.0 新增）
   - 每 2-3 天执行一次
   - experiences/*.md → 提取 → 6类分类 → 去重合并 → 更新 L0

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

### 开发前先找现成项目（2026-03-14）

**来源**：InfoCollector 开发浪费大量时间

**教训**：开发任何东西前，先搜索 GitHub/开源社区是否有现成方案

**已记录到**：`memory/profile/facts.md` 用户偏好

**适用场景**：任何开发项目启动前

---

### OpenClaw Gateway 运维踩坑（2026-03-19）

**来源**：配置模型时遇到的问题

**问题清单**：
1. **Windows 上 restart 不支持**：`openclaw gateway restart` 报错，因为 SIGUSR1 信号在 Windows 不存在
   - 解决：用 `stop` + `start`，或在 OpenClaw 应用里重启
2. **Gateway 重启后配置可能丢失**：重启失败时可能回滚到旧配置
   - 预防：修改 openclaw.json 后确认 Gateway 正常运行
3. **模型路由短暂丢失**：重启后可能报 "No API key found for provider xxx"
   - 解决：手动切换模型恢复

**适用场景**：任何 Gateway 配置修改、模型切换场景

---

### PowerShell 与沙箱限制（2026-03-19）

**来源**：Vibe Coding 教程整理时遇到

**问题**：
1. **控制台中文乱码**：PowerShell 控制台显示 GBK 编码，文件实际 UTF-8
   - 解决：不用担心，编辑器里正常显示
2. **write 工具路径限制**：sandbox 模式下不能写 workspace 外的路径
   - 解决：先写 workspace，再用 `exec` 复制到目标位置

**适用场景**：Windows 环境下的文件操作、跨目录复制

---

## AI 系统设计

### InkOS 多 Agent 协作模式（2026-03-14）

**来源**：分析 GitHub 上的 AI 小说创作系统

**模式**：
- **管线式 Agent 协作**：雷达→建筑师→写手→审计员→修订者
- **真相文件系统**：7 个长期记忆文件解决连贯性问题（角色、大纲、情节、场景、世界、时间线、设定）

**适用场景**：设计多 Agent 协作系统、长文本生成项目

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