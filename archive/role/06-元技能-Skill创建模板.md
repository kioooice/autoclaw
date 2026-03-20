# 元技能：创建 Skill 的 Skill

## 触发条件

当需要将散落的领域材料（文档/APIs/代码/规格）转化为可复用的 Skill 时触发。

---

## Skill 目录结构

```
skill-name/
├── SKILL.md          # 必需：入口文件（触发条件 + 边界 + 示例）
├── references/       # 可选：长文档
│   └── index.md      # 推荐：导航索引
├── scripts/          # 可选：辅助脚本
└── assets/           # 可选：模板/配置
```

---

## YAML Frontmatter（必需）

```yaml
---
name: skill-name
description: "做什么 + 什么时候用（触发关键词）"
---
```

规则：
- `name` 必须匹配 `^[a-z][a-z0-9-]*$`
- `description` 必须是可判定的（不是"帮助做X"）

---

## SKILL.md 最小骨架

```markdown
---
name: my-skill
description: "[领域]能力：包含[能力1]，[能力2]。当[触发条件]时使用。"
---

# my-skill Skill

一句话说明边界和产出。

## When to Use This Skill

触发条件：
- [触发条件1：具体任务/关键词]
- [触发条件2]
- [触发条件3]

## Not For / Boundaries

- 这个技能不会做什么
- 必需的输入；如果缺失，先问1-3个问题

## Quick Reference

### 常用模式

**模式1：** 一行解释
```
[可直接粘贴运行的命令/代码片段]
```

## Examples

### Example 1
- Input:
- Steps:
- Expected output:

### Example 2

### Example 3

## References

- `references/index.md`: 导航
- `references/...`: 长文档

## Maintenance

- Sources: 文档/仓库/规格（不要编造）
- Last updated: YYYY-MM-DD
- Known limits: 明确排除的内容
```

---

## 质量检查清单

1. `name` 符合命名规则并匹配目录名
2. `description` 说清楚"做什么 + 什么时候用"
3. 有"When to Use This Skill"和"Not For / Boundaries"
4. Quick Reference ≤ 20 个模式
5. ≥ 3 个可复现的示例
6. 长内容放在 `references/` 并有索引
7. 不确定的内容有验证路径
8. 读起来像操作手册，不是文档堆砌

---

## 工作流程

1. **Scope**: 写出 MUST/SHOULD/NEVER（三句话）
2. **Extract patterns**: 选出10-20个高频模式
3. **Add examples**: ≥3个端到端示例
4. **Define boundaries**: 排除范围 + 必需输入
5. **Split references**: 长文本移入 `references/`
6. **Apply the gate**: 运行检查清单验证
