# Claude Code v2.1.88 源码深度分析报告

**分析日期**：2026-03-31
**源码版本**：v2.1.88 (从 npm @anthropic-ai/claude-code 反编译)
**分析方法**：基于源码独立分析，不依赖已有报告

---

## 一、项目概况

### 1.1 基本信息

| 项目 | 数据 |
|------|------|
| 包名 | @anthropic-ai/claude-code |
| 版本 | 2.1.88 |
| 语言 | TypeScript (ES2022) |
| 源文件数 | 1,332 个 .ts 文件 |
| 最大单文件 | query.ts (约 785KB) |
| 运行时 | Bun 编译 → Node.js >= 18 bundle |
| 构建产物 | cli.js (~12MB 自包含 bundle) |

### 1.2 目录结构概览

```
src/
├── main.tsx              # 入口 bootstrap (并行初始化优化)
├── query.ts              # 主 Agent 循环 (核心引擎)
├── Tool.ts               # 工具接口定义
├── tools.ts              # 工具注册表
├── state/                # 全局状态管理
├── services/             # 业务逻辑层
│   ├── api/              # Claude API 客户端
│   ├── analytics/        # 遥测系统 (GrowthBook + 1P + Datadog)
│   ├── compact/          # 上下文压缩
│   ├── mcp/              # MCP 协议实现
│   └── tools/            # 工具执行引擎
├── tools/                # 40+ 工具实现
├── commands/             # ~80 斜杠命令
├── components/           # React/Ink 终端 UI
├── bridge/               # Claude Desktop/远程桥接
├── tasks/                # 任务系统实现
├── utils/                # 工具函数库
├── bootstrap/            # 启动状态管理
├── coordinator/          # 多 Agent 协调器 (feature-gated)
├── assistant/            # KAIROS 自助模式 (feature-gated)
└── proactive/            # 主动通知系统 (feature-gated)
```

---

## 二、核心架构分析

### 2.1 Agent 循环引擎 (query.ts)

**核心循环设计**：

```
while (true) {
  1. 构建系统提示 (fetchSystemPromptParts)
  2. 处理用户输入 (processUserInput)
  3. 规范化消息 (normalizeMessagesForAPI)
  4. 调用 Claude API (流式)
  5. 检查 stop_reason
     - "tool_use" → 执行工具 → append tool_result → loop
     - 其他 → yield 最终响应
}
```

**关键特性**：

1. **Thinking 规则**：thinking block 必须保留完整轨迹（assistant → tool_use → tool_result → next assistant）
2. **max_output_tokens 恢复**：流式错误不立即泄露给 SDK，等待恢复循环判断
3. **工具执行器**：`StreamingToolExecutor` 并行执行 concurrent-safe 工具
4. **上下文压缩**：自动触发 autoCompact 超过阈值时

### 2.2 Feature Flag 系统 (bun:bundle)

**编译时死代码消除 (DCE)**：

```typescript
// stubs/bun-bundle.ts
export function feature(_flag: string): boolean {
  return false  // 发布版本中，所有 feature() 返回 false
}
```

**关键 insight**：Bun 的 `feature()` 是编译时 intrinsic，不是运行时函数。

- Anthropic 内部构建：`feature('DAEMON')` = true → 代码保留
- npm 发布版本：`feature('DAEMON')` = false → 代码被删除

**缺失模块原因**：108 个模块在发布版本中被 DCE 删除，无法从 bundle 恢复。

---

## 三、工具系统架构

### 3.1 工具接口定义 (Tool.ts)

每个工具实现：

```typescript
interface Tool<Input, Output, Progress> {
  // 生命周期
  validateInput(): ValidationResult
  checkPermissions(): PermissionResult
  call(): Promise<Output>
  
  // 能力标识
  isEnabled(): boolean        // feature gate
  isConcurrencySafe(): boolean // 可并行执行
  isReadOnly(): boolean       // 无副作用
  isDestructive(): boolean    // 不可逆操作
  
  // 渲染 (React/Ink)
  renderToolUseMessage()
  renderToolResultMessage()
  renderToolUseProgressMessage()
  
  // AI 接口
  prompt(): string            // LLM 描述
  description(): string       // 动态描述
  inputSchema: ZodSchema      // 输入验证
}
```

### 3.2 工具注册 (tools.ts)

**内置工具 (~40+)**：

| 类别 | 工具 |
|------|------|
| 文件操作 | FileRead, FileEdit, FileWrite, NotebookEdit |
| 搜索 | Glob, Grep, ToolSearch |
| 执行 | Bash, PowerShell |
| Web | WebFetch, WebSearch |
| MCP | MCPTool, ListMcpResources, ReadMcpResource |
| Agent | AgentTool, TeamCreate, TeamDelete, SendMessage |
| 任务 | TaskCreate/Get/List/Update/Stop/Output |
| 规划 | EnterPlanMode, ExitPlanMode, TodoWrite |
| 其他 | AskUserQuestion, Brief, Config, Skill, LSP |

