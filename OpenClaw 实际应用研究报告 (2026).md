# OpenClaw 实际应用研究报告

**研究日期**：2026年3月27日  
**数据来源**：GitHub、官方文档、社区Showcase、ClawHub 技能市场

---

## 摘要

OpenClaw 是一款**开源、自托管**的个人 AI 助手网关，由 Peter Steinberger 发起，社区驱动开发。其核心理念是"**Any OS. Any Platform. The lobster way.**"——在任何操作系统、任何平台上运行，以"龙虾的方式"（暗指外骨骼保护、自给自足）构建个人 AI 助手。

截至 2026 年 3 月，OpenClaw 已支持 **20+ 消息渠道**、**35+ 模型提供商**、**多代理编排**、**语音交互**、**浏览器自动化**等核心能力，并在社区涌现出大量创新应用案例。

---

## 一、项目概览

### 1.1 基本信息

| 项目属性 | 详情 |
|---------|------|
| **开源协议** | MIT License |
| **主要语言** | TypeScript |
| **运行时** | Node.js 24 (推荐) / Node.js 22.16+ |
| **GitHub 仓库** | github.com/openclaw/openclaw |
| **官方网站** | openclaw.ai |
| **文档站点** | docs.openclaw.ai |
| **技能市场** | clawhub.com |
| **社区** | Discord: discord.gg/clawd |
| **创建者** | Peter Steinberger (@steipete) |

### 1.2 发展历程

OpenClaw 经历了多次迭代：
- **Warelay** → **Clawdbot** → **Moltbot** → **OpenClaw**

最初是个人学习和实验项目，目标是构建一个"**真正能做事**"的 AI 助手——能在真实计算机上执行真实任务。

### 1.3 核心理念

根据 `VISION.md`，OpenClaw 的设计哲学：

1. **自托管优先**：运行在用户自己的硬件上，用户的数据、用户的规则
2. **安全与能力平衡**：强大的默认安全策略，同时暴露清晰的控制点供高级用户使用
3. **终端优先**：安装过程透明，用户能看到文档、认证、权限和安全态势
4. **可扩展架构**：核心保持精简，可选能力通过插件分发

---

## 二、技术架构

### 2.1 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    消息渠道层 (Channels)                      │
│  WhatsApp | Telegram | Discord | Slack | Signal | iMessage  │
│  Feishu | LINE | Matrix | Teams | WeChat | IRC | WebChat   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     Gateway (网关)                           │
│                  ws://127.0.0.1:18789                        │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐  │
│  │ 会话管理    │ 路由分发    │ 安全认证    │ 事件广播    │  │
│  └─────────────┴─────────────┴─────────────┴─────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│   Pi Agent    │  │   CLI 工具    │  │  WebChat UI   │
│  (AI 运行时)   │  │ openclaw ...  │  │  浏览器界面   │
└───────────────┘  └───────────────┘  └───────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                     Nodes (设备节点)                          │
│  macOS | iOS | Android | Linux | Windows (WSL2)            │
│  能力: Canvas | Camera | Screen | Voice | Location          │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 核心组件

| 组件 | 功能 |
|------|------|
| **Gateway** | 单一控制平面，管理消息连接、会话、工具和事件 |
| **Pi Agent** | 嵌入式 AI 运行时，支持工具流式传输 |
| **Nodes** | 设备节点，暴露摄像头、屏幕、位置等设备能力 |
| **Canvas** | 代理驱动的可视化工作空间 (A2UI) |
| **Skills** | 可插拔的技能系统，支持 ClawHub 分发 |

### 2.3 通信协议

- **传输层**：WebSocket，JSON 文本帧
- **认证**：设备配对 + 令牌验证
- **幂等性**：副作用方法需要幂等键
- **安全性**：本地连接可自动批准，远程连接需显式授权

### 2.4 支持的渠道

