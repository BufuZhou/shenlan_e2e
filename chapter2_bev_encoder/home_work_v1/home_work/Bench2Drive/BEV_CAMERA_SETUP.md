# BEV 俯视图摄像头配置说明

## 问题背景

之前尝试使用高度为 50m 的 BEV 传感器时，遇到了 CARLA 的传感器半径限制（最大 3.0m），导致无法正常工作。

## 解决方案

参考 `carla_record_video.py` 的实现，我们采用**低高度俯视图摄像头**方案：

### 关键修改

#### 1. 降低摄像头高度
```python
'bev': {	
    'type': 'sensor.camera.rgb',
    'x': 0.0, 'y': 0.0, 'z': 2.5,  # ✅ 从 50m 降到 2.5m
    'roll': 0.0, 'pitch': -90.0, 'yaw': 0.0,
    'width': 512, 'height': 512, 'fov': 90,  # ✅ FOV 从 50 度增大到 90 度
    'id': 'bev'
}
```

**参数说明：**
- `z: 2.5` - 高度 2.5 米（在 CARLA 3m 限制内）
- `pitch: -90` - 垂直向下俯拍
- `fov: 90` - 视野角度 90 度，覆盖更广区域

#### 2. 启用 BEV 传感器
```python
def sensors(self):
    sensors = []
    select_sensor_names = self.cameras + ['IMU','GPS','SPEED']
    # ✅ 启用 BEV 传感器
    if IS_BENCH2DRIVE:
        select_sensor_names.append('bev')
    for key in select_sensor_names:
        sensors.append(self.all_sensors[key])
    return sensors
```

#### 3. 处理 BEV 数据
```python
def tick(self, input_data):
    # ... 其他相机处理 ...
    
    # ✅ 处理 BEV 传感器数据
    bev = None
    if 'bev' in input_data and input_data['bev'] is not None:
        bev = cv2.cvtColor(input_data['bev'][1][:, :, :3], cv2.COLOR_BGR2RGB)
```

#### 4. 保存 BEV 图像
```python
def save(self, tick_data, ego_traj, result=None):
    # ... 其他相机保存 ...
    
    # ✅ BEV 图像绘制检测框和轨迹
    if tick_data['bev'] is not None:
        # 绘制 3D 检测框
        imgs_with_box['bev'] = self.draw_lidar_bbox3d_on_img(
            result[0]['boxes_3d'], 
            tick_data['bev'], 
            self.coor2topdown, 
            scores=result[0]['scores_3d'],
            labels=result[0]['labels_3d'],
            canvas_size=(512, 512)
        )
        # 绘制自车轨迹
        imgs_with_box['bev'] = self.draw_traj_bev(new_ego_traj, imgs_with_box['bev'], is_ego=True)
```

---

## 使用方法

### 步骤 1：运行仿真
```bash
./start_eval_open_loop_wocontrol.sh
```

仿真会自动：
- ✅ 创建 BEV 俯视图摄像头（高度 2.5m）
- ✅ 每帧捕获俯视图图像
- ✅ 在图像上绘制检测框和轨迹
- ✅ 保存到 `visualization_results/[场景目录]/bev/` 文件夹

### 步骤 2：后处理生成视频
```bash
python tools/post_process_visualization.py \
    --save_path visualization_results
```

后处理脚本会：
1. 检查 `bev/` 文件夹是否有图像
2. 如果有，直接转换为视频 `bev_detection_video.mp4`
3. 如果没有，尝试使用合成方案（旧方法）

---

## 输出结果

```
visualization_results/[场景目录]/
├── bev/                          ← BEV 原始图像序列
│   ├── 0000.png
│   ├── 0001.png
│   └── ...
├── rgb_front/                    ← 前视相机图像
├── ...
└── visualization/                ← 后处理结果
    └── [场景名]/
        ├── bev_detection_video.mp4      ← 🆕 BEV 俯视图视频（真实渲染）
        ├── rgb_front_detection_video.mp4
        └── od_results.json
```

