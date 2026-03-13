# HEARTBEAT.md

心跳任务清单。每次心跳时检查。

## 周期任务

### 每次心跳（可选执行）

- [ ] 检查是否有待处理的反思任务
- [ ] 检查 memory/experiences/ 是否有需要提炼的内容

### 定期任务（每 2-3 天）

- [ ] 执行 REFLECT：审视近期 experiences，更新 insights
- [ ] 清理过时的 world/facts
- [ ] 合并重复的日常日志

### 每周任务

- [ ] 运行归档脚本：`powershell scripts/archive-experiences.ps1`
- [ ] 检查 archive/ 目录，清理过老的归档文件（超过 90 天）

## 反思触发条件

当满足以下任一条件时，在心跳中执行反思：

1. `memory/experiences/` 有 3+ 天的未处理记录
2. 用户明确要求"反思"或"总结"
3. 发现重复出现的模式/问题

## 反思流程

1. 读取近期 `memory/experiences/*.md`
2. 识别：
   - 重复出现的模式
   - 学到的教训
   - 可复用的最佳实践
3. 更新 `memory/insights/insights.md`
4. 清理已处理的 experiences

---

*保持此文件精简，避免 token 浪费*