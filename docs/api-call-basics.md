# API 调用基础思路

> 把输入、输出、API调用三件事分开理解

---

## 核心概念

```
API 调用 = 三件独立的事

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   输入      │ ──→ │  API调用    │ ──→ │   输出      │
│ (你给什么)  │     │ (怎么调用)  │     │ (返回什么)  │
└─────────────┘     └─────────────┘     └─────────────┘

三个问题：
1. 我要给 API 什么？（输入）
2. 我怎么调用 API？（调用）
3. API 会给我什么？（输出）
```

---

## 第一件事：输入（你给 API 什么）

### 1.1 输入的本质

**输入 = 你想让 API 知道的信息**

```
API 不知道你的业务，你必须告诉它：
- 你要做什么
- 你有什么数据
- 你想要什么结果
```

### 1.2 输入的三种类型

| 类型 | 说明 | 例子 |
|------|------|------|
| **必填参数** | API 必须有才能工作 | 用户ID、搜索关键词 |
| **可选参数** | 可提供，不提供用默认值 | 分页大小、排序方式 |
| **上下文数据** | 帮助 API 理解你的意图 | 用户偏好、历史记录 |

### 1.3 输入的格式

**不同 API 要求不同格式：**

```
┌─────────────────────────────────────────────────────┐
│ 格式 1：URL 参数（Query Parameters）                 │
│                                                     │
│ GET /api/users?page=1&limit=10&sort=name           │
│                                                     │
│ 输入：                                              │
│ - page = 1（第几页）                                 │
│ - limit = 10（每页多少）                             │
│ - sort = name（按什么排序）                          │
│                                                     │
│ 特点：直接写在 URL 里，可见                          │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 格式 2：请求体（Body）                               │
│                                                     │
│ POST /api/users                                     │
│ Content-Type: application/json                      │
│                                                     │
│ {                                                   │
│   "name": "Alice",                                  │
│   "email": "alice@example.com",                     │
│   "age": 25                                         │
│ }                                                   │
│                                                     │
│ 输入：                                              │
│ - name = Alice                                      │
│ - email = alice@example.com                         │
│ - age = 25                                          │
│                                                     │
│ 特点：写在请求体里，不可见，适合大量数据               │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 格式 3：路径参数（Path Parameters）                  │
│                                                     │
│ GET /api/users/123                                  │
│                                                     │
│ 输入：                                              │
│ - 123 = 用户ID                                      │
│                                                     │
│ 特点：写在 URL 路径里，标识具体资源                   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 格式 4：请求头（Headers）                            │
│                                                     │
│ Authorization: Bearer token123                      │
│ Accept: application/json                            │
│                                                     │
│ 输入：                                              │
│ - token123 = 认证信息                               │
│ - application/json = 期望的响应格式                  │
│                                                     │
│ 特点：不在参数里，是元信息（认证、格式等）             │
└─────────────────────────────────────────────────────┘
```

### 1.4 输入准备流程

```
调用 API 前，问自己：

1. API 需要哪些必填参数？
   → 文档里会写 "required"

2. 我有哪些可选参数可以提供？
   → 文档里会写 "optional" 或有默认值

3. 参数用什么格式传递？
   → 看 API 文档的 "Content-Type" 或参数位置

4. 参数有什么限制？
   → 类型（字符串/数字）、长度、范围
```

### 1.5 输入常见错误

```
错误 1：缺少必填参数
→ API 返回 400 Bad Request

错误 2：参数类型错误
→ 给了字符串但 API 要数字
→ API 返回 400 Bad Request

错误 3：参数格式错误
→ JSON 格式不对（少了引号、逗号）
→ API 返回 400 Bad Request

错误 4：参数值超出范围
→ page = -1 或 limit = 10000
→ API 返回 400 或 422
```

---

## 第二件事：API 调用（怎么调用）

### 2.1 调用的本质

**调用 = 你和 API 建立连接、发送请求、等待响应**

```
调用过程：

你              API
 │               │
 │── 建立连接 ───→│
 │               │
 │── 发送输入 ───→│
 │               │
 │               │── 处理
 │               │
 │←── 返回输出 ───│
 │               │
关闭连接          │
```

### 2.2 调用的核心要素

