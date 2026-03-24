# Trae IDE 技能移植包

从 OpenClaw 技能库精选的适合 Trae IDE 的开发技能。

## 技能清单

### 核心技能（第一批）

| 文件 | 用途 | 优先级 |
|------|------|--------|
| `code.md` | 编码工作流（规划→实现→验证→测试） | ⭐⭐⭐⭐⭐ |
| `systematic-debugging.md` | 系统化调试方法论 | ⭐⭐⭐⭐⭐ |
| `test-driven-development.md` | TDD 测试驱动开发 | ⭐⭐⭐⭐⭐ |
| `git-essentials.md` | Git 命令和工作流 | ⭐⭐⭐⭐⭐ |

### 增强技能（第二批）

| 文件 | 用途 | 优先级 |
|------|------|--------|
| `brainstorming.md` | 创意/功能探索，设计阶段使用 | ⭐⭐⭐⭐ |
| `context-hub.md` | 获取第三方库最新文档，减少幻觉 | ⭐⭐⭐⭐ |
| `security-auditor.md` | 代码安全审计，审查漏洞 | ⭐⭐⭐⭐ |
| `receiving-code-review.md` | 处理代码审查反馈 | ⭐⭐⭐⭐ |
| `requesting-code-review.md` | 请求代码审查 | ⭐⭐⭐⭐ |

### 高级技能（第三批）

| 文件 | 用途 | 优先级 |
|------|------|--------|
| `self-improving.md` | 自我反思+持续改进 | ⭐⭐⭐ |
| `finishing-a-development-branch.md` | 开发分支完成流程 | ⭐⭐⭐ |

## 移植说明

### 1. 理解技能结构

每个 `.md` 文件包含：
- **触发条件**：何时激活此技能
- **步骤/流程**：具体执行方法
- **工具**：需要的工具支持
- **注意事项**：常见问题和最佳实践

### 2. 适配 Trae IDE

需要修改的部分：
- 工具调用方式（根据 Trae 的 tool 接口调整）
- 文件路径引用
- 命令行指令（如适用）

### 3. 触发关键词

建议为每个技能设置触发关键词：

```
code → "写代码"、"实现功能"、"编码"
debug → "调试"、"报错"、"bug"
tdd → "测试驱动"、"先写测试"
git → "git"、"提交"、"分支"、"合并"
brainstorm → "头脑风暴"、"设计方案"、"怎么实现"
security → "安全审计"、"漏洞检查"
code-review → "代码审查"、"review"
```

## 快速开始

1. 选择一个技能文件
2. 理解其工作流程
3. 适配 Trae IDE 的工具接口
4. 测试并迭代优化

## 来源

这些技能来自 OpenClaw 技能库，经过筛选适合 IDE 开发场景。

- 技能仓库：https://github.com/openclaw/skills
- ClawHub：https://clawhub.com

---

*整理时间：2026-03-23*