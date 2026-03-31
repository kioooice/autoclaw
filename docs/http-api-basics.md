# HTTP 与 API 基础教程

> 理解 Request、Response、Status Code、JSON Body

---

## 目录

1. [HTTP 是什么](#1-http-是什么)
2. [Request 请求](#2-request-请求)
3. [Response 响应](#3-response-响应)
4. [Status Code 状态码](#4-status-code-状态码)
5. [JSON Body 请求/响应体](#5-json-body-请求响应体)
6. [实战：Python 发送请求](#6-实战python-发送请求)

---

## 1. HTTP 是什么

HTTP (HyperText Transfer Protocol) 是客户端与服务器之间的通信协议。

```
┌─────────────┐                    ┌─────────────┐
│   Client    │  ──── Request ───▶ │   Server    │
│  (浏览器/API)│                    │  (后端服务)  │
│             │  ◀─── Response ──── │             │
└─────────────┘                    └─────────────┘
```

**核心概念：**
- **请求 (Request)**：客户端发送给服务器的消息
- **响应 (Response)**：服务器返回给客户端的消息
- **无状态**：每个请求独立，服务器不记住之前的请求

---

## 2. Request 请求

### 2.1 请求结构

一个 HTTP 请求包含：

```
┌─────────────────────────────────────────────┐
│  请求行 (Request Line)                       │
│  GET /api/users HTTP/1.1                    │
├─────────────────────────────────────────────┤
│  请求头 (Headers)                            │
│  Host: api.example.com                      │
│  Content-Type: application/json             │
│  Authorization: Bearer xxx                  │
├─────────────────────────────────────────────┤
│  空行                                       │
├─────────────────────────────────────────────┤
│  请求体 (Body) - 可选                        │
│  {"name": "Alice", "age": 25}              │
└─────────────────────────────────────────────┘
```

### 2.2 请求方法 (HTTP Methods)

| 方法 | 用途 | 是否有 Body |
|------|------|-------------|
| **GET** | 获取资源 | ❌ 无 |
| **POST** | 创建资源 | ✅ 有 |
| **PUT** | 全量更新资源 | ✅ 有 |
| **PATCH** | 部分更新资源 | ✅ 有 |
| **DELETE** | 删除资源 | 可选 |

```python
# 常见场景示例

# GET - 获取用户列表
GET /api/users

# GET - 获取单个用户
GET /api/users/123

# POST - 创建新用户
POST /api/users
Body: {"name": "Alice", "email": "alice@example.com"}

# PUT - 更新用户全部信息
PUT /api/users/123
Body: {"name": "Alice", "email": "new@example.com", "age": 26}

# PATCH - 更新用户部分信息
PATCH /api/users/123
Body: {"email": "new@example.com"}

# DELETE - 删除用户
DELETE /api/users/123
```

### 2.3 常用请求头 (Headers)

```http
Content-Type: application/json          # 请求体格式
Authorization: Bearer eyJhbGc...        # 认证令牌
Accept: application/json                # 期望的响应格式
User-Agent: MyApp/1.0                   # 客户端标识
Cache-Control: no-cache                # 缓存控制
```

**Content-Type 常见值：**

| 值 | 说明 |
|----|------|
| `application/json` | JSON 格式（最常用） |
| `application/x-www-form-urlencoded` | 表单默认格式 |
| `multipart/form-data` | 文件上传 |
| `text/plain` | 纯文本 |
| `text/html` | HTML |

### 2.4 URL 结构

```
https://api.example.com:8080/users?page=1&limit=10#section
└─┬─┘ └──────┬──────┘└┬┘└──┬──┘└───────┬───────┘└───┬──┘
 协议      域名      端口  路径     查询参数      锚点
```

**查询参数 (Query Parameters)：**
```
GET /api/users?role=admin&status=active&page=1&limit=20

# 多个参数用 & 连接
# ?key1=value1&key2=value2&key3=value3
```

---

## 3. Response 响应

### 3.1 响应结构

```
┌─────────────────────────────────────────────┐
│  状态行 (Status Line)                       │
│  HTTP/1.1 200 OK                           │
├─────────────────────────────────────────────┤
│  响应头 (Headers)                           │
│  Content-Type: application/json            │
│  Content-Length: 123                       │
│  Date: Tue, 31 Mar 2026 06:25:00 GMT       │
├─────────────────────────────────────────────┤
│  空行                                       │
├─────────────────────────────────────────────┤
│  响应体 (Body)                              │
│  {"id": 123, "name": "Alice"}              │
└─────────────────────────────────────────────┘
```

### 3.2 常用响应头

```http
Content-Type: application/json          # 响应体格式
Content-Length: 1234                    # 响应体大小（字节）
Set-Cookie: session=abc123              # 设置 Cookie
Location: /users/123                     # 重定向地址
Cache-Control: max-age=3600             # 缓存时间
Access-Control-Allow-Origin: *          # CORS 跨域
```

---

## 4. Status Code 状态码

### 4.1 状态码分类

状态码是 3 位数字，第一位表示类别：

| 类别 | 范围 | 含义 |
|------|------|------|
| **1xx** | 100-199 | 信息响应（很少用） |
| **2xx** | 200-299 | ✅ 成功 |
| **3xx** | 300-399 | ➡️ 重定向 |
| **4xx** | 400-499 | ❌ 客户端错误 |
| **5xx** | 500-599 | ❌ 服务器错误 |

### 4.2 常见状态码详解

#### ✅ 2xx 成功

| 状态码 | 名称 | 说明 | 场景 |
|--------|------|------|------|
| **200** | OK | 请求成功 | GET/PUT/PATCH/DELETE 成功 |
| **201** | Created | 资源创建成功 | POST 创建成功 |
| **204** | No Content | 成功但无返回内容 | DELETE 成功 |

```json
// 200 OK 响应示例
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 123,
    "name": "Alice",
    "email": "alice@example.com"
}

// 201 Created 响应示例
HTTP/1.1 201 Created
Content-Type: application/json
Location: /users/123

{
    "id": 123,
    "name": "Alice",
    "created_at": "2026-03-31T06:25:00Z"
}

// 204 No Content 响应示例
HTTP/1.1 204 No Content
// 无响应体
```

#### ➡️ 3xx 重定向

| 状态码 | 名称 | 说明 |
|--------|------|------|
| **301** | Moved Permanently | 永久重定向 |
| **302** | Found | 临时重定向 |
| **304** | Not Modified | 资源未修改（缓存有效） |

#### ❌ 4xx 客户端错误

| 状态码 | 名称 | 说明 | 原因 |
|--------|------|------|------|
| **400** | Bad Request | 请求格式错误 | JSON 格式错误、缺少必填字段 |
| **401** | Unauthorized | 未认证 | 未登录、Token 过期 |
| **403** | Forbidden | 禁止访问 | 无权限访问该资源 |
| **404** | Not Found | 资源不存在 | URL 错误、资源已删除 |
| **405** | Method Not Allowed | 方法不允许 | 用 GET 访问只支持 POST 的接口 |
| **409** | Conflict | 冲突 | 用户名已存在、版本冲突 |
| **422** | Unprocessable Entity | 无法处理 | 验证失败、数据不合法 |
| **429** | Too Many Requests | 请求过多 | 触发限流 |

```json
// 400 Bad Request 响应示例
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
    "error": "Invalid JSON",
    "message": "Request body is not valid JSON"
}

// 401 Unauthorized 响应示例
HTTP/1.1 401 Unauthorized
Content-Type: application/json
WWW-Authenticate: Bearer

{
    "error": "Unauthorized",
    "message": "Token has expired"
}

// 404 Not Found 响应示例
HTTP/1.1 404 Not Found
Content-Type: application/json

{
    "error": "Not Found",
    "message": "User with id 999 not found"
}

// 422 Unprocessable Entity 响应示例
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/json

{
    "error": "Validation Failed",
    "errors": [
        {"field": "email", "message": "Invalid email format"},
        {"field": "age", "message": "Must be a positive integer"}
    ]
}
```

#### ❌ 5xx 服务器错误

| 状态码 | 名称 | 说明 | 原因 |
|--------|------|------|------|
| **500** | Internal Server Error | 服务器内部错误 | 代码 bug、异常未捕获 |
| **502** | Bad Gateway | 网关错误 | 上游服务不可用 |
| **503** | Service Unavailable | 服务不可用 | 服务维护、过载 |
| **504** | Gateway Timeout | 网关超时 | 上游服务响应超时 |

```json
// 500 Internal Server Error 响应示例
HTTP/1.1 500 Internal Server Error
Content-Type: application/json

{
    "error": "Internal Server Error",
    "message": "An unexpected error occurred"
}

// 503 Service Unavailable 响应示例
HTTP/1.1 503 Service Unavailable
Content-Type: application/json
Retry-After: 3600

{
    "error": "Service Unavailable",
    "message": "System is under maintenance"
}
```

### 4.3 状态码速查表

```
成功：200 ✅  201 ✅  204 ✅

客户端错误：
├── 你发错了：400 ❌（格式错）
├── 你没登录：401 🔐（要认证）
├── 你没权限：403 🚫（禁止访问）
├── 找不到：  404 ❓（资源不存在）
├── 方法错：  405 🚫（方法不允许）
├── 冲突了：  409 ⚠️（重复/冲突）
├── 验证失败：422 ⚠️（数据不合法）
└── 太频繁：  429 🐌（被限流）

服务器错误：
├── 服务器崩了：500 💥
├── 上游挂了：  502 💥
├── 维护中：    503 🔧
└── 超时了：    504 ⏰
```

---

## 5. JSON Body 请求/响应体

### 5.1 什么是 Body

Body 是请求或响应携带的数据，通常用 JSON 格式。

```
Request:
POST /api/users
Content-Type: application/json

{
    "name": "Alice",
    "email": "alice@example.com",
    "age": 25
}

Response:
HTTP/1.1 201 Created
Content-Type: application/json

{
    "id": 123,
    "name": "Alice",
    "email": "alice@example.com",
    "age": 25,
    "created_at": "2026-03-31T06:25:00Z"
}
```

### 5.2 请求体格式

**POST/PUT/PATCH 通常带 Body：**

```json
// 创建用户
POST /api/users
{
    "name": "Alice",
    "email": "alice@example.com"
}

// 登录
POST /api/auth/login
{
    "username": "alice",
    "password": "secret123"
}

// 搜索
POST /api/search
{
    "query": "python",
    "filters": {
        "category": "programming",
        "language": "en"
    },
    "page": 1,
    "limit": 20
}

// 批量操作
POST /api/users/batch
{
    "users": [
        {"name": "Alice", "email": "alice@example.com"},
        {"name": "Bob", "email": "bob@example.com"}
    ]
}
```

### 5.3 响应体格式

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
    "limit": 20
}

// 分页响应（标准格式）
{
    "items": [...],
    "pagination": {
        "total": 100,
        "page": 1,
        "per_page": 20,
        "total_pages": 5
    }
}
```

**错误响应：**

```json
// 简单错误
{
    "error": "User not found"
}

// 详细错误
{
    "error": {
        "code": "USER_NOT_FOUND",
        "message": "User with id 999 does not exist",
        "details": {
            "user_id": 999
        }
    }
}

// 验证错误（多字段）
{
    "error": "Validation Failed",
    "fields": {
        "email": ["Invalid email format"],
        "password": ["Must be at least 8 characters"],
        "age": ["Must be a positive integer"]
    }
}
```

### 5.4 Body vs Query Parameters

| 特性 | Query Parameters | Body |
|------|------------------|------|
| **位置** | URL 中 | 请求体内 |
| **可见性** | 可见（浏览器地址栏） | 不可见 |
| **大小限制** | URL 长度限制（~2KB-8KB） | 理论无限制 |
| **编码** | URL 编码 | 由 Content-Type 决定 |
| **适用场景** | GET、过滤、分页 | POST/PUT/PATCH、敏感数据 |

```
# Query Parameters - 用于过滤、分页
GET /api/users?role=admin&status=active&page=1&limit=20

# Body - 用于创建、更新、敏感数据
POST /api/users
{
    "name": "Alice",
    "password": "secret123"  # 密码绝不能放 URL！
}
```

---

## 6. 实战：Python 发送请求

### 6.1 使用 requests 库

```python
import requests

# 安装：pip install requests
```

### 6.2 GET 请求

```python
import requests

# 基础 GET
response = requests.get("https://api.example.com/users/123")
print(response.status_code)  # 200
print(response.json())       # 解析 JSON

# 带查询参数
params = {
    "role": "admin",
    "status": "active",
    "page": 1,
    "limit": 20
}
response = requests.get("https://api.example.com/users", params=params)

# 带请求头
headers = {
    "Authorization": "Bearer your_token_here",
    "Accept": "application/json"
}
response = requests.get("https://api.example.com/users", headers=headers)

# 完整示例
def get_user(user_id, token):
    url = f"https://api.example.com/users/{user_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print("用户不存在")
        return None
    elif response.status_code == 401:
        print("Token 无效或已过期")
        return None
    else:
        print(f"请求失败: {response.status_code}")
        return None
```

### 6.3 POST 请求

```python
import requests

# 基础 POST（JSON Body）
data = {
    "name": "Alice",
    "email": "alice@example.com",
    "age": 25
}
response = requests.post(
    "https://api.example.com/users",
    json=data  # 自动设置 Content-Type: application/json
)

# 手动设置 Content-Type
headers = {"Content-Type": "application/json"}
response = requests.post(
    "https://api.example.com/users",
    json=data,
    headers=headers
)

# 完整示例
def create_user(name, email, token):
    url = "https://api.example.com/users"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "name": name,
        "email": email
    }
    
    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 201:
        user = response.json()
        print(f"用户创建成功，ID: {user['id']}")
        return user
    elif response.status_code == 400:
        error = response.json()
        print(f"请求格式错误: {error}")
    elif response.status_code == 409:
        print("邮箱已被使用")
    elif response.status_code == 422:
        error = response.json()
        print(f"验证失败: {error}")
    else:
        print(f"创建失败: {response.status_code}")
    
    return None
```

### 6.4 PUT / PATCH / DELETE

```python
import requests

# PUT - 全量更新
def update_user_full(user_id, name, email, age, token):
    url = f"https://api.example.com/users/{user_id}"
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "name": name,
        "email": email,
        "age": age
    }
    response = requests.put(url, json=data, headers=headers)
    return response.status_code == 200

# PATCH - 部分更新
def update_user_partial(user_id, updates, token):
    url = f"https://api.example.com/users/{user_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.patch(url, json=updates, headers=headers)
    return response.status_code == 200

# 只更新邮箱
update_user_partial(123, {"email": "new@example.com"}, "your_token")

# DELETE - 删除
def delete_user(user_id, token):
    url = f"https://api.example.com/users/{user_id}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    
    if response.status_code == 204:
        print("删除成功")
        return True
    elif response.status_code == 404:
        print("用户不存在")
        return False
    return False
```

### 6.5 错误处理最佳实践

```python
import requests
from requests.exceptions import RequestException

def safe_request(method, url, **kwargs):
    """安全封装请求，处理各种异常"""
    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()  # 非 2xx 抛出异常
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        # HTTP 错误（4xx, 5xx）
        status = e.response.status_code
        
        if status == 400:
            print("请求格式错误")
        elif status == 401:
            print("未授权，请先登录")
        elif status == 403:
            print("无权限访问")
        elif status == 404:
            print("资源不存在")
        elif status == 429:
            print("请求太频繁，请稍后重试")
        elif 500 <= status < 600:
            print(f"服务器错误: {status}")
        else:
            print(f"HTTP 错误: {status}")
        
        # 尝试获取错误详情
        try:
            error_data = e.response.json()
            print(f"错误详情: {error_data}")
        except:
            pass
        return None
    
    except requests.exceptions.ConnectionError:
        print("网络连接失败")
        return None
    
    except requests.exceptions.Timeout:
        print("请求超时")
        return None
    
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None
    
    except ValueError:
        print("响应不是有效的 JSON")
        return None


# 使用示例
result = safe_request(
    "POST",
    "https://api.example.com/users",
    json={"name": "Alice", "email": "alice@example.com"},
    headers={"Authorization": "Bearer token"},
    timeout=10  # 10秒超时
)

if result:
    print(f"创建成功: {result}")
```

### 6.6 处理分页

```python
import requests

def get_all_users(token):
    """获取所有用户（处理分页）"""
    base_url = "https://api.example.com/users"
    headers = {"Authorization": f"Bearer {token}"}
    
    all_users = []
    page = 1
    
    while True:
        params = {"page": page, "limit": 50}
        response = requests.get(base_url, params=params, headers=headers)
        
        if response.status_code != 200:
            print(f"请求失败: {response.status_code}")
            break
        
        data = response.json()
        users = data.get("data", [])
        all_users.extend(users)
        
        # 检查是否还有下一页
        total_pages = data.get("pagination", {}).get("total_pages", 1)
        if page >= total_pages:
            break
        
        page += 1
    
    return all_users

# 使用
users = get_all_users("your_token")
print(f"共获取 {len(users)} 个用户")
```

### 6.7 文件上传

```python
import requests

def upload_file(file_path, token):
    """上传文件"""
    url = "https://api.example.com/upload"
    headers = {"Authorization": f"Bearer {token}"}
    
    # multipart/form-data 格式
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    return None

# 上传并指定文件名
def upload_with_name(file_path, token):
    url = "https://api.example.com/upload"
    headers = {"Authorization": f"Bearer {token}"}
    
    with open(file_path, "rb") as f:
        files = {"file": ("custom_name.pdf", f, "application/pdf")}
        response = requests.post(url, files=files, headers=headers)
    
    return response.json() if response.status_code == 200 else None
```

---

## 快速参考卡

### HTTP 方法速查

| 方法 | 用途 | Body | 幂等 |
|------|------|------|------|
| GET | 获取 | ❌ | ✅ |
| POST | 创建 | ✅ | ❌ |
| PUT | 全量更新 | ✅ | ✅ |
| PATCH | 部分更新 | ✅ | ❌ |
| DELETE | 删除 | 可选 | ✅ |

> **幂等**：多次相同请求，结果相同

### 状态码速查

```
2xx 成功
├── 200 OK              → 成功，有响应体
├── 201 Created         → 创建成功
└── 204 No Content      → 成功，无响应体

4xx 客户端错误
├── 400 Bad Request     → 格式错误
├── 401 Unauthorized    → 未认证
├── 403 Forbidden       → 无权限
├── 404 Not Found       → 不存在
├── 422 Unprocessable   → 验证失败
└── 429 Too Many        → 请求过多

5xx 服务器错误
├── 500 Internal Error  → 服务器 bug
├── 502 Bad Gateway     → 上游错误
├── 503 Unavailable     → 服务维护
└── 504 Gateway Timeout → 上游超时
```

### requests 速查

```python
import requests

# GET
r = requests.get(url, params={...}, headers={...})
data = r.json()

# POST
r = requests.post(url, json={...}, headers={...})

# PUT / PATCH / DELETE
r = requests.put(url, json={...})
r = requests.patch(url, json={...})
r = requests.delete(url)

# 状态码
r.status_code      # 200, 404, 500...
r.ok               # True if 2xx
r.raise_for_status()  # 非 2xx 抛异常

# 响应
r.json()           # 解析 JSON
r.text             # 原始文本
r.headers          # 响应头
```

---

## 练习建议

1. **工具练习**：使用 Postman 或 curl 发送各种请求
2. **状态码识别**：故意发送错误请求，观察不同状态码
3. **API 测试**：找公开 API（如 JSONPlaceholder、ReqRes）练习
4. **错误处理**：编写健壮的请求代码，处理所有异常情况
5. **分页处理**：实现一个自动翻页获取所有数据的函数

**推荐练习 API：**
- https://jsonplaceholder.typicode.com （免费假 API）
- https://reqres.in （免费测试 API）
- https://httpbin.org （HTTP 请求测试）

---

*文档创建于 2026-03-31*