| 要素 | 说明 | 例子 |
|------|------|------|
| **URL** | API 的地址 | https://api.example.com/users |
| **方法** | 你要做什么操作 | GET、POST、PUT、DELETE |
| **Headers** | 元信息 | Content-Type、Authorization |
| **Body** | 请求数据 | JSON 对象 |
| **Timeout** | 等多久 | 10秒、30秒 |

### 2.3 调用的基本步骤

```
步骤 1：准备输入
       → 收集参数、构建请求体

步骤 2：确定 URL 和方法
       → 看 API 文档

步骤 3：设置请求头
       → Content-Type、认证等

步骤 4：发送请求
       → 调用 API

步骤 5：等待响应
       → 在 timeout 内等待

步骤 6：处理结果
       → 成功：解析输出
       → 失败：处理错误
```

### 2.4 调用方式对比

**方式一：用工具/库（推荐）**

```python
import requests

# 调用 = 一行代码
response = requests.get("https://api.example.com/users", params={"page": 1})

# 工具帮你处理了：
# - 建立连接
# - 发送请求
# - 等待响应
# - 解析输出
```

**方式二：用 curl（测试用）**

```bash
# 调用 = 一个命令
curl -X GET "https://api.example.com/users?page=1"

# 适合快速测试，不适合程序里用
```

**方式三：用浏览器（简单测试）**

```
直接在浏览器地址栏输入：
https://api.example.com/users?page=1

只能测 GET 请求，适合快速验证
```

### 2.5 调用的注意事项

```
注意 1：超时设置
       → 必须设置 timeout，否则可能无限等待
       → requests.get(url, timeout=10)

注意 2：重试机制
       → 网络不稳定时可能需要重试
       → 但不要无限重试，设置最大次数

注意 3：并发限制
       → 不要同时发太多请求
       → API 有限流（rate limit）

注意 4：错误处理
       → 调用可能失败，必须处理
       → 网络错误、API 错误、解析错误
```

### 2.6 调用的完整示例

```python
import requests

# ==================== 准备输入 ====================
url = "https://api.example.com/users"
params = {"page": 1, "limit": 10}
headers = {"Authorization": "Bearer token123"}

# ==================== 发起调用 ====================
try:
    # 这里是"调用"本身
    response = requests.get(
        url,
        params=params,      # 输入：URL参数
        headers=headers,    # 输入：请求头
        timeout=10          # 调用设置：超时
    )
    
    # ==================== 处理调用结果 ====================
    if response.status_code == 200:
        # 成功：准备解析输出
        data = response.json()
    else:
        # 失败：处理错误
        print(f"API 返回错误: {response.status_code}")
        
except requests.exceptions.Timeout:
    # 调用失败：超时
    print("请求超时")
    
except requests.exceptions.ConnectionError:
    # 调用失败：连接失败
    print("无法连接到 API")
```

---

## 第三件事：输出（API 给你什么）

### 3.1 输出的本质

**输出 = API 处理后返回的结果**

```
API 处理你的输入后，返回：

- 状态码：告诉你成功还是失败
- 响应头：元信息（格式、时间等）
- 响应体：实际数据（你真正想要的）
```

### 3.2 输出的三个部分

```
┌─────────────────────────────────────────────────────┐
│ HTTP/1.1 200 OK                      ← 状态码       │
│ Content-Type: application/json       ← 响应头      │
│ Date: Tue, 31 Mar 2026 08:52:00 GMT                 │
│                                                     │
│ {                                    ← 响应体      │
│   "data": [                                         │
│     {"id": 1, "name": "Alice"},                     │
│     {"id": 2, "name": "Bob"}                        │
│   ],                                                │
│   "total": 100                                      │
│ }                                                   │
└─────────────────────────────────────────────────────┘
```

### 3.3 状态码（最重要）

**状态码告诉你调用是否成功**

```
2xx = 成功
├── 200 OK          → 成功，有数据返回
├── 201 Created     → 成功，创建了新资源
└── 204 No Content  → 成功，没有数据返回（如删除）

4xx = 你的问题（客户端错误）
├── 400 Bad Request    → 输入格式错误
├── 401 Unauthorized   → 没登录/Token无效
├── 403 Forbidden      → 没权限
├── 404 Not Found      → 资源不存在
├── 422 Unprocessable  → 输入验证失败
└── 429 Too Many       → 请求太多，被限流

5xx = API的问题（服务器错误）
├── 500 Internal Error → API 内部出错
├── 502 Bad Gateway    → 上游服务出错
├── 503 Unavailable    → API 暂时不可用
└── 504 Gateway Timeout → 上游服务超时
```