**Feature-gated 工具**（发布版本中缺失）：

```typescript
// 条件导入示例
const REPLTool = process.env.USER_TYPE === 'ant'
  ? require('./tools/REPLTool/REPLTool.js').REPLTool
  : null

const SleepTool = feature('PROACTIVE') || feature('KAIROS')
  ? require('./tools/SleepTool/SleepTool.js').SleepTool
  : null

const cronTools = feature('AGENT_TRIGGERS')
  ? [CronCreateTool, CronDeleteTool, CronListTool]
  : []
```

### 3.3 StreamingToolExecutor (并行执行)

**并发控制策略**：

```typescript
class StreamingToolExecutor {
  // 工具状态: 'queued' | 'executing' | 'completed' | 'yielded'
  
  canExecuteTool(isConcurrencySafe: boolean): boolean {
    const executing = this.tools.filter(t => t.status === 'executing')
    return executing.length === 0 
      || (isConcurrencySafe && executing.every(t => t.isConcurrencySafe))
  }
  
  // 并发安全工具可并行，非安全工具独占执行
}
```

---

## 四、权限系统分析

### 4.1 权限流程

```
Tool Call Request
     ↓
validateInput() → 拒绝无效输入
     ↓
PreToolUse Hooks → 用户定义 shell hooks (settings.json)
     ↓
Permission Rules → alwaysAllow/alwaysDeny/alwaysAsk 规则
     ↓
Interactive Prompt → 无匹配规则时询问用户
     ↓
checkPermissions() → 工具特定逻辑 (路径沙箱等)
     ↓
APPROVED → tool.call()
```

### 4.2 Permission Context 结构

```typescript
type ToolPermissionContext = {
  mode: PermissionMode                     // default/plan/bypass
  additionalWorkingDirectories: Map<...>
  alwaysAllowRules: ToolPermissionRulesBySource  // 自动批准
  alwaysDenyRules: ToolPermissionRulesBySource   // 自动拒绝
  alwaysAskRules: ToolPermissionRulesBySource    // 必须询问
  isBypassPermissionsModeAvailable: boolean
  isAutoModeAvailable?: boolean
  strippedDangerousRules?: ...             // MDM 剥离的危险规则
  shouldAvoidPermissionPrompts?: boolean   // 后台 Agent
  awaitAutomatedChecksBeforeDialog?: boolean  // 协调器 worker
}
```

### 4.3 Bash 安全检查

**文件大小**：bashSecurity.ts (102KB), bashPermissions.ts (98KB)

**检查维度**：
- 命令语义分析 (destructive, readonly, network)
- 路径验证 (沙箱边界)
- 危险模式检测 (rm -rf, sudo, etc.)
- 只读验证 (readOnlyValidation.ts, 68KB)

---

## 五、遥测系统分析

### 5.1 Analytics Sink 架构

```typescript
// services/analytics/index.ts

type AnalyticsSink = {
  logEvent: (eventName: string, metadata: LogEventMetadata) => void
  logEventAsync: (eventName, metadata) => Promise<void>
}

// 事件先入队列，sink attach 后异步 drain
const eventQueue: QueuedEvent[] = []
let sink: AnalyticsSink | null = null

// 阻止敏感数据泄露的类型标记
type AnalyticsMetadata_I_VERIFIED_THIS_IS_NOT_CODE_OR_FILEPATHS = never
type AnalyticsMetadata_I_VERIFIED_THIS_IS_PII_TAGGED = never
```

**双 Sink 架构**：
1. **1P Sink** → Anthropic 内部 BigQuery (PII 可见)
2. **Datadog Sink** → 公共后端 (PII 被 stripProtoFields 过滤)

### 5.2 GrowthBook Feature Flags

```typescript
// services/analytics/growthbook.ts

type GrowthBookUserAttributes = {
  id: string
  sessionId: string
  deviceID: string
  platform: 'win32' | 'darwin' | 'linux'
  apiBaseUrlHost?: string
  organizationUUID?: string
  accountUUID?: string
  userType?: string
  subscriptionType?: string
  rateLimitTier?: string
  firstTokenTime?: number
  email?: string
  appVersion?: string
}

// 远程 eval + 本地缓存
const remoteEvalFeatureValues = new Map<string, unknown>()
const experimentDataByFeature = new Map<string, StoredExperimentData>()
```

**关键发现**：GrowthBook 可以在运行时改变任何用户的行为，无需用户同意。

