# CLI-Anything 项目研究

[importance: 0.8] [access_count: 1] [date: 2026-03-14]

---

## 项目概述

**CLI-Anything** 由港大开发，将任何软件转换为 AI Agent 可用的 CLI 工具。

- **GitHub**: https://github.com/HKUDS/CLI-Anything
- **Stars**: 12.8k+
- **License**: MIT

## 核心功能

一条命令为任何软件生成 CLI：
```
/cli-anything ./gimp
```

## 7 阶段流程

1. Analyze - 扫描源代码
2. Design - 设计命令结构
3. Implement - 构建 CLI
4. Plan Tests - 创建测试计划
5. Write Tests - 实现测试
6. Document - 更新文档
7. Publish - 发布安装

## 支持平台

- Claude Code（主要）
- OpenCode
- Qodercli
- Codex

## 已验证软件

11 个软件，1508 个测试全部通过：
- GIMP、Blender、Inkscape（图形）
- LibreOffice（办公）
- OBS Studio、Kdenlive、Shotcut（视频）
- Audacity（音频）
- Draw.io（图表）

## 关键特性

- 调用真实软件后端（非模拟）
- 无 UI 自动化，纯 CLI 可靠性
- 内置 JSON 输出，Agent 友好
- 状态管理（撤销/重做）

---

*来源：2026-03-14 对话研究*