| 类型 | 渠道 | 技术栈 |
|------|------|--------|
| 即时通讯 | WhatsApp | Baileys |
| 即时通讯 | Telegram | grammY |
| 即时通讯 | Discord | discord.js |
| 即时通讯 | Slack | Bolt |
| 即时通讯 | Signal | signal-cli |
| 即时通讯 | iMessage (BlueBubbles) | BlueBubbles API |
| 企业通讯 | Microsoft Teams | Bot Framework |
| 企业通讯 | Google Chat | Chat API |
| 企业通讯 | Feishu (飞书) | 官方 API |
| 企业通讯 | Mattermost | 插件 |
| 其他 | WeChat | @tencent-weixin/openclaw-weixin |
| 其他 | Matrix, LINE, IRC, Nostr, Twitch, Zalo | 官方/社区插件 |

### 2.5 支持的模型提供商

**官方支持 35+ 模型提供商**：

| 类别 | 提供商 |
|------|--------|
| 主流厂商 | OpenAI, Anthropic, Google, AWS Bedrock |
| 订阅认证 | OpenAI (OAuth), ChatGPT Plus |
| 开源部署 | vLLM, SGLang, Ollama |
| 云服务商 | Azure OpenAI, GCP Vertex AI, AWS Bedrock |
| 国内厂商 | 阿里百炼、智谱 GLM、月之暗面 Kimi、DeepSeek |

---

## 三、核心能力

### 3.1 多渠道消息收发

- **统一 Gateway**：单一进程服务所有消息渠道
- **群组支持**：基于 @提及 的激活规则
- **私聊安全**：白名单 + 配对码验证
- **媒体支持**：图片、音频、视频、文档双向传输

### 3.2 多代理路由

- **会话隔离**：每个发送者/工作区独立会话
- **会话模型**：私话合并为 `main` 会话，群聊独立隔离
- **代理编排**：支持子代理生成、会话间通信

### 3.3 设备节点能力

| 平台 | 能力 |
|------|------|
| **macOS** | Canvas、摄像头、屏幕录制、语音唤醒、Talk Mode、系统命令 |
| **iOS** | Canvas、摄像头、屏幕录制、语音唤醒、位置、设备配对 |
| **Android** | Canvas、摄像头、屏幕录制、语音、位置、通知、短信、联系人、日历 |
| **Windows (WSL2)** | Linux 子系统支持 |
| **Linux** | Docker 容器部署 |

### 3.4 浏览器自动化

- **独立浏览器**：OpenClaw 管理的 Chrome/Chromium
- **快照 + 操作**：页面截图、元素操作、文件上传
- **配置文件**：支持 Chrome 扩展中继

### 3.5 自动化与调度

- **Cron 任务**：定时执行脚本和代理任务
- **Webhook**：外部事件触发
- **心跳机制**：周期性检查邮件、日历、通知
- **Gmail Pub/Sub**：实时邮件推送

### 3.6 技能系统

- **ClawHub 技能市场**：版本化技能分发，支持回滚
- **安装命令**：`npx clawhub@latest install <skill-name>`
- **技能类型**： bundled (内置)、managed (管理)、workspace (工作区)

---

## 四、实际应用案例分析

### 4.1 开发与编程

| 案例 | 用户 | 描述 |
|------|------|------|
| **PR Review → Telegram** | @bangnokia | OpenCode 完成代码变更 → 打开 PR → OpenClaw 审查差异并在 Telegram 反馈评审意见 |
| **iOS App via Telegram** | @coard | 完全通过 Telegram 聊天构建 iOS 应用（地图+录音），部署到 TestFlight |
| **Linear CLI** | @NessZerra | Linear 项目管理 CLI，与 Claude Code / OpenClaw 集成 |
| **Beeper CLI** | @jules | 通过 Beeper 本地 MCP API 管理所有聊天 (iMessage, WhatsApp 等) |
| **CodexMonitor** | @odrobnik | Homebrew 安装的 OpenAI Codex 会话监控工具 |

### 4.2 自动化工作流