---

## 六、上下文压缩系统

### 6.1 三层压缩策略

```typescript
// services/compact/

1. autoCompact.ts     → 超阈值时自动触发，调用 API 生成摘要
2. snipCompact.ts     → 删除僵尸消息和过期标记 (HISTORY_SNIP feature)
3. contextCollapse.ts → 重构上下文结构 (CONTEXT_COLLAPSE feature)
```

### 6.2 Auto Compact 逻辑

```typescript
// 触发阈值计算
function getAutoCompactThreshold(model: string): number {
  const effectiveContextWindow = getEffectiveContextWindowSize(model)
  return effectiveContextWindow - AUTOCOMPACT_BUFFER_TOKENS  // ~13k buffer
}

// 连续失败熔断 (防止无限重试)
const MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3
```

**压缩后消息结构**：

```
messages[] =
  [compact_summary] + [compact_boundary marker] + [recent messages full]
```

---

## 七、MCP 协议集成

### 7.1 传输层支持

```typescript
// services/mcp/client.ts

支持的传输:
- stdio    → spawn child process
- sse      → HTTP EventSource
- http     → Streamable HTTP
- ws       → WebSocket
- sdk      → in-process transport
```

### 7.2 认证机制

- OAuth 2.0 flow (McpOAuthConfig)
- Cross-App Access (XAA / SEP-990)
- API key via headers

### 7.3 工具命名约定

```
mcp__<server>__<tool>  // MCP 工具在 Claude Code 中的命名
```

---

## 八、多 Agent 系统

### 8.1 Agent Tool 设计

```typescript
// tools/AgentTool/AgentTool.tsx

输入 Schema:
{
  description: string       // 3-5 词任务描述
  prompt: string           // 任务内容
  subagent_type?: string   // 专用 agent 类型
  model?: 'sonnet' | 'opus' | 'haiku'
  run_in_background?: boolean
  
  // 多 Agent 参数
  name?: string            // 可寻址名称
  team_name?: string       // 团队名
  mode?: PermissionMode    // 权限模式
  
  // 隔离模式
  isolation?: 'worktree' | 'remote'  // git worktree 或远程 CCR
  cwd?: string             // 工作目录覆盖
}
```

### 8.2 子 Agent 模式

| 模式 | 描述 |
|------|------|
| default | 同进程，共享对话 |
| fork | 子进程，新 messages[]，共享文件缓存 |
| worktree | 隔离 git worktree + fork |
| remote | 桥接到 Claude Code Remote / container |

### 8.3 后台任务自动触发

```typescript
// 超过 120s 自动转为后台
function getAutoBackgroundMs(): number {
  if (isEnvTruthy(process.env.CLAUDE_AUTO_BACKGROUND_TASKS) 
      || getFeatureValue_CACHED_MAY_BE_STALE('tengu_auto_background_agents', false)) {
    return 120_000
  }
  return 0
}
```

---

## 九、状态管理

### 9.1 AppState 结构

```typescript
type AppState = {
  settings: SettingsJson
  verbose: boolean
  mainLoopModel: ModelSetting
  toolPermissionContext: ToolPermissionContext
  
  // Bridge 状态
  replBridgeEnabled: boolean      // 配置驱动
  replBridgeExplicit: boolean     // 命令驱动
  replBridgeConnected: boolean    // 注册完成
  replBridgeSessionActive: boolean // WebSocket 活跃
  
  // 远程状态
  remoteConnectionStatus: 'connecting' | 'connected' | 'reconnecting' | 'disconnected'
  remoteBackgroundTaskCount: number
  
  // 视图状态
  expandedView: 'none' | 'tasks' | 'teammates'
  coordinatorTaskIndex: number
  footerSelection: FooterItem | null
  
  // Agent 状态
  agent: string | undefined       // CLI --agent 参数
  kairosEnabled: boolean          // 助手模式
  
  // 推测执行
  speculation: SpeculationState
}
```

### 9.2 React 集成

```typescript
// state/AppState.tsx

AppStateProvider → createContext
useAppState(sel) → selector-based subscriptions
useSetAppState() → immer-style updater
```

---

## 十、启动优化分析

### 10.1 并行初始化

```typescript
// main.tsx 入口

// 1. MDM subprocess 并行启动 (plutil/reg query)
startMdmRawRead()

// 2. Keychain 预取并行 (OAuth + API key)
startKeychainPrefetch()

// 3. 其他模块加载 (~135ms)
// MDM 和 Keychain 在后台运行，不阻塞主流程
```

### 10.2 懒加载策略

