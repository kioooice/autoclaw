# 铁锈智能识别系统 - 机器学习升级方案

## 一、现状分析

### 当前方案
- 基于 HSV 颜色空间的阈值分割
- 简单的色相/饱和度/亮度判断
- 优点：快速、无需训练、可解释
- 缺点：对光照敏感、复杂背景易误判、难以区分相似颜色

### 升级目标
- 提高识别准确率（目标 >90%）
- 降低误检率（背景误判 <5%）
- 适应不同光照条件
- 支持不同类型金属表面

---

## 二、技术方案

### 方案对比

| 方案 | 难度 | 准确率 | 训练数据需求 | 部署复杂度 |
|------|------|--------|--------------|------------|
| 方案A: 传统ML分类 | ⭐⭐ | 80-85% | 500+ | 低 |
| 方案B: 深度学习分割 | ⭐⭐⭐ | 90-95% | 1000+ | 中 |
| 方案C: 预训练模型微调 | ⭐⭐ | 85-92% | 200+ | 低 |
| 方案D: 混合方案 | ⭐⭐⭐ | 92-98% | 500+ | 中 |

**推荐：方案D（混合方案）**

---

## 三、混合方案详解

### 架构设计

```
输入图片
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  第一阶段：快速筛选（传统CV）                          │
│  - HSV 颜色分割                                      │
│  - 边缘检测                                          │
│  - 输出：候选区域                                    │
└─────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  第二阶段：精细分类（深度学习）                        │
│  - CNN 分类器判断候选区域是否为铁锈                   │
│  - 输出：置信度分数                                  │
└─────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  第三阶段：后处理                                    │
│  - 形态学优化                                        │
│  - 轮廓分析                                          │
│  - 输出：最终结果                                    │
└─────────────────────────────────────────────────────┘
```

### 优势
1. **效率高** - 传统CV先筛选，减少ML计算量
2. **准确率高** - ML处理边界情况
3. **可解释** - 每个阶段都可追踪调试

---

## 四、实施步骤

### Phase 1: 数据准备（1-2周）

#### 1.1 数据收集
```
数据来源：
├── 公开数据集
│   ├── NEU 表面缺陷数据集
│   ├── GC10-DET 金属缺陷数据集
│   └── 自建数据集
│
└── 实际场景数据
    ├── 正常金属表面（负样本）
    ├── 不同程度铁锈（正样本）
    ├── 不同光照条件
    └── 不同金属材质
```

#### 1.2 数据标注
```bash
# 推荐工具
- LabelMe：多边形标注
- CVAT：视频/图像标注
- LabelImg：矩形标注

# 标注格式
├── images/
│   ├── img_001.jpg
│   ├── img_002.jpg
│   └── ...
└── labels/
    ├── img_001.json  # 标注文件
    ├── img_002.json
    └── ...
```

#### 1.3 数据增强
```python
# 增强策略
transformations = {
    'rotate': [90, 180, 270],      # 旋转
    'flip': ['horizontal', 'vertical'],  # 翻转
    'brightness': [0.8, 1.2],      # 亮度
    'contrast': [0.8, 1.2],        # 对比度
    'noise': ['gaussian', 'salt'], # 噪声
    'blur': [3, 5],                # 模糊
}
```

### Phase 2: 模型开发（2-3周）

#### 2.1 模型选择

**候选模型：**

| 模型 | 大小 | 速度 | 适合场景 |
|------|------|------|----------|
| MobileNetV3 | 5MB | 快 | 浏览器端 |
| EfficientNet-B0 | 20MB | 中 | 平衡选择 |
| ResNet18 | 45MB | 中 | 高精度 |
| U-Net (分割) | 30MB | 慢 | 像素级分割 |

**推荐：MobileNetV3 + 轻量分割头**

#### 2.2 训练代码框架

```python
# train.py
import tensorflow as tf
from tensorflow.keras import layers, models

def build_rust_detector():
    """构建铁锈检测模型"""
    
    # 使用预训练 MobileNetV3 作为骨干
    base = tf.keras.applications.MobileNetV3Small(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    
    # 冻结前几层
    for layer in base.layers[:50]:
        layer.trainable = False
    
    # 分类头
    x = base.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(128, activation='relu')(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(2, activation='softmax')(x)  # 铁锈/非铁锈
    
    model = models.Model(base.input, outputs)
    return model

# 编译模型
model = build_rust_detector()
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# 训练
model.fit(
    train_dataset,
    validation_data=val_dataset,
    epochs=50,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(patience=5),
        tf.keras.callbacks.ModelCheckpoint('best_model.h5')
    ]
)

# 转换为 TensorFlow.js 格式
import tensorflowjs as tfjs
tfjs.converters.save_keras_model(model, 'tfjs_model')
```

#### 2.3 数据集划分

```
总数据集
├── 训练集 70%
├── 验证集 15%
└── 测试集 15%

# 每个类别样本数建议
- 铁锈样本：500-1000+
- 非铁锈样本：500-1000+
- 背景样本：200-500+
```

### Phase 3: 浏览器端部署（1周）

#### 3.1 模型转换

```bash
# Keras -> TensorFlow.js
tensorflowjs_converter --input_format keras \
    model.h5 \
    ./tfjs_model

# 输出文件
tfjs_model/
├── model.json          # 模型结构
├── group1-shard1of1.bin # 权重文件
└── ...
```

#### 3.2 前端集成

