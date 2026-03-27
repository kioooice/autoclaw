# 2026-03-26 YOLO CPU 部署方案研究

## 背景
用户有 i3-12100 CPU 边缘设备，需要实时目标检测方案（无 GPU）。

## 决策
推荐 YOLOv8n + OpenVINO 方案，预估 100-150 FPS。

## 输出
- 创建案例：`insights/cases/yolo-cpu-deployment.md`
- 包含完整部署步骤、替代品对比、优化技巧

---
*记录于 2026-03-26 SESSION COMMIT*