| 案例 | 用户 | 描述 |
|------|------|------|
| **Tesco Shop Autopilot** | @marchattonhere | 每周饮食计划 → 常购商品 → 预订配送时段 → 确认订单。无需 API，纯浏览器控制 |
| **Wine Cellar Skill** | @prades_maxime | 让 OpenClaw 构建本地酒窖技能，962 瓶酒的 CSV 管理 |
| **Padel Court Booking** | @joshp123 | Playtomic 球场可用性检查 + 预订 CLI |
| **ParentPay School Meals** | @George5562 | 英国学校餐预订自动化 |
| **Accounting Intake** | Community | 从邮件收集 PDF，为税务顾问准备文档 |

### 4.3 智能家居与物联网

| 案例 | 用户 | 描述 |
|------|------|------|
| **Home Assistant Add-on** | @ngutman | 在 Home Assistant OS 上运行 OpenClaw Gateway |
| **GoHome Automation** | @joshp123 | Nix 原生家庭自动化，Grafana 仪表盘 |
| **Roborock Vacuum** | @joshp123 | 自然语言控制扫地机器人 |
| **Winix Air Purifier** | @antonplex | 空气净化器智能控制 |
| **Bambu 3D Printer** | @tobiasbischoff | BambuLab 3D 打印机控制：状态、任务、摄像头、AMS、校准 |

### 4.4 语音与电话

| 案例 | 用户 | 描述 |
|------|------|------|
| **Clawdia Phone Bridge** | @alejandroOPI | Vapi 语音助手 ↔ OpenClaw HTTP 桥接，近实时电话通话 |
| **Telegram Voice Notes** | Community | papla.media TTS 包装，发送 Telegram 语音笔记 |
| **OpenRouter Transcription** | @obviyus | 多语言音频转录 |

### 4.5 知识与学习

| 案例 | 用户 | 描述 |
|------|------|------|
| **xuezh Chinese Learning** | @joshp123 | 中文学习引擎，发音反馈和学习流程 |
| **Karakeep Semantic Search** | @jamesbrooksco | 书签向量搜索，使用 Qdrant + OpenAI/Ollama 嵌入 |
| **WhatsApp Memory Vault** | Community | WhatsApp 导出数据摄入，转录 1000+ 语音笔记 |

### 4.6 健康与生活

| 案例 | 用户 | 描述 |
|------|------|------|
| **Oura Ring Health Assistant** | @AS | Oura 戒指数据 + 日历 + 预约 + 健身计划的个人健康助手 |
| **Vienna Transport** | @hjanuschka | 维也纳公共交通实时到站、中断、电梯状态、路线规划 |
| **Job Search Agent** | @attol8 | 职位搜索，匹配 CV 关键词，返回相关机会 |

### 4.7 多代理编排

| 案例 | 用户 | 描述 |
|------|------|------|
| **Kev's Dream Team** | @adam91holt | **14+ 代理**在单一 Gateway 下运行，Opus 4.5 编排器委派给 Codex workers。完整技术文档涵盖模型选择、沙箱、Webhook、心跳、委派流程 |

---

## 五、生态系统

### 5.1 ClawHub 技能市场

**网址**：clawhub.com (clawhub.ai)

**特点**：
- 版本化技能分发（类似 npm）
- 向量搜索技能
- 一键安装：`npx clawhub@latest install <skill-name>`
- 回滚支持

**热门技能示例**：
- `homeassistant` - Home Assistant 控制
- `caldav-calendar` - CalDAV 日历集成
- `openrouter-transcribe` - 多语言转录
- `r2-upload` - Cloudflare R2/S3 上传

### 5.2 社区贡献者

根据 GitHub 贡献者列表，OpenClaw 拥有 **150+ 贡献者**，包括：

- **核心团队**：Peter Steinberger (@steipete), Vincent Koc, Vignesh 等
- **社区活跃者**：@joshp123 (多技能贡献), @adam91holt (多代理架构), @kitze (Agents UI) 等

### 5.3 Discord 社区

- **频道**：discord.gg/clawd
- **活跃频道**：#showcase, #help, #general
- **社区规模**：数千成员（具体数据未公开）

---