```javascript
// ml-detector.js
class RustMLDetector {
    constructor() {
        this.model = null;
        this.ready = false;
    }

    async load() {
        // 加载 TensorFlow.js 模型
        this.model = await tf.loadLayersModel('./tfjs_model/model.json');
        this.ready = true;
        console.log('ML模型加载完成');
    }

    async predict(imageData) {
        if (!this.ready) return null;

        // 预处理
        const tensor = tf.browser.fromPixels(imageData)
            .resizeBilinear([224, 224])
            .toFloat()
            .div(255.0)
            .expandDims(0);

        // 预测
        const prediction = await this.model.predict(tensor).data();
        
        // 返回结果
        return {
            isRust: prediction[1] > 0.5,
            confidence: prediction[1] * 100
        };
    }

    async detectRustRegions(image, candidateRegions) {
        // 对候选区域进行精细分类
        const results = [];
        
        for (const region of candidateRegions) {
            const patch = this.extractPatch(image, region);
            const pred = await this.predict(patch);
            
            if (pred.isRust) {
                results.push({
                    ...region,
                    confidence: pred.confidence
                });
            }
        }
        
        return results;
    }
}
```

#### 3.3 混合检测流程

```javascript
async function hybridDetection(img) {
    // 1. 传统CV快速筛选
    const candidates = await quickHSVFilter(img);
    console.log(`候选区域: ${candidates.length}`);
    
    // 2. ML精细分类
    const rustRegions = await mlDetector.detectRustRegions(img, candidates);
    console.log(`确认铁锈: ${rustRegions.length}`);
    
    // 3. 后处理
    const finalResult = postProcess(rustRegions);
    
    return finalResult;
}
```

### Phase 4: 持续改进（长期）

#### 4.1 反馈收集机制

```javascript
// 用户标注接口
function collectFeedback(imageId, isCorrect, userCorrection) {
    fetch('/api/feedback', {
        method: 'POST',
        body: JSON.stringify({
            imageId,
            isCorrect,
            timestamp: Date.now(),
            correction: userCorrection // 用户标注的正确区域
        })
    });
}

// 在界面上添加反馈按钮
// ✓ 正确识别  ✗ 识别错误
```

#### 4.2 定期重训练

```bash
# 每月/每季度执行
1. 导出用户反馈数据
2. 数据清洗和标注审核
3. 合并到训练集
4. 增量训练或全量重训练
5. A/B 测试新模型
6. 部署上线
```

#### 4.3 性能监控

```javascript
// 监控指标
const metrics = {
    accuracy: 0,        // 准确率
    falsePositive: 0,   // 误检率
    falseNegative: 0,   // 漏检率
    avgProcessTime: 0,  // 平均处理时间
    userFeedback: 0     // 用户反馈比例
};

// 上报监控数据
function reportMetrics(metric, value) {
    // 发送到分析平台
}
```

---

## 五、资源需求

### 5.1 硬件

| 用途 | 配置 | 预算 |
|------|------|------|
| 模型训练 | GPU (RTX 3060+) | ¥3000-5000 |
| 数据存储 | 500GB SSD | ¥300 |
| 云训练(可选) | Colab Pro / AutoDL | ¥100-300/月 |

### 5.2 软件/工具

```
开发环境:
- Python 3.9+
- TensorFlow 2.x / PyTorch
- OpenCV
- NumPy, Pandas

标注工具:
- LabelMe (免费)
- CVAT (开源)

部署:
- TensorFlow.js
- CDN 托管模型文件
```

### 5.3 人力

| 阶段 | 工作量 | 技能要求 |
|------|--------|----------|
| 数据准备 | 40-80小时 | 数据标注、清洗 |
| 模型开发 | 40-60小时 | ML/DL、CV |
| 前端集成 | 20-30小时 | JavaScript、TF.js |
| 测试优化 | 20-40小时 | 测试、调试 |

---

## 六、时间规划

```
Week 1-2:  数据收集、标注
Week 3-4:  模型训练、调优
Week 5:    前端集成、部署
Week 6:    测试、优化
Week 7+:   持续改进
```

---

## 七、风险与应对

| 风险 | 概率 | 应对措施 |
|------|------|----------|
| 数据不足 | 中 | 数据增强、迁移学习 |
| 过拟合 | 中 | Dropout、数据增强、早停 |
| 浏览器性能 | 低 | 模型量化、混合方案 |
| 准确率不达标 | 中 | 收集更多数据、调整模型 |

---

## 八、下一步行动

### 立即可做
1. ✅ 收集现有图片样本
2. ✅ 安装标注工具 (LabelMe)
3. ✅ 开始标注 100-200 张图片

### 本周目标
1. 完成 200+ 样本标注
2. 搭建训练环境
3. 跑通第一个 baseline 模型

### 本月目标
1. 完成数据集构建 (500+ 样本)
2. 训练并评估模型
3. 集成到现有系统

---

## 附录：参考资源

### 数据集
- [NEU Metal Surface Defect Dataset](https://github.com/justisdPSU/NEU_det)
- [GC10-DET](https://github.com/lukeai/gc10det)
- [Severstal Steel Defect Detection](https://www.kaggle.com/c/severstal-steel-defect-detection)

### 论文
- "Surface Defect Detection of Metal Parts Based on Deep Learning"
- "Automatic Detection of Steel Surface Defects Using CNN"

### 教程
- [TensorFlow.js 官方教程](https://www.tensorflow.org/js/tutorials)
- [迁移学习指南](https://www.tensorflow.org/tutorials/images/transfer_learning)

---

*方案版本: v1.0*
*创建时间: 2026-03-25*
*维护者: AI Assistant*