```typescript
// 循环依赖打破
const getTeammateUtils = () => require('./utils/teammate.js')
const getTeammatePromptAddendum = () => require('./utils/swarm/teammatePromptAddendum.js')

// Feature-gated 模块
const coordinatorModeModule = feature('COORDINATOR_MODE') 
  ? require('./coordinator/coordinatorMode.js') 
  : null
```

---

## 十一、关键设计模式

| 模式 | 位置 | 用途 |
|------|------|------|
| AsyncGenerator streaming | QueryEngine, query() | API 到消费端全链路流式 |
| Builder + Factory | buildTool() | 工具定义安全默认值 |
| Branded Types | SystemPrompt, asSystemPrompt() | 防止 string/array 混淆 |
| Feature Flags + DCE | feature() from bun:bundle | 编译时死代码消除 |
| Discriminated Unions | Message types | 类型安全消息处理 |
| Observer + State Machine | StreamingToolExecutor | 工具执行生命周期 |
| Snapshot State | FileHistoryState | 文件操作 undo/redo |
| Ring Buffer | Error log | 长会话内存限制 |
| Fire-and-Forget Write | recordTranscript() | 非阻塞持久化 |
| Lazy Schema | lazySchema() | 延迟 Zod schema 评估 |
| AsyncLocalStorage | agent context | 共享进程中的 Agent 上下文隔离 |

---

## 十二、与 OpenClaw 的对比

| 维度 | Claude Code | OpenClaw |
|------|-------------|----------|
| 运行时 | Bun → Node bundle | Node.js 直接运行 |
| UI | React/Ink 终端 | 多渠道 (Telegram, Discord, Web, etc.) |
| 工具数 | 40+ 内置 | 可扩展 Skills 系统 |
| Feature Flags | Bun compile-time | 配置驱动运行时 |
| 遥测 | 双 Sink (1P + Datadog) | 可选 |
| 多 Agent | fork/worktree/remote | subagent + ACP harness |
| MCP | 完整实现 | 通过 mcporter 转发 |
| 远程控制 | GrowthBook + managed settings | Gateway 配置 |

---

## 十三、技术亮点

### 13.1 编译时 DCE 的巧妙使用

通过 Bun 的 `feature()` intrinsic，Anthropic 可以：
- 内部使用完整功能 (daemon, proactive, KAIROS)
- 发布版本自动删除这些代码
- 无法从 bundle 逆向恢复删除的模块

### 13.2 并行初始化优化

- MDM subprocess 与模块加载并行 (~65ms 节省)
- Keychain 预取避免串行读取
- 启动 profiler 追踪每个阶段

### 13.3 推测执行

```typescript
type SpeculationState = 
  | { status: 'idle' }
  | { status: 'active', id, abort, messagesRef, boundary, ... }

// 在用户输入时提前执行，节省时间
```

### 13.4 上下文预算管理

```typescript
// token budget + 500k auto-continue
getCurrentTurnTokenBudget()
getTurnOutputTokens()
checkTokenBudget()

// API task_budget (beta task-budgets-2026-03-13)
taskBudget?: { total: number }
```

---

## 十四、潜在风险点

### 14.1 遥测不可退出

- 1P logging 无 UI 退出选项
- `OTEL_LOG_TOOL_DETAILS=1` 可捕获完整工具输入
- 环境指纹 + 进程指标 + repo hash 每次事件发送

### 14.2 远程控制

- GrowthBook 可无同意改变用户行为
- managed settings 显示阻塞对话框，拒绝 = app 退出
- 6+ killswitches (bypass permissions, fast mode, voice mode)

### 14.3 Undercover Mode

- Anthropic 员工在公共仓库自动进入
- 模型指令："Do not blow your cover"
- 无强制关闭选项

---

## 十五、总结

Claude Code 是一个**生产级 AI Agent 框架**，展示了从基本循环到复杂系统的 12 层渐进式构建：

1. **基础循环** → while-true API 调用
2. **工具分发** → 注册表 + 工厂模式
3. **规划模式** → TodoWrite + Plan Mode
4. **子 Agent** → fork + worktree 隔离
5. **知识注入** → SkillTool + CLAUDE.md
6. **上下文压缩** → 三层策略
7. **持久任务** → 任务系统
8. **后台任务** → DreamTask + daemon
9. **Agent 团队** → TeamCreate/Delete
10. **团队协议** → SendMessage
11. **自主 Agent** → coordinator auto-claim
12. **Worktree 隔离** → 目录级隔离

**核心价值**：这份源码是学习生产级 AI Agent 架构的绝佳教材，展示了如何在基本 Agent 循环上层层叠加：权限、流式、并发、压缩、子 Agent、持久化、MCP 等机制。

---

*分析完成，保存于 workspace/github-trending/claude-code-source-analysis-2026-03-31.md*