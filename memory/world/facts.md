# 用户事实记录

## 已安装技能

| 技能名 | 触发词 | 路径 | 说明 |
|--------|--------|------|------|
| github-trending-analysis | `今日 GitHub 热点`、`GitHub trending`、`查看 GitHub 热门项目` | ~/.openclaw-autoclaw/skills/github-trending-analysis | GitHub 每日热点分析，生成 Markdown 报告 |
| autoglm-websearch | 联网搜索相关关键词 | ~/.openclaw-autoclaw/skills/autoglm-websearch | AutoGLM 网络搜索 |
| autoglm-browser-agent | 浏览器自动化任务 | ~/.openclaw-autoclaw/skills/autoglm-browser-agent | 智能浏览器自动化 |

## 技术环境

- OS: Windows 10/11
- Shell: PowerShell (默认 GBK 编码，需注意 UTF-8 文件)
- Workspace: C:\Users\Administrator\.openclaw-autoclaw\workspace

## 编码问题记录

- Windows PowerShell 默认 GBK 编码
- UTF-8 文件（如 SKILL.md）读取时会乱码
- 解决方案：使用 `[System.IO.File]::WriteAllText()` 写入 UTF-8

---

*更新于 2026-03-29*