## 六、安全设计

### 6.1 安全原则

根据官方安全文档：

1. **默认拒绝**：未知发送者收到配对码，代理不处理其消息
2. **显式授权**：公网 DM 需要显式 `dmPolicy="open"` + 白名单
3. **工具沙箱**：非主会话可配置 Docker 沙箱隔离
4. **令牌认证**：WebSocket 连接需要令牌验证
5. **设备配对**：新设备需配对批准

### 6.2 安全命令

```bash
# 安全检查
openclaw doctor

# 配对管理
openclaw pairing approve <sender>

# 白名单配置
channels.whatsapp.allowFrom: ["+15555550123"]
```

### 6.3 沙箱配置

```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "mode": "non-main"
      }
    }
  }
}
```

---

## 七、部署方式

### 7.1 本地安装 (推荐)

```bash
# 安装
npm install -g openclaw@latest

# 引导设置
openclaw onboard --install-daemon

# 启动 Gateway
openclaw gateway
```

### 7.2 Docker 部署

适合服务器部署，支持持久化和沙箱隔离。

### 7.3 Nix 部署

```bash
# 声明式配置
nix-openclaw
```

### 7.4 远程访问

| 方式 | 描述 |
|------|------|
| **Tailscale Serve** | Tailnet 内 HTTPS 访问 |
| **Tailscale Funnel** | 公网 HTTPS（需密码认证） |
| **SSH 隧道** | `ssh -L 18789:127.0.0.1:18789 user@host` |

---

## 八、与其他框架对比

### 8.1 对比表

| 特性 | OpenClaw | LangChain | AutoGPT | Cursor |
|------|----------|-----------|---------|--------|
| **自托管** | ✅ 完全 | ✅ 可选 | ✅ 可选 | ❌ 云端 |
| **消息渠道** | ✅ 20+ | ❌ 需集成 | ❌ 需集成 | ❌ 无 |
| **多代理编排** | ✅ 内置 | ✅ 框架级 | ✅ 核心 | ❌ 单一 |
| **设备节点** | ✅ iOS/Android/macOS | ❌ 无 | ❌ 无 | ❌ 无 |
| **技能市场** | ✅ ClawHub | ✅ LangChain Hub | ❌ 无 | ❌ 无 |
| **语音交互** | ✅ 原生 | ❌ 需集成 | ❌ 无 | ❌ 无 |
| **浏览器控制** | ✅ 内置 | ❌ 需集成 | ✅ 插件 | ❌ 无 |
| **开源** | ✅ MIT | ✅ Apache 2.0 | ✅ MIT | ❌ 闭源 |

### 8.2 独特优势

1. **消息渠道原生支持**：无需额外集成，开箱即用 20+ 渠道
2. **设备节点生态**：iOS/Android/macOS 原生应用，暴露设备能力
3. **Canvas 可视化**：代理驱动的 UI 渲染 (A2UI)
4. **语音原生**：语音唤醒 + 连续对话
5. **技能版本化**：ClawHub 提供 npm 式版本管理

---

## 九、应用场景总结

### 9.1 个人用户

| 场景 | 应用 |
|------|------|
| **日常助理** | 日程管理、邮件处理、信息检索 |
| **学习辅助** | 语言学习、知识管理、笔记整理 |
| **健康管理** | 健身计划、睡眠追踪、饮食建议 |
| **智能家居** | 设备控制、场景联动、能耗管理 |
| **购物自动化** | 自动比价、定期采购、订单跟踪 |

### 9.2 开发者

| 场景 | 应用 |
|------|------|
| **代码审查** | PR 自动审查、代码质量反馈 |
| **项目开发** | 端到端应用构建、测试、部署 |
| **文档生成** | 自动文档、API 文档、README |
| **CI/CD 集成** | 构建通知、部署确认、错误告警 |
| **多代理协作** | 任务分解、并行开发、结果整合 |

### 9.3 企业用户

