# Job Tracker - 工作投递记录 App

## 📱 项目概述

一个专为求职者设计的 Android 应用，用于记录和管理工作投递信息。

## ✨ 核心功能

### 1. 投递记录管理
- 添加新投递（公司、职位、投递日期、状态）
- 编辑/删除投递记录
- 查看投递详情

### 2. 状态追踪
- 投递状态：已投递 → 简历筛选 → 笔试 → 面试 → Offer → 已拒绝
- 可视化进度展示

### 3. 数据统计
- 投递总数统计
- 各状态数量统计
- 投递成功率分析

### 4. 提醒功能
- 面试提醒
- 跟进提醒

## 🛠️ 技术栈

- **语言**: Kotlin
- **UI**: Jetpack Compose
- **架构**: MVVM + Repository Pattern
- **数据库**: Room (本地存储)
- **依赖注入**: Hilt
- **导航**: Jetpack Navigation

## 📁 项目结构

```
app/
├── data/
│   ├── local/
│   │   ├── JobApplicationDao.kt
│   │   ├── JobApplicationDatabase.kt
│   │   └── entity/
│   │       └── JobApplicationEntity.kt
│   ├── repository/
│   │   └── JobApplicationRepository.kt
│   └── model/
│       ├── JobApplication.kt
│       └── ApplicationStatus.kt
├── di/
│   └── AppModule.kt
├── ui/
│   ├── theme/
│   │   ├── Color.kt
│   │   ├── Theme.kt
│   │   └── Type.kt
│   ├── components/
│   │   ├── JobApplicationCard.kt
│   │   ├── StatusBadge.kt
│   │   └── StatisticsCard.kt
│   ├── screens/
│   │   ├── HomeScreen.kt
│   │   ├── AddEditScreen.kt
│   │   ├── DetailScreen.kt
│   │   └── StatisticsScreen.kt
│   └── viewmodel/
│       ├── HomeViewModel.kt
│       ├── AddEditViewModel.kt
│       └── StatisticsViewModel.kt
└── MainActivity.kt
```

## 🚀 快速开始

### 环境要求
- Android Studio Hedgehog (2023.1.1) 或更高版本
- JDK 17
- Android SDK 34
- Kotlin 1.9.0

### 运行项目
1. 克隆项目
2. 在 Android Studio 中打开
3. 同步 Gradle
4. 运行到模拟器或真机

## 📊 数据库设计

### JobApplication 表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Long | 主键，自增 |
| companyName | String | 公司名称 |
| position | String | 职位名称 |
| status | String | 投递状态 |
| applyDate | Long | 投递日期（时间戳） |
| salary | String | 薪资范围（可选） |
| location | String | 工作地点（可选） |
| notes | String | 备注（可选） |
| createdAt | Long | 创建时间 |
| updatedAt | Long | 更新时间 |

## 🎨 UI 设计

### 主色调
- Primary: #1976D2 (蓝色)
- Secondary: #4CAF50 (绿色)
- Background: #FFFFFF
- Surface: #F5F5F5
- Error: #B00020

### 状态颜色
- 已投递: #9E9E9E (灰色)
- 简历筛选: #FFC107 (琥珀色)
- 笔试: #FF9800 (橙色)
- 面试: #2196F3 (蓝色)
- Offer: #4CAF50 (绿色)
- 已拒绝: #F44336 (红色)

## 📱 界面预览

### 首页
- 顶部统计卡片
- 投递列表（按时间倒序）
- 悬浮添加按钮

### 添加/编辑页
- 表单输入
- 状态选择器
- 日期选择器

### 详情页
- 完整信息展示
- 状态更新按钮
- 编辑/删除操作

### 统计页
- 投递趋势图表
- 状态分布饼图
- 成功率分析

## 🔧 后续优化

- [ ] 数据导出/导入
- [ ] 云同步
- [ ] 面试提醒通知
- [ ] 暗黑模式
- [ ] 多语言支持

## 📄 许可证

MIT License
