# Agent Collaboration Rules (OpenClaw)

> 来源：D:\02-Projects\project\10\docs\agent-collaboration-sop.md
> 更新日期：2026-03-29

## 核心规则

### 角色定义

| Agent | 角色 | 职责 |
|-------|------|------|
| **Codex** | 主控与最终责任方 | 任务分解、决策、集成、验证、用户报告 |
| **OpenCode** | 小任务并行执行者 | 单文件编辑、测试修复、文档整理、局部脚本 |
| **OpenClaw** | 特种执行者 | 浏览器验证、跨工具执行、长链路自动化 |

### 黄金法则

1. **Codex 是唯一主控** — 所有产品判断、最终集成、验证交付由 Codex 负责
2. **只执行指定流程** — 不承担产品判断与最终集成，不擅自扩大执行面
3. **结构化回传** — 至少包含：状态、执行步骤、结果、证据、风险或阻塞点
4. **遇阻即停** — 出现副作用风险、权限阻塞或目标不清时，立即停止并回传 `blocked`

---

## 何时使用 OpenClaw

### ✅ 适合的场景

- 浏览器自动化验证
- 桌面或本地应用工作流
- 跨工具编排（多系统联动）
- 长链路自动化任务
- 需要真实环境交互的任务

### ❌ 不适合的场景

- 常规代码编辑（应由 Codex 或 OpenCode 直接处理）
- 最终项目集成
- 仅因之前尝试模糊而委派的任务

---

## 路由决策表

| 情况 | 执行者 |
|------|--------|
| 主功能设计或范围决策 | Codex |
| 跨文件集成 | Codex |
| 最终验收和用户报告 | Codex |
| 小范围独立代码修复 | OpenCode |
| 添加或修复某区域的测试 | OpenCode |
| 整理文档或脚本 | OpenCode |
| 浏览器驱动的工作流 | OpenClaw |
| 跨应用自动化 | OpenClaw |
| 长外部工具执行链 | OpenClaw |

---

## 任务卡片格式

### OpenClaw 任务卡

```text
Task owner: OpenClaw

Goal:
[精确的操作目标]

Execution surface:
- Browser / desktop / local runtime / cross-tool workflow

Inputs:
- URLs, tools, credentials source, local paths, or environment notes

Constraints:
- 避免无关副作用
- 执行变得模糊时停止并报告
- 返回证据，而不仅仅是结论

Expected output:
- 执行的步骤
- 涉及的系统
- 结果
- 风险或阻塞点
- 捕获的证据

Done when:
- [...]
```

---

## 回传格式（强制）

每次执行后必须返回：

```text
Status:
[done | done_with_concerns | blocked]

What I completed:
- [...]

Files or systems touched:
- [...]

Verification or evidence:
- [...]

Risks or unresolved points:
- [...]

What Codex should decide next:
- [...]
```

---

## 升级规则

### 从 OpenClaw 升级回 Codex

- 自动化路径变得有风险或模糊
- 外部状态变化可能有副作用
- 环境权限阻止安全完成
- 结果需要产品级判断，而不仅仅是执行

---

## 反模式（避免）

- 把 OpenClaw 当作"最后的希望"桶
- 发送模糊的任务
- 将集成责任从 Codex 移走
- 在同一写入范围上运行多个 worker 而没有明确所有权
- 不改变简报就重试相同的失败委派

---

## 短版本（快速参考）

`Codex` 拥有任务。`OpenCode` 处理小而明确边界任务。`OpenClaw` 处理浏览器、桌面或更长外部自动化等专业执行面。每个委派任务都有紧凑的简报，每个 worker 返回结构化摘要，最终集成和验证总是回到 `Codex`。