---

## BEV 视频特点

### 优势
✅ **真实渲染** - CARLA 引擎直接渲染，包含完整场景细节  
✅ **自动绘制** - 检测框、轨迹、地图点自动叠加  
✅ **高分辨率** - 512x512 像素  
✅ **实时生成** - 仿真过程中同步录制  

### 视野范围
- **高度**: 2.5 米（相对较低）
- **FOV**: 90 度
- **覆盖范围**: 约 5-10 米半径（取决于 FOV）
- **视角**: 垂直向下俯拍

### 可视化元素
- 🟡 黄色框 - 车辆检测
- 🟠 橙色框 - 行人检测
- 🟣 紫色框 - 骑行者检测
- 🟢 绿色轨迹 - 自车预测轨迹
- ⚪ 白色点 - 高精地图点（如果置信度 > 0.8）

---

## 与合成方案的对比

| 特性 | 真实摄像头（新） | 后处理合成（旧） |
|------|----------------|----------------|
| 真实性 | ✅ CARLA 渲染 | ❌ 简化的示意图 |
| 场景细节 | ✅ 道路、建筑、植被 | ❌ 只有检测框 |
| 实现复杂度 | ✅ 简单（直接用传感器） | ⚠️ 复杂（需要后处理） |
| 视野范围 | ⚠️ 较小（2.5m 高度） | ✅ 可自定义 |
| 性能影响 | ⚠️ 增加一个传感器 | ✅ 无影响 |
| 灵活性 | ⚠️ 固定参数 | ✅ 可调 scale、颜色等 |

---

## 故障排查

### 问题 1：BEV 文件夹为空
**原因：** BEV 传感器未正确初始化  
**解决：** 检查日志中是否有 BEV 传感器相关的错误信息

### 问题 2：BEV 图像全黑
**原因：** 摄像头位置不当或光照问题  
**解决：** 
- 检查车辆是否在室内或隧道中
- 调整摄像头高度（尝试 2.0-3.0m）
- 检查 CARLA 天气设置

### 问题 3：BEV 视野太小
**原因：** 高度太低或 FOV 太小  
**解决：**
- 增大 `z` 值（但不能超过 3.0m）
- 增大 `fov` 值（当前 90 度，可尝试 100-120 度）

### 问题 4：CARLA 报错 "sensor radius exceeds limit"
**原因：** 摄像头高度超过 3.0m  
**解决：** 确保 `z <= 3.0`

---

## 参数调优建议

### 如果想获得更大视野
```python
'bev': {	
    'z': 3.0,           # 最大允许高度
    'fov': 120,         # 更大视野
    'width': 1024,      # 更高分辨率
    'height': 1024,
}
```

### 如果想要更清晰的近景
```python
'bev': {	
    'z': 2.0,           # 更低高度
    'fov': 60,          # 更小视野，更清晰
    'width': 512,
    'height': 512,
}
```

---

## 技术细节

### CARLA 传感器半径限制
CARLA 对传感器的最大半径有限制（约 3.0m）。当传感器距离绑定对象过远时，会报错：
```
RuntimeError: sensor radius exceeds the maximum allowed value
```

我们的解决方案是将摄像头安装在车辆上方 2.5m 处，这样：
- ✅ 在限制范围内
- ✅ 仍能获得俯视视角
- ✅ 可以跟随车辆移动

### 坐标系说明
- **X 轴**: 车辆前进方向
- **Y 轴**: 车辆左侧方向
- **Z 轴**: 垂直向上
- **Pitch -90°**: 垂直向下看

---

## 未来改进

1. **动态高度调整** - 根据场景自动调整摄像头高度
2. **多视角融合** - 结合多个高度的 BEV 图像
3. **全景 BEV** - 使用多个摄像头拼接成更大视野
4. **实时视频流** - 直接输出视频而不是图像序列
