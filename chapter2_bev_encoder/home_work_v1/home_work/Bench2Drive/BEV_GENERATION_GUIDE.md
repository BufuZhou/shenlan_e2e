# BEV 俯视图生成说明

## 概述

由于 CARLA 传感器半径限制（最大 3.0m），无法直接使用高度为 50m 的 BEV 传感器。我们提供了两种方案来生成 BEV 俯视图：

## 方案对比

### 方案 1：后处理合成 BEV（推荐）✅

**优点：**
- ✅ 无需修改仿真代码
- ✅ 基于真实检测框和自车数据
- ✅ 清晰展示检测结果和车辆位置
- ✅ 可自定义颜色、比例尺等

**缺点：**
- ⚠️ 不是真实的渲染图像，是合成的示意图
- ⚠️ 不包含地图细节（道路、建筑等）

**使用方法：**
```bash
# 单独运行
python tools/generate_bev_video.py \
    --scenario_dir visualization_results/[场景目录] \
    --output_dir visualization_results/visualization/[场景目录]

# 或在后处理脚本中自动调用
python tools/post_process_visualization.py \
    --save_path visualization_results
```

**输出文件：**
- `bev_synthesized_video.mp4` - BEV 俯视图视频

---

### 方案 2：Spectator 相机录制（实验性）

**优点：**
- ✅ 真实的 CARLA 渲染图像
- ✅ 包含完整的场景细节

**缺点：**
- ⚠️ 需要启用环境变量 `ENABLE_BEV_RECORDING=1`
- ⚠️ 实现较复杂，当前版本仅移动 spectator 位置
- ⚠️ 无法直接捕获 spectator 视角的图像

**启用方法：**
```bash
export ENABLE_BEV_RECORDING=1
./start_eval_open_loop_wocontrol.sh
```

---

## BEV 合成视频特性

### 可视化元素

1. **自车位置**
   - 绿色圆点 + 十字标记（画布中心）
   - 方向箭头显示车辆朝向

2. **检测框**
   - 🟡 黄色：车辆 (vehicle)
   - 🟠 橙色：行人 (pedestrian)
   - 🟣 紫色：骑行者 (cyclist)
   - ⚪ 白色：其他物体

3. **辅助信息**
   - 网格线（每 10 米一条）
   - 比例尺（左下角）
   - 帧号（左上角）

### 参数配置

```bash
python tools/generate_bev_video.py \
    --scenario_dir <场景目录> \
    --output_dir <输出目录> \
    --fps 20 \              # 帧率
    --canvas_size 512 \     # 画布大小（像素）
    --scale 4.0             # 像素/米 比例
```

**建议参数：**
- `scale=4.0`：1 米 = 4 像素（适合城市道路场景）
- `canvas_size=512`：平衡清晰度和文件大小
- `fps=20`：与仿真帧率一致

---

## 完整工作流程

### 步骤 1：运行仿真
```bash
./start_eval_open_loop_wocontrol.sh
```

### 步骤 2：后处理（自动生成 BEV）
```bash
python tools/post_process_visualization.py \
    --save_path visualization_results
```

后处理脚本会：
1. 检查是否有原始 BEV 图像
2. 如果没有，自动调用 `generate_bev_video.py` 合成 BEV
3. 生成 RGB 前视视频
4. 生成 OD 检测结果 JSON

### 步骤 3：查看结果
```
visualization_results/visualization/[场景名]/
├── bev_synthesized_video.mp4       ← BEV 俯视图
├── rgb_front_detection_video.mp4   ← 前视相机（带检测框）
└── od_results.json                 ← 检测结果数据
```

---

## 故障排查

### 问题 1：BEV 视频未生成
**原因：** detections.json 文件缺失或损坏  
**解决：** 检查仿真是否正常保存了检测结果

### 问题 2：BEV 视频中看不到检测框
**原因：** 检测框置信度太低或被过滤  
**解决：** 检查 `detections.json` 中的分数，调整阈值

### 问题 3：BEV 视野太小或太大
**原因：** scale 参数不合适  
**解决：** 
- 增大 `scale`（如 6.0）→ 视野更小，细节更多
- 减小 `scale`（如 2.0）→ 视野更大，范围更广

---

## 示例输出

生成的 BEV 视频特点：
- 📹 分辨率：512x512
- 🎬 帧率：20 FPS
- 📦 文件大小：~1MB（126 帧）
- 🎨 深色背景 + 彩色检测框
- 📏 带比例尺和网格线

---

## 未来改进方向

1. **添加地图图层**
   - 从 CARLA HD Map 提取道路信息
   - 绘制车道线、路口等

2. **轨迹可视化**
   - 绘制自车历史轨迹
   - 显示预测轨迹

3. **3D 效果**
   - 使用透视投影增强立体感
   - 添加阴影效果

4. **实时生成**
   - 在仿真过程中实时生成 BEV
   - 避免后处理等待时间
