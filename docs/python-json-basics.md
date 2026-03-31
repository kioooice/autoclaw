# Python 与 JSON 基础教程

> 适合初学者的快速入门指南

---

## 目录

1. [Python 基础](#1-python-基础)
   - [变量](#11-变量)
   - [函数](#12-函数)
   - [列表](#13-列表)
   - [字典](#14-字典)
   - [循环](#15-循环)
2. [JSON 基础](#2-json-基础)
   - [对象](#21-对象)
   - [数组](#22-数组)
   - [字段读取](#23-字段读取)
3. [Python 操作 JSON](#3-python-操作-json)

---

## 1. Python 基础

### 1.1 变量

变量是存储数据的容器。Python 不需要声明类型，直接赋值即可。

```python
# 基本类型
name = "Alice"        # 字符串
age = 25              # 整数
height = 1.65         # 浮点数
is_student = True     # 布尔值

# 变量命名规则
# ✅ 推荐：小写字母 + 下划线
user_name = "Bob"
total_count = 100

# ❌ 避免：数字开头、特殊字符
# 1name = "xxx"       # 错误！
# user-name = "xxx"   # 错误！

# 多重赋值
a, b, c = 1, 2, 3
x = y = z = 0
```

**要点：**
- 变量名要有意义，便于理解
- Python 是动态类型，变量可以改变类型
- 使用 `type()` 查看变量类型

---

### 1.2 函数

函数是可重复使用的代码块。

```python
# 基本定义
def greet():
    print("Hello!")

greet()  # 调用函数

# 带参数的函数
def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Alice")

# 带返回值的函数
def add(a, b):
    return a + b

result = add(3, 5)  # result = 8

# 默认参数
def greet_with_message(name, message="Welcome"):
    print(f"{message}, {name}!")

greet_with_message("Bob")              # Welcome, Bob!
greet_with_message("Bob", "Hi")         # Hi, Bob!

# 关键字参数
def create_profile(name, age, city):
    return {"name": name, "age": age, "city": city}

profile = create_profile(age=25, name="Alice", city="Beijing")

# 可变参数 *args
def sum_all(*numbers):
    return sum(numbers)

print(sum_all(1, 2, 3, 4, 5))  # 15

# 关键字可变参数 **kwargs
def print_info(**info):
    for key, value in info.items():
        print(f"{key}: {value}")

print_info(name="Alice", age=25, city="Shanghai")
```

**要点：**
- `def` 关键字定义函数
- `return` 返回结果，没有 return 则返回 `None`
- 函数名要有描述性（动词+名词）

---

### 1.3 列表 (List)

列表是有序的可变集合，用 `[]` 表示。

```python
# 创建列表
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]  # 可以混合类型

# 访问元素（索引从 0 开始）
print(fruits[0])   # "apple"
print(fruits[-1])  # "cherry"（倒数第一个）
print(fruits[-2])  # "banana"（倒数第二个）

# 切片
nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(nums[2:5])   # [2, 3, 4]
print(nums[:3])    # [0, 1, 2]
print(nums[7:])    # [7, 8, 9]
print(nums[::2])   # [0, 2, 4, 6, 8]（步长为2）

# 修改列表
fruits[1] = "blueberry"
print(fruits)  # ["apple", "blueberry", "cherry"]

# 添加元素
fruits.append("orange")       # 末尾添加
fruits.insert(1, "mango")      # 指定位置插入
fruits.extend(["grape", "kiwi"])  # 扩展列表

# 删除元素
fruits.remove("apple")         # 按值删除
deleted = fruits.pop()         # 删除并返回最后一个
del fruits[0]                  # 按索引删除

# 常用操作
print(len(fruits))             # 长度
print("banana" in fruits)      # 是否存在
print(fruits.count("apple"))   # 出现次数
print(fruits.index("cherry"))  # 找索引

# 排序
nums = [3, 1, 4, 1, 5, 9, 2, 6]
nums.sort()                    # 原地排序
nums.sort(reverse=True)        # 降序
sorted_nums = sorted(nums)     # 返回新列表

# 列表推导式
squares = [x**2 for x in range(10)]
# [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

evens = [x for x in range(20) if x % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

**要点：**
- 列表有序、可变、允许重复
- 索引从 0 开始，支持负数索引
- 列表推导式是 Python 特色，简洁高效

---

### 1.4 字典 (Dict)

字典是键值对的无序集合，用 `{}` 表示。

```python
# 创建字典
person = {
    "name": "Alice",
    "age": 25,
    "city": "Beijing"
}

# 访问值
print(person["name"])       # "Alice"
print(person.get("age"))    # 25
print(person.get("job", "N/A"))  # 不存在时返回默认值

# 修改/添加
person["age"] = 26          # 修改
person["job"] = "Engineer"  # 添加新键

# 删除
del person["city"]
job = person.pop("job")      # 删除并返回值

# 遍历字典
for key in person:
    print(key)               # 只遍历键

for key, value in person.items():
    print(f"{key}: {value}") # 遍历键值对

for value in person.values():
    print(value)             # 只遍历值

# 嵌套字典
users = {
    "user1": {"name": "Alice", "age": 25},
    "user2": {"name": "Bob", "age": 30}
}
print(users["user1"]["name"])  # "Alice"

# 字典推导式
squares = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 合并字典 (Python 3.9+)
defaults = {"theme": "dark", "lang": "en"}
settings = {"lang": "zh", "font": "Arial"}
merged = defaults | settings  # settings 覆盖 defaults
# {"theme": "dark", "lang": "zh", "font": "Arial"}
```

**要点：**
- 字典键必须不可变（字符串、数字、元组）
- 键唯一，值可重复
- 访问不存在的键会报错，用 `get()` 更安全

---

### 1.5 循环

#### for 循环

```python
# 遍历列表
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# 遍历范围
for i in range(5):        # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 10, 2): # 1, 3, 5, 7, 9（步长为2）
    print(i)

# 遍历字典
person = {"name": "Alice", "age": 25}
for key, value in person.items():
    print(f"{key}: {value}")

# enumerate：同时获取索引和值
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# zip：同时遍历多个列表
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 35]
for name, age in zip(names, ages):
    print(f"{name} is {age} years old")
```

#### while 循环

```python
# 基本语法
count = 0
while count < 5:
    print(count)
    count += 1

# 带条件判断
while True:
    user_input = input("输入 'quit' 退出: ")
    if user_input == "quit":
        break
    print(f"你输入了: {user_input}")
```

#### 循环控制

```python
# break：跳出整个循环
for i in range(10):
    if i == 5:
        break
    print(i)  # 0, 1, 2, 3, 4

# continue：跳过本次迭代
for i in range(10):
    if i % 2 == 0:
        continue
    print(i)  # 1, 3, 5, 7, 9

# else：循环正常结束时执行
for i in range(5):
    print(i)
else:
    print("循环完成")  # 会执行

for i in range(5):
    if i == 3:
        break
    print(i)
else:
    print("循环完成")  # 不会执行（因为 break）
```

**要点：**
- `for` 适合遍历序列，`while` 适合条件循环
- `break` 和 `continue` 控制循环流程
- 循环的 `else` 子句很少用，但知道有用

---

## 2. JSON 基础

JSON (JavaScript Object Notation) 是轻量级数据交换格式。

### 2.1 对象

JSON 对象用 `{}` 表示，包含键值对。

```json
{
    "name": "Alice",
    "age": 25,
    "isStudent": false,
    "city": "Beijing"
}
```

**规则：**
- 键必须是字符串（用双引号 `"`）
- 值可以是：字符串、数字、布尔值、null、对象、数组
- 键值对用逗号分隔
- 最后一个键值对后不加逗号

### 2.2 数组

JSON 数组用 `[]` 表示，有序元素列表。

```json
[
    "apple",
    "banana",
    "cherry"
]
```

```json
[
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
    {"name": "Charlie", "age": 35}
]
```

**规则：**
- 元素可以是任意类型
- 元素用逗号分隔
- 最后一个元素后不加逗号

### 2.3 字段读取

**JSON 路径语法：**

```json
{
    "user": {
        "name": "Alice",
        "contacts": {
            "email": "alice@example.com",
            "phones": ["123-4567", "987-6543"]
        }
    },
    "orders": [
        {"id": 1, "product": "Book"},
        {"id": 2, "product": "Pen"}
    ]
}
```

**读取路径：**
| 目标 | 路径 |
|------|------|
| 用户名 | `user.name` → "Alice" |
| 邮箱 | `user.contacts.email` → "alice@example.com" |
| 第一个电话 | `user.contacts.phones[0]` → "123-4567" |
| 第一个订单产品 | `orders[0].product` → "Book" |
| 所有订单ID | `orders[*].id` → [1, 2] |

---

## 3. Python 操作 JSON

### 3.1 基本操作

```python
import json

# Python 字典 → JSON 字符串
data = {"name": "Alice", "age": 25, "city": "Beijing"}
json_str = json.dumps(data)
print(json_str)
# {"name": "Alice", "age": 25, "city": "Beijing"}

# 格式化输出
json_str = json.dumps(data, indent=2, ensure_ascii=False)
print(json_str)
# {
#   "name": "Alice",
#   "age": 25,
#   "city": "Beijing"
# }

# JSON 字符串 → Python 字典
parsed = json.loads(json_str)
print(parsed["name"])  # "Alice"

# 写入文件
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# 读取文件
with open("data.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)
    print(loaded)
```

### 3.2 处理嵌套 JSON

```python
import json

json_data = '''
{
    "users": [
        {"name": "Alice", "scores": [85, 90, 78]},
        {"name": "Bob", "scores": [92, 88, 95]}
    ],
    "metadata": {
        "total": 2,
        "subject": "Math"
    }
}
'''

data = json.loads(json_data)

# 访问嵌套数据
print(data["users"][0]["name"])          # "Alice"
print(data["users"][1]["scores"][2])     # 95
print(data["metadata"]["subject"])       # "Math"

# 遍历用户
for user in data["users"]:
    avg_score = sum(user["scores"]) / len(user["scores"])
    print(f"{user['name']}: {avg_score:.1f}")
# Alice: 84.3
# Bob: 91.7
```

### 3.3 错误处理

```python
import json

# 处理无效 JSON
invalid_json = '{"name": "Alice", age: 25}'  # age 没引号，无效

try:
    data = json.loads(invalid_json)
except json.JSONDecodeError as e:
    print(f"JSON 解析错误: {e}")

# 安全访问嵌套字段
def safe_get(data, *keys, default=None):
    """安全获取嵌套字典的值"""
    result = data
    for key in keys:
        if isinstance(result, dict) and key in result:
            result = result[key]
        else:
            return default
    return result

data = {"user": {"name": "Alice"}}
print(safe_get(data, "user", "name"))           # "Alice"
print(safe_get(data, "user", "email"))           # None
print(safe_get(data, "user", "email", default="N/A"))  # "N/A"
```

---

## 快速参考卡

### Python 速查

| 操作 | 代码 |
|------|------|
| 列表创建 | `items = [1, 2, 3]` |
| 列表追加 | `items.append(4)` |
| 列表访问 | `items[0]`, `items[-1]` |
| 列表切片 | `items[1:3]`, `items[:2]` |
| 字典创建 | `d = {"a": 1, "b": 2}` |
| 字典访问 | `d["a"]`, `d.get("c", 0)` |
| 字典遍历 | `for k, v in d.items():` |
| 循环范围 | `for i in range(5):` |
| 循环枚举 | `for i, x in enumerate(items):` |

### JSON 速查

| Python 类型 | JSON 类型 |
|-------------|-----------|
| dict | object |
| list, tuple | array |
| str | string |
| int, float | number |
| True/False | true/false |
| None | null |

---

## 练习建议

1. **变量练习**：创建不同类型的变量，使用 `type()` 查看类型
2. **函数练习**：编写一个计算器函数，支持加减乘除
3. **列表练习**：实现一个简单的待办事项列表
4. **字典练习**：创建一个联系人管理系统
5. **循环练习**：使用循环打印九九乘法表
6. **JSON练习**：从 API 获取 JSON 数据并解析（如天气 API）

---

*文档创建于 2026-03-31*