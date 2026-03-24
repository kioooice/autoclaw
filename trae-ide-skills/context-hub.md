---
name: context-hub
description: >
  使用 Context Hub (chub) 获取第三方库、SDK 或 API 的最新文档。当需要使用某个库（如 OpenAI、Stripe、Anthropic 等）编写代码时，
  先通过 chub 获取最新文档，而不是依赖训练数据中的记忆。触发场景：提到"使用 XX API"、"调用 XX SDK"、"查询 XX 库"、
  "怎么用 XX"、或任何需要调用外部服务/库的编码任务。支持搜索、获取、注释、反馈等功能。
---

# Context Hub - API 文档检索技能

Context Hub 是为 AI 编程代理设计的文档检索工具。通过 `chub` CLI 获取最新、准确的 API 文档，避免幻觉和过时信息。

## 核心功能

| 功能 | 命令 | 用途 |
|------|------|------|
| 搜索文档 | `chub search "<库名>"` | 查找相关文档 ID |
| 获取文档 | `chub get <id> --lang py\|js` | 获取特定语言的文档 |
| 添加注释 | `chub annotate <id> "<注释>"` | 保存本地经验，下次自动显示 |
| 提供反馈 | `chub feedback <id> up\|down` | 评分文档质量，帮助改进 |

## 使用流程

### Step 1 — 搜索文档 ID

```bash
chub search "<库名>"
```

从结果中选择最匹配的 `id`（如 `openai/chat`、`anthropic/sdk`、`stripe/api`）。

### Step 2 — 获取文档

```bash
chub get <id> --lang py    # Python 版本
chub get <id> --lang js    # JavaScript 版本
```

如果文档只有一个语言版本，可省略 `--lang`。

### Step 3 — 使用文档

阅读获取的文档，编写准确的代码。不要依赖记忆中的 API 形状。

### Step 4 — 保存经验（可选但推荐）

完成任务后，如果发现了文档中没有的内容（坑点、变通方案、版本差异），保存下来：

```bash
chub annotate <id> "Webhook 验证需要原始请求体 — 不要在验证前解析"
```

注释是本地的，会在下次 `chub get` 时自动显示。

### Step 5 — 反馈（可选但推荐）

使用文档后，评价质量：

```bash
chub feedback <id> up --label accurate "示例清晰，模型名称正确"
chub feedback <id> down --label outdated "列出 gpt-4o 但 gpt-5 已发布"
```

可用标签：`outdated`、`inaccurate`、`incomplete`、`wrong-examples`、`wrong-version`、`poorly-structured`、`accurate`、`well-structured`、`helpful`、`good-examples`。

## 常用命令速查

| 目标 | 命令 |
|------|------|
| 列出所有文档 | `chub search` |
| 搜索文档 | `chub search "stripe"` |
| 获取详情 | `chub search stripe/api` |
| 获取 Python 文档 | `chub get stripe/api --lang py` |
| 获取 JS 文档 | `chub get openai/chat --lang js` |
| 保存到文件 | `chub get anthropic/sdk --lang py -o docs.md` |
| 获取多个文档 | `chub get openai/chat stripe/api --lang py` |
| 保存注释 | `chub annotate stripe/api "需要原始请求体"` |
| 列出注释 | `chub annotate --list` |
| 评分文档 | `chub feedback stripe/api up` |
| 更新缓存 | `chub update` |

## 高级用法

### 增量获取

当文档有多个参考文件时：

```bash
chub get acme/widgets --file references/advanced.md
chub get acme/widgets --file advanced.md,errors.md
chub get acme/widgets --full    # 获取全部
```

### JSON 输出（用于脚本处理）

```bash
chub search "stripe" --json
chub get stripe/api --json
chub annotate --list --json
```

### 缓存管理

```bash
chub cache status    # 查看缓存状态
chub cache clear     # 清除缓存
chub update          # 更新注册表
```

## 自我改进循环

```
没有 Context Hub                    有 Context Hub
───────────────                     ──────────────
搜索网页                            获取精选文档
噪音结果                            更高成功率
代码报错                            代理记录坑点
费力修复                            ↗ 下次更聪明
知识遗忘
↻ 下次重复
```

## 注意事项

1. **优先使用文档**：不要依赖训练记忆中的 API 形状，先 `chub get` 获取文档
2. **保存经验**：发现坑点或变通方案后，用 `chub annotate` 保存
3. **反馈质量**：用 `chub feedback` 评分，帮助维护者改进文档
4. **指定语言**：如果文档有多语言版本，务必指定 `--lang py` 或 `--lang js`

## 配置文件

配置位于 `~/.chub/config.yaml`：

```yaml
sources:
  - name: community
    url: https://cdn.aichub.org/v1

source: "official,maintainer,community"
refresh_interval: 86400
telemetry: true    # 匿名使用统计
feedback: true     # 允许发送反馈
```

---

*基于 https://github.com/andrewyng/context-hub 创建*
*版本: 1.0.0*