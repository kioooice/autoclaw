# YOLO CPU 部署方案（边缘设备无 GPU）

## 问题
- 场景：边缘设备无 GPU，需要实时目标检测
- 硬件：Intel i3-12100 CPU

## 解决方案：YOLOv8n + OpenVINO

### 性能预估（i3-12100）
| 配置 | FPS | 延迟 |
|------|-----|------|
| YOLOv8n (OpenVINO) | 100-150 | 6-10ms |
| YOLOv8s (OpenVINO) | 40-60 | 16-25ms |

### 部署步骤
```bash
pip install ultralytics openvino
yolo export model=yolov8n.pt format=openvino
```

### Python 推理
```python
from ultralytics import YOLO
model = YOLO("yolov8n_openvino_model/")
results = model("image.jpg")
```

## YOLO 替代品对比（2024-2025）

| 方案 | 优势 | 劣势 | 适合场景 |
|------|------|------|----------|
| YOLOv8/v11 | 生态最成熟、文档全 | 商用需授权 | 通用检测、快速落地 |
| YOLOv10 | 无 NMS、更快推理 | 生态较新 | 追求速度 |
| RT-DETR | 端到端、无后处理 | 比 YOLO 略慢 | 精确定位 |
| Grounding DINO | 零样本、自然语言 | 需 GPU、较重 | 开放词汇检测 |
| NanoDet | 1.8MB、极轻量 | 精度一般 | 树莓派/低端设备 |

## 优化技巧
- 降低分辨率：`imgsz=320` 或 `imgsz=416`
- OpenVINO：Intel CPU 专用优化
- ONNX Runtime：通用加速方案

---
*创建于 2026-03-26，提炼自 experiences/2026-03-26.md*