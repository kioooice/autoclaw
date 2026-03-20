# InfoCollector

信息收集与知识管理桌面应用。

## 功能

- 🚀 快捷键唤起收集窗口（Ctrl+Shift+C）
- 🤖 AI 自动总结内容（DeepSeek）
- 🏷️ AI 自动分类和打标签
- 💾 本地 SQLite 存储
- 🔍 搜索已收集内容

## 技术栈

- **前端**: Next.js 15 + React 19 + Tailwind CSS
- **桌面**: Tauri 2
- **存储**: SQLite
- **AI**: DeepSeek API

## 开发

### 前置要求

- Node.js 18+
- Rust (https://rustup.rs)
- pnpm/npm/yarn

### 安装依赖

```bash
npm install
```

### 开发模式

```bash
npm run tauri:dev
```

### 构建

```bash
npm run tauri:build
```

## 配置

1. 打开应用，点击设置按钮
2. 输入 DeepSeek API Key（从 https://platform.deepseek.com 获取）
3. 可选：修改快捷键

## 使用

1. 按 `Ctrl+Shift+C` 唤起收集窗口
2. 粘贴链接或文本
3. 可选：添加笔记
4. 点击"收集"，AI 将自动总结并分类

## License

MIT