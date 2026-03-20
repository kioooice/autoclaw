# Case: memory_search 不可用

## 问题
`memory_search` 返回空结果，`"provider": "none"`。

## 原因
OpenClaw 的 memory_search 需要 `memory-lancedb` 扩展 + OpenAI API Key。

## 解决方案
1. 配置 openclaw.json（需要 OpenAI API Key）
2. 或用 `read` 直接读取记忆文件作为替代

## 当前状态
未配置（用户无 OpenAI API Key）

---
*创建于 2026-03-20 SESSION COMMIT*