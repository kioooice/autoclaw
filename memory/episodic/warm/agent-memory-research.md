# Agent 记忆系统调研

[importance: 0.7] [date: 2026-03-19]

---

## 背景

用户认为 OpenViking API 价格太贵（VLM + Embedding），寻找低成本替代方案。

## 对比结论

| 方案 | 成本 | 推荐 |
|------|------|------|
| OpenViking | 高（¥50-200/月） | 功能最强，但贵 |
| Hindsight | 中（可用本地模型零成本） | ✅ 推荐 |
| Hermes Agent | 低（支持 DeepSeek 等便宜模型） | ✅ 推荐 |
| 当前文件方案 | 零 | 简单可控 |

## Hindsight 特点

- 三层架构：World/Experiences/Mental Models
- 三个操作：Retain/Recall/Reflect
- 支持本地模型（Ollama/LMStudio）
- Docker 部署

```bash
docker run -e HINDSIGHT_API_LLM_PROVIDER=ollama \
  ghcr.io/vectorize-io/hindsight:latest
```

## Hermes Agent 特点

- 完整 Agent 框架（类似 OpenClaw）
- 自学习循环，自动创建技能
- 支持 OpenRouter 200+ 模型
- 可从 OpenClaw 迁移

---

*来源：2026-03-19 对话*