### 3.4 响应体（你真正想要的）

**响应体格式由 Content-Type 决定**

```
Content-Type: application/json
→ 响应体是 JSON 格式

{
  "data": [...],
  "total": 100,
  "page": 1
}

你需要解析：
data = response.json()
```

```
Content-Type: text/html
→ 响应体是 HTML 格式

<html>
  <body>...</body>
</html>

你需要：
html = response.text
```

```
Content-Type: application/octet-stream
→ 响应体是二进制数据（如图片、文件）

你需要：
content = response.content
# 保存到文件
with open("image.png", "wb") as f:
    f.write(content)
```

### 3.5 输出解析流程

```
收到响应后：

步骤 1：看状态码
       → 2xx：继续解析
       → 4xx/5xx：处理错误

步骤 2：确认格式
       → 看 Content-Type

步骤 3：解析响应体
       → JSON：response.json()
       → 文本：response.text
       → 二进制：response.content

步骤 4：提取你需要的字段
       → 按业务需求提取数据
```

### 3.6 输出解析示例

```python
import requests

response = requests.get("https://api.example.com/users/123")

# ==================== 步骤 1：看状态码 ====================
if response.status_code == 200:
    # 成功，继续
    
elif response.status_code == 404:
    # 用户不存在
    print("找不到这个用户")
    return None
    
elif response.status_code == 401:
    # 需要登录
    print("请先登录")
    return None
    
else:
    # 其他错误
    print(f"请求失败: {response.status_code}")
    return None

# ==================== 步骤 2：确认格式 ====================
content_type = response.headers.get("Content-Type")
# "application/json"

# ==================== 步骤 3：解析响应体 ====================
data = response.json()

# ==================== 步骤 4：提取字段 ====================
user_id = data["id"]        # 123
user_name = data["name"]    # "Alice"
user_email = data["email"]  # "alice@example.com"

print(f"用户: {user_name}, 邮箱: {user_email}")
```

### 3.7 输出的常见结构

**成功响应：**

```json
// 单个资源
{
  "id": 123,
  "name": "Alice",
  "email": "alice@example.com"
}

// 列表资源
{
  "data": [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
  ],
  "total": 100,
  "page": 1,
  "limit": 10
}

// 操作结果
{
  "success": true,
  "message": "用户创建成功",
  "id": 123
}
```

**错误响应：**

```json
// 简单错误
{
  "error": "用户不存在"
}

// 详细错误
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "用户ID 999 不存在"
  }
}

// 验证错误
{
  "error": "验证失败",
  "fields": {
    "email": ["格式不正确"],
    "age": ["必须是正整数"]
  }
}
```

---

## 三件事的关系图

```
┌─────────────────────────────────────────────────────────────────┐
│                        API 调用全景                              │
│                                                                 │
│   输入（你准备）          调用（你执行）          输出（API返回）  │
│   ────────────          ────────────          ────────────     │
│                                                                 │
│   ┌──────────┐          ┌──────────┐          ┌──────────┐     │
│   │ URL参数  │    ──→   │ 建立连接 │    ──→   │ 状态码   │     │
│   │ ?page=1  │          │          │          │ 200 OK   │     │
│   └──────────┘          └──────────┘          └──────────┘     │
│                                                                 │
│   ┌──────────┐          ┌──────────┐          ┌──────────┐     │
│   │ 请求体   │    ──→   │ 发送请求 │    ──→   │ 响应头   │     │
│   │ JSON数据 │          │          │          │ Content- │     │
│   └──────────┘          └──────────┘          │ Type     │     │
│                                                └──────────┘     │
│   ┌──────────┐          ┌──────────┐          ┌──────────┐     │
│   │ 请求头   │    ──→   │ 等待响应 │    ──→   │ 响应体   │     │
│   │ Auth     │          │ timeout  │          │ JSON数据 │     │
│   └──────────┘          └──────────┘          └──────────┘     │
│                                                                 │
│   你的职责：              你的职责：              API的职责：     │
│   - 准备参数              - 发起调用              - 处理输入     │
│   - 构建数据              - 设置超时              - 返回状态     │
│   - 设置认证              - 处理错误              - 返回数据     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 实战：完整调用流程

### 场景：获取用户列表

```python
import requests

