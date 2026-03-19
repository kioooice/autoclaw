# L1: CLI-Anything 概览

## 项目概述
- **GitHub**: https://github.com/HKUDS/CLI-Anything
- **Stars**: 12.8k+
- **License**: MIT
- **开发者**: 港大

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

## 已验证软件（11 个，1508 测试通过）
| 类别 | 软件 |
|------|------|
| 图形 | GIMP、Blender、Inkscape |
| 办公 | LibreOffice |
| 视频 | OBS Studio、Kdenlive、Shotcut |
| 音频 | Audacity |
| 图表 | Draw.io |

## 关键特性
- 调用真实软件后端（非模拟）
- 无 UI 自动化，纯 CLI 可靠性
- 内置 JSON 输出，Agent 友好
- 状态管理（撤销/重做）

## 支持平台
Claude Code、OpenCode、Qodercli、Codex

---
*创建于 2026-03-14*