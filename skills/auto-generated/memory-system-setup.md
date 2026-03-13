# memory-system-setup

自动创建。从 2026-03-13 完善记忆系统任务中提炼。

## 触发条件

- 用户要求"完善记忆系统"或"改进知识积累"
- 需要设计或重构本地记忆架构

## 步骤

1. **检查现有结构**：读取 `memory/` 目录，确认 world/experiences/insights 是否存在
2. **提炼历史数据**：扫描近期日志，将关键信息写入 `world/facts.md`
3. **启用标签系统**：为 facts 添加 `[标签]` 前缀便于分类
4. **创建归档脚本**：`scripts/archive-experiences.ps1` 归档旧数据
5. **更新 HEARTBEAT**：添加定期反思和归档任务
6. **记录 insights**：技术发现、踩坑记录

## 工具

- `read`：读取现有文件
- `write` / `edit`：更新记忆文件
- `exec`：创建目录、检查结构

## 注意事项

- `memory_search` 需要 OpenAI API Key，无则跳过语义搜索
- 标签格式：`[标签1] [标签2] 内容`
- 归档阈值：30 天

## 改进记录

- 2026-03-13：初始创建，基于 Hermes Agent "自主创建技能" 机制