# Case: Windows Gateway Restart 失败

## 问题
`openclaw gateway restart` 在 Windows 上不工作。

## 原因
SIGUSR1 信号在 Windows 不存在。

## 解决方案
- 用 `openclaw gateway stop` + `openclaw gateway start`
- 或在 OpenClaw 应用里重启

## 适用
任何 Windows 环境下的 Gateway 重启。

---
*创建于 2026-03-20 SESSION COMMIT*