| 场景 | 应用 |
|------|------|
| **客服自动化** | 多渠道客服、智能应答、工单创建 |
| **内部协作** | Slack/Teams 机器人、知识库问答 |
| **数据分析** | 报表生成、趋势分析、异常检测 |
| **流程自动化** | 审批流程、数据同步、定时任务 |

---

## 十、挑战与局限

### 10.1 技术挑战

1. **模型成本**：高级模型 (Claude Opus, GPT-5) 调用成本较高
2. **稳定性**：部分渠道（如 WhatsApp）依赖第三方库，可能不稳定
3. **配置复杂度**：多渠道、多代理配置学习曲线较陡

### 10.2 安全考量

1. **权限边界**：工具访问本地文件、网络，需谨慎配置
2. **数据隐私**：消息内容经过 AI 处理，敏感信息需脱敏
3. **远程访问**：公网暴露需强认证和加密

### 10.3 生态局限

1. **技能质量参差**：社区技能未经统一审核
2. **文档覆盖**：部分高级功能文档不够完善
3. **中文支持**：文档和社区以英文为主

---

## 十一、发展趋势

### 11.1 官方路线图

根据 `VISION.md`：

**当前优先级**：
- 安全和默认配置
- Bug 修复和稳定性
- 安装可靠性和首次运行体验

**下一步优先级**：
- 支持所有主要模型提供商
- 改进主要消息渠道支持
- 性能和测试基础设施
- 更好的计算机使用和代理能力
- CLI 和 Web 前端的人体工程学
- macOS、iOS、Android、Windows、Linux 伴侣应用

### 11.2 社区趋势

1. **多代理编排**：Dream Team 模式（14+ 代理）成为高级用户标配
2. **语音交互**：语音唤醒 + Talk Mode 日益普及
3. **浏览器自动化**：无需 API 的自动化流程增长
4. **垂直技能**：行业特定技能（医疗、法律、金融）涌现

### 11.3 技术演进

1. **Canvas/A2UI**：从文本交互转向可视化 UI
2. **MCP 集成**：通过 mcporter 支持模型上下文协议
3. **沙箱增强**：更细粒度的权限控制
4. **本地模型**：Ollama/vLLM 等本地部署支持增强

---

## 十二、结论

OpenClaw 代表了 **个人 AI 助手** 的一种新范式：

1. **真正自托管**：数据在用户手中，规则由用户定义
2. **无处不在**：通过 20+ 消息渠道，用户可从任何地方与助手交互
3. **能力扩展**：通过设备节点、浏览器自动化、技能系统，助手能执行真实任务
4. **生态开放**：MIT 协议、ClawHub 市场、社区驱动开发

对于追求**隐私控制**、**能力扩展**、**渠道统一**的用户，OpenClaw 提供了当前市场上有竞争力的解决方案。

### 适用人群

| 人群 | 适配度 | 原因 |
|------|--------|------|
| **开发者** | ⭐⭐⭐⭐⭐ | 完全控制、可扩展、命令行友好 |
| **技术爱好者** | ⭐⭐⭐⭐ | 学习曲线适中、社区活跃 |
| **隐私敏感用户** | ⭐⭐⭐⭐⭐ | 完全自托管、数据本地化 |
| **企业用户** | ⭐⭐⭐ | 需要一定技术能力部署维护 |
| **普通消费者** | ⭐⭐ | 配置复杂，建议等待更成熟的打包方案 |

---

## 参考资料

1. **官方资源**
   - GitHub: https://github.com/openclaw/openclaw
   - 文档: https://docs.openclaw.ai
   - 网站: https://openclaw.ai

2. **社区资源**
   - Discord: https://discord.gg/clawd
   - X/Twitter: https://x.com/openclaw
   - ClawHub: https://clawhub.com

3. **视频教程**
   - "OpenClaw: The self-hosted AI that Siri should have been (Full setup)" - VelvetShark
   - OpenClaw Showcase 视频

4. **社区 Showcase**
   - https://docs.openclaw.ai/start/showcase

---

*报告生成时间：2026年3月27日*  
*数据来源截止日期：2026年3月27日*