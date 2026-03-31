# Git 基础命令教程

> 重点：status、add、commit、log、diff

---

## 目录

1. [Git 是什么](#1-git-是什么)
2. [git status 查看状态](#2-git-status-查看状态)
3. [git add 添加到暂存区](#3-git-add-添加到暂存区)
4. [git commit 提交更改](#4-git-commit-提交更改)
5. [git log 查看历史](#5-git-log-查看历史)
6. [git diff 查看差异](#6-git-diff-查看差异)
7. [完整工作流程](#7-完整工作流程)

---

## 1. Git 是什么

Git 是版本控制系统，跟踪文件的变化历史。

```
工作目录 ──→ 暂存区 ──→ 本地仓库 ──→ 远程仓库

你编辑文件      git add      git commit     git push
```

**核心概念：**

| 区域 | 说明 |
|------|------|
| **工作目录** | 你实际编辑的文件 |
| **暂存区** | 准备提交的文件（等待区） |
| **本地仓库** | 已提交的历史记录 |
| **远程仓库** | GitHub/GitLab 等云端备份 |

---

## 2. git status 查看状态

`git status` 显示当前文件状态，是最常用的命令。

### 2.1 基本用法

```bash
git status
```

### 2.2 输出解读

```bash
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   README.md        # 绿色：已暂存，准备提交
        new file:   utils.py

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
        modified:   app.py           # 红色：已修改，未暂存
        deleted:    old_file.txt

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        test.py                     # 红色：新文件，未跟踪
```

### 2.3 文件状态

| 状态 | 显示 | 含义 | 下一步 |
|------|------|------|--------|
| **Untracked** | 红色 | 新文件，Git 未跟踪 | `git add` |
| **Modified** | 红色 | 已修改，未暂存 | `git add` |
| **Staged** | 绿色 | 已暂存，准备提交 | `git commit` |
| **Deleted** | 红色 | 已删除，未暂存 | `git add`（确认删除） |
| **Committed** | 不显示 | 已提交到仓库 | 完成 |

### 2.4 简洁输出

```bash
# 简短格式
git status -s

# 输出：
M  README.md     # 左边M = 已暂存
 M app.py        # 右边M = 未暂存
?? test.py       # ?? = 未跟踪
D  old_file.txt  # 已暂存删除
 D deleted.txt   # 未暂存删除
```

### 2.5 常用场景

```bash
# 开始工作前，先看状态
git status

# 添加文件后，确认是否暂存
git status

# 提交前，最后确认
git status

# 随时查看，养成习惯
git status
```

---

## 3. git add 添加到暂存区

`git add` 将文件从工作目录添加到暂存区。

### 3.1 基本用法

```bash
# 添加单个文件
git add filename.txt

# 添加多个文件
git add file1.txt file2.txt file3.txt

# 添加当前目录下所有文件
git add .

# 添加所有文件（整个仓库）
git add -A
git add --all

# 添加所有已跟踪的修改文件（不含新文件）
git add -u
```

### 3.2 添加示例

```bash
# 创建新文件
echo "print('hello')" > test.py

# 查看状态
git status
# test.py 显示为 Untracked（红色）

# 添加到暂存区
git add test.py

# 再看状态
git status
# test.py 显示为 Changes to be committed（绿色）
```

### 3.3 添加修改的文件

```bash
# 修改已有文件
echo "# 新增注释" >> README.md

# 查看状态
git status
# README.md 显示为 modified（红色）

# 添加修改
git add README.md

# 状态变为 staged（绿色）
git status
```

### 3.4 添加删除的文件

```bash
# 删除文件
rm old_file.txt

# 查看状态
git status
# deleted: old_file.txt（红色）

# 确认删除
git add old_file.txt
# 或
git add -u  # 添加所有删除

# 状态变为 staged deleted（绿色）
```

### 3.5 添加部分内容

```bash
# 只添加文件的部分修改（交互式）
git add -p filename.txt

# Git 会逐块询问：
# y = 暂存这块
# n = 不暂存这块
# q = 退出
# a = 暂存所有
# d = 不暂存所有
```

### 3.6 撤销添加

```bash
# 撤销暂存（文件回到未暂存状态）
git restore --staged filename.txt
# 或旧命令
git reset HEAD filename.txt

# 撤销所有暂存
git restore --staged .
```

---

## 4. git commit 提交更改

`git commit` 将暂存区的文件保存到本地仓库。

### 4.1 基本用法

```bash
# 提交暂存区的内容
git commit -m "提交说明"

# 示例
git commit -m "添加用户登录功能"
git commit -m "修复密码验证 bug"
git commit -m "更新 README 文档"
```

### 4.2 提交信息规范

**好的提交信息：**

```bash
git commit -m "添加用户注册功能"
git commit -m "修复登录页面样式问题"
git commit -m "优化数据库查询性能"
git commit -m "删除废弃的测试文件"
```

**不好的提交信息：**

```bash
git commit -m "更新"              # ❌ 太模糊
git commit -m "修改了一些东西"     # ❌ 不知道改了什么
git commit -m "fix"               # ❌ 没说明修复了什么
git commit -m "111"               # ❌ 无意义
```

### 4.3 多行提交信息

```bash
# 打开编辑器写多行提交信息
git commit

# 或直接写多行
git commit -m "标题" -m "详细描述" -m "更多说明"

# 示例
git commit -m "添加用户注册功能" \
           -m "- 实现邮箱注册" \
           -m "- 实现手机号注册" \
           -m "- 添加表单验证"
```

### 4.4 跳过暂存直接提交

```bash
# 将已跟踪文件的修改直接提交（跳过 git add）
git commit -a -m "提交说明"
git commit --all -m "提交说明"

# 注意：只适用于已跟踪文件，新文件仍需 git add
```

### 4.5 修改上次提交

```bash
# 修改上次提交的信息
git commit --amend -m "新的提交信息"

# 添加遗漏的文件到上次提交
git add forgotten_file.txt
git commit --amend --no-edit  # 保持原提交信息
```

### 4.6 查看提交内容

```bash
# 提交后查看
git log

# 查看具体改动
git show  # 最新提交
git show <commit-hash>  # 指定提交
```

---

## 5. git log 查看历史

`git log` 显示提交历史记录。

### 5.1 基本用法

```bash
git log
```

输出：

```
commit a1b2c3d4e5f6... (HEAD -> main)
Author: Alice <alice@example.com>
Date:   Tue Mar 31 15:00:00 2026 +0800

    添加用户登录功能

commit b2c3d4e5f6g7...
Author: Alice <alice@example.com>
Date:   Mon Mar 30 10:00:00 2026 +0800

    初始化项目

...
```

### 5.2 简洁输出

```bash
# 一行显示
git log --oneline

# 输出：
a1b2c3d 添加用户登录功能
b2c3d4 初始化项目
c3d4e5 配置 Git 忽略文件
```

### 5.3 显示最近 N 条

```bash
# 最近 3 条
git log -3
git log --oneline -3

# 输出：
a1b2c3d 添加用户登录功能
b2c3d4 初始化项目
c3d4e5 配置 Git 忽略文件
```

### 5.4 显示文件变动

```bash
# 显示每次提交改了哪些文件
git log --name-only

# 输出：
commit a1b2c3d
    添加用户登录功能

    auth.py
    login.html

commit b2c3d4
    初始化项目

    README.md
    main.py
```

```bash
# 显示文件变动统计
git log --stat

# 输出：
commit a1b2c3d
    添加用户登录功能

    auth.py      |  45 +++++++
    login.html   |  12 +++
    2 files changed, 57 insertions(+)
```

### 5.5 图形化显示分支

```bash
# 显示分支合并图
git log --oneline --graph

# 输出：
*   a1b2c3d 合并分支 feature-login
|\  
| * b2c3d4 添加登录功能
* | c3d4e5 修复 bug
|/  
* d4e5f6 初始化项目
```

### 5.6 按条件筛选

```bash
# 按作者筛选
git log --author="Alice"

# 按提交信息筛选
git log --grep="登录"

# 按时间筛选
git log --since="2026-03-01"
git log --until="2026-03-31"
git log --since="1 week ago"
git log --after="yesterday"

# 按文件筛选
git log -- auth.py  # 只看 auth.py 的提交历史
```

### 5.7 格式化输出

```bash
# 自定义格式
git log --pretty=format:"%h - %an, %ar : %s"

# 输出：
a1b2c3d - Alice, 2 hours ago : 添加用户登录功能
b2c3d4 - Alice, 1 day ago : 初始化项目

# 格式占位符：
# %h  = 短 hash
# %H  = 完整 hash
# %an = 作者名字
# %ae = 作者邮箱
# %ar = 相对时间
# %ad = 绝对时间
# %s  = 提交信息
```

---

## 6. git diff 查看差异

`git diff` 显示文件的具体改动内容。

### 6.1 三种 diff

```bash
# 工作目录 vs 暂存区（未暂存的改动）
git diff

# 暂存区 vs 最新提交（已暂存但未提交的改动）
git diff --staged
git diff --cached  # 同上

# 两次提交之间
git diff <commit1> <commit2>
```

### 6.2 工作目录 diff

```bash
# 查看所有未暂存的改动
git diff

# 查看单个文件的改动
git diff filename.txt
```

输出示例：

```diff
diff --git a/README.md b/README.md
index abc123..def456 100644
--- a/README.md
+++ b/README.md
@@ -1,5 +1,6 @@
 # Project Name
 
+# 新增的标题
 这是一个示例项目
 
-旧的一行内容
+新的一行内容
```

**解读：**

| 符号 | 含义 |
|------|------|
| `--- a/文件` | 原文件 |
| `+++ b/文件` | 新文件 |
| `@@ -1,5 +1,6 @@` | 原文件第1-5行，新文件第1-6行 |
| `-` 开头的行 | 删除的行（红色） |
| `+` 开头的行 | 新增的行（绿色） |
| 空格开头 | 未改变的行 |

### 6.3 暂存区 diff

```bash
# 查看已暂存的改动（即将提交的内容）
git diff --staged
git diff --cached

# 查看暂存的单个文件
git diff --staged filename.txt
```

### 6.4 提交间 diff

```bash
# 比较两次提交
git diff <旧commit> <新commit>

# 示例
git diff HEAD~2 HEAD      # 最近2次提交的差异
git diff a1b2c3 b2c3d4    # 指定两次提交

# 比较某个提交与当前
git diff a1b2c3           # 指定提交与当前工作目录
git diff a1b2c3 --staged  # 指定提交与暂存区
```

### 6.5 与分支比较

```bash
# 当前分支 vs 其他分支
git diff main             # 当前 vs main
git diff main feature     # main vs feature
```

### 6.6 只看文件名

```bash
# 只显示改了哪些文件，不看具体内容
git diff --name-only
git diff --name-status   # 显示状态（A/M/D）

# 输出：
M README.md
A new_file.txt
D deleted_file.txt
```

### 6.7 统计改动

```bash
# 显示改动统计
git diff --stat

# 输出：
README.md      |  5 ++---
new_file.txt   | 10 +++++++++++
deleted_file.txt |  3 ---
3 files changed, 10 insertions(+), 8 deletions(-)
```

### 6.8 diff 快速对照

| 命令 | 比较对象 |
|------|----------|
| `git diff` | 工作目录 vs 暂存区 |
| `git diff --staged` | 暂存区 vs 最新提交 |
| `git diff HEAD` | 工作目录 vs 最新提交 |
| `git diff A B` | 提交A vs 提交B |
| `git diff main` | 当前 vs main 分支 |

---

## 7. 完整工作流程

### 7.1 标准流程

```bash
# 1. 开始工作 - 查看状态
git status

# 2. 编辑文件
vim app.py

# 3. 查看改动
git diff app.py

# 4. 添加到暂存区
git add app.py

# 5. 确认暂存
git status
git diff --staged

# 6. 提交
git commit -m "修复登录验证 bug"

# 7. 查看历史
git log --oneline -3
```

### 7.2 实际示例

```bash
# 查看当前状态
$ git status
On branch main
nothing to commit, working tree clean

# 创建新文件
$ echo "def hello(): print('hello')" > utils.py

# 查看状态（新文件未跟踪）
$ git status
Untracked files:
    utils.py

# 添加到暂存区
$ git add utils.py

# 确认已暂存
$ git status
Changes to be committed:
    new file:   utils.py

# 提交
$ git commit -m "添加 utils.py 工具函数"

# 查看历史
$ git log --oneline -3
a1b2c3d 添加 utils.py 工具函数
b2c3d4 初始化项目
...

# 继续编辑
$ echo "def goodbye(): print('bye')" >> utils.py

# 查看改动内容
$ git diff utils.py
+def goodbye(): print('bye')

# 添加修改
$ git add utils.py

# 提交修改
$ git commit -m "添加 goodbye 函数"
```

### 7.3 多文件提交

```bash
# 修改多个文件
vim app.py
vim utils.py
vim README.md

# 查看所有改动
git diff

# 分别添加（精细控制）
git add app.py utils.py
# README.md 暂时不提交

# 或全部添加
git add .

# 提交
git commit -m "添加核心功能和文档"
```

### 7.4 日常检查习惯

```bash
# 每天开始工作
git status           # 看看有什么未完成
git log --oneline -5 # 看看最近做了什么

# 每次提交前
git diff             # 看看改了什么
git diff --staged    # 确认暂存的内容
git status           # 确认提交清单

# 提交后
git log --oneline -1 # 确认提交成功
```

---

## 快速参考卡

### status

```bash
git status          # 详细状态
git status -s       # 简短状态
```

状态含义：
- `??` = 新文件
- `M` = 已修改（右边=未暂存，左边=已暂存）
- `A` = 已添加
- `D` = 已删除

### add

```bash
git add file        # 添加单个文件
git add .           # 添加当前目录所有
git add -A          # 添加所有
git add -u          # 只添加已跟踪的修改
git add -p          # 交互式添加部分
```

撤销：
```bash
git restore --staged file  # 撤销暂存
```

### commit

```bash
git commit -m "说明"       # 提交
git commit -a -m "说明"    # 跳过暂存（已跟踪文件）
git commit --amend -m "新说明"  # 修改上次提交
```

提交信息规范：
- 说明做了什么，不要太长
- 用动词开头：添加、修复、更新、删除

### log

```bash
git log                     # 详细历史
git log --oneline           # 简洁一行
git log --oneline -5        # 最近5条
git log --oneline --graph   # 分支图
git log --stat              # 文件统计
git log --author="Alice"    # 按作者筛选
```

### diff

```bash
git diff             # 未暂存的改动
git diff --staged    # 已暂存的改动
git diff HEAD        # vs 最新提交
git diff A B         # 两次提交间
git diff --stat      # 只看统计
```

---

## 练习建议

1. **创建测试仓库**
   ```bash
   mkdir git-test && cd git-test
   git init
   ```

2. **练习 status**：创建、修改、删除文件，观察状态变化

3. **练习 add**：分别添加单文件、多文件、全部文件

4. **练习 commit**：写规范的提交信息

5. **练习 log**：用各种格式查看历史

6. **练习 diff**：故意修改文件，观察 diff 输出

---

*文档创建于 2026-03-31*