# ==================== 第一件事：准备输入 ====================

# 输入 1：URL参数（Query Parameters）
params = {
    "page": 1,       # 第几页
    "limit": 20,     # 每页多少条
    "status": "active"  # 只看活跃用户
}

# 输入 2：请求头（Headers）
headers = {
    "Authorization": "Bearer your_token_here",  # 认证
    "Accept": "application/json"                # 期望返回JSON
}

# ==================== 第二件事：发起调用 ====================

url = "https://api.example.com/users"

try:
    # 调用本身
    response = requests.get(
        url,
        params=params,      # 传入输入（URL参数）
        headers=headers,    # 传入输入（请求头）
        timeout=10          # 调用设置
    )
    
    # ==================== 第三件事：处理输出 ====================
    
    # 输出 1：状态码
    if response.status_code != 200:
        # 失败：根据状态码处理
        if response.status_code == 401:
            print("需要登录")
        elif response.status_code == 429:
            print("请求太频繁，稍后再试")
        else:
            print(f"错误: {response.status_code}")
        return
    
    # 输出 2：响应头（可选，一般不需要）
    content_type = response.headers.get("Content-Type")
    print(f"返回格式: {content_type}")
    
    # 输出 3：响应体（重要）
    data = response.json()
    
    # 提取你需要的数据
    users = data["data"]           # 用户列表
    total = data["total"]          # 总数
    
    print(f"获取到 {len(users)} 个用户，总共 {total} 个")
    
    for user in users:
        print(f"  - {user['name']} ({user['email']})")
        
# ==================== 调用失败的错误处理 ====================

except requests.exceptions.Timeout:
    print("请求超时，API 响应太慢")

except requests.exceptions.ConnectionError:
    print("无法连接到 API，网络问题")

except requests.exceptions.RequestException as e:
    print(f"请求出错: {e}")

except ValueError:
    # JSON 解析失败
    print("返回的数据不是有效的 JSON")
```

---

## 三件事的独立思考法

### 调用 API 前，分开问三个问题

```
问题 1：输入
───────
- API 需要什么？
- 我有什么？
- 用什么格式传？
- 有什么限制？

问题 2：调用
───────
- 用什么方法？
- 发到哪个 URL？
- 设置什么超时？
- 怎么处理失败？

问题 3：输出
───────
- 成功返回什么？
- 失败返回什么？
- 数据什么格式？
- 我需要哪些字段？
```

### 调试时，分开检查三个环节

```
调试输入：
- 参数是否齐全？
- 格式是否正确？
- 值是否在范围内？

调试调用：
- URL 是否正确？
- 方法是否匹配？
- 网络是否通？
- 超时是否够？

调试输出：
- 状态码是什么？
- 响应体能解析吗？
- 字段存在吗？
```

---

## 快速参考卡

### 输入速查

| 类型 | 位置 | 用法 |
|------|------|------|
| URL参数 | URL中 | `?key=value&key2=value2` |
| 请求体 | Body | `json={...}` 或 `data={...}` |
| 路径参数 | URL路径 | `/users/123` |
| 请求头 | Headers | `headers={"Auth": "..."}` |

### 调用速查

```python
# GET（查）
requests.get(url, params={...}, headers={...}, timeout=10)

# POST（创）
requests.post(url, json={...}, headers={...}, timeout=10)

# PUT（改）
requests.put(url, json={...}, headers={...}, timeout=10)

# DELETE（删）
requests.delete(url, headers={...}, timeout=10)
```

### 输出速查

```python
# 状态码
response.status_code    # 200, 404, 500...

# 响应头
response.headers        # dict

# 响应体
response.json()         # JSON → dict
response.text           # 文本 → str
response.content        # 二进制 → bytes

# 快速判断成功
response.ok             # True if 2xx
response.raise_for_status()  # 非2xx抛异常
```

---

## 总结

```
API 调用 = 输入 + 调用 + 输出

输入：你准备，告诉 API 你要什么
调用：你执行，和 API 通信
输出：API 返回，告诉你结果

三者独立，分开思考，分开调试

准备输入 → 发起调用 → 处理输出
   ↓          ↓          ↓
 参数/数据   URL/方法    状态码/数据
```

---

*文档创建于 2026-03-31*
*重点：输入、输出、API调用三件事分开讲解*