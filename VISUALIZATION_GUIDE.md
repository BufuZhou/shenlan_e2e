# 可视化功能使用说明

## 概述

本作业要求提交可视化结果，包括BEV和RGB视角的检测视频，以及OD感知结果的JSON文件。

## 提交内容

### 1. 代码文件
需要提交以下修改/新增的文件：
- **修改后的启动脚本**: `start_eval_open_loop_wocontrol.sh`
- **修改后的评估器**: `leaderboard/leaderboard/leaderboard_evaluator.py` (添加了可视化参数)
- **修改后的Agent**: `leaderboard/team_code/drivetransformer_vis_agent_open_loop_wocontrol.py` (添加了检测结果保存功能)
- **后处理脚本**: `tools/post_process_visualization.py` (新增)

### 2. 可视化结果

仿真完成后，会生成以下文件：

#### (1) BEV和RGB视角视频
- **BEV视角视频**: `visualization_results/visualization/bev_detection_video.mp4`
  - 包含检测框的俯视图
  - 显示车辆、行人等目标的3D边界框
  
- **RGB前视视角视频**: `visualization_results/visualization/rgb_front_detection_video.mp4`
  - 包含检测框的前视摄像头画面
  - 显示前方目标的3D边界框

#### (2) OD感知结果JSON文件
- **位置**: `visualization_results/visualization/od_results.json`
- **内容**: 
  - 每帧的检测结果
  - 包含3D边界框、类别、置信度等信息
  - 自车轨迹信息

## 使用流程

### 步骤1: 运行仿真

```bash
cd /root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive

# 启动CARLA服务器
./CarlaUE4.sh -carla-rpc-port=30002 -vulkan -RenderOffScreen -nosound &

# 运行仿真（启用可视化）
bash start_eval_open_loop_wocontrol.sh
```

### 步骤2: 后处理生成视频和JSON

仿真完成后，运行后处理脚本：

```bash
cd /root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive

python tools/post_process_visualization.py \
    --save_path /root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/visualization_results \
    --fps 20
```

### 步骤3: 检查生成的文件

后处理完成后，会生成以下文件：

```
visualization_results/
├── rgb_front/           # RGB前视视角图片序列（含检测框）
├── bev/                 # BEV视角图片序列（含检测框）
├── meta/                # 元数据
├── detections.json      # 检测结果JSON
└── visualization/       # 后处理生成的视频和JSON
    ├── bev_detection_video.mp4       # BEV视频
    ├── rgb_front_detection_video.mp4 # RGB视频
    └── od_results.json               # OD感知结果JSON
```

## 自定义配置

### 修改保存路径

编辑 `start_eval_open_loop_wocontrol.sh`:

```bash
export VISUALIZATION_SAVE_PATH="/your/custom/path"
```

### 调整视频帧率

运行后处理脚本时指定 `--fps` 参数：

```bash
python tools/post_process_visualization.py \
    --save_path /path/to/save \
    --fps 30  # 修改为30fps
```

## 注意事项

1. **磁盘空间**: 图片序列和视频文件可能占用较大空间，确保有足够的磁盘空间
2. **仿真时间**: 启用可视化会略微增加仿真时间
3. **视频长度**: 根据作业要求，视频长度不要太长，可以选择关键片段
4. **检测框质量**: 确保模型能够正确输出检测结果，否则视频中可能没有检测框

## 问题排查

### 问题1: 没有生成图片
- 检查 `ENABLE_VISUALIZATION` 环境变量是否设置为1
- 检查 `--enable-visualization` 参数是否正确传递

### 问题2: 视频中没有检测框
- 检查模型是否正确加载
- 检查 `detections.json` 是否包含检测结果
- 确认模型输出的 `boxes_3d`, `scores_3d`, `labels_3d` 字段存在

### 问题3: 后处理脚本报错
- 确保图片序列文件夹存在
- 检查文件权限
- 查看错误信息中的具体路径

## 加分项建议

根据作业要求，以下实现可以获得加分：

1. **其他视频创意**:
   - 添加轨迹预测可视化
   - 添加速度/转向角等控制信息
   - 多视角拼接视频
   - 添加时间戳和帧号水印

2. **说明文档**:
   - 详细说明OD感知模型的实现逻辑
   - 记录遇到的问题和解决方案
   - 分析模型性能和局限性

## 提交清单

提交前请确认：

- [ ] 修改后的 `start_eval_open_loop_wocontrol.sh`
- [ ] 修改后的 `leaderboard_evaluator.py`
- [ ] 修改后的 `drivetransformer_vis_agent_open_loop_wocontrol.py`
- [ ] 新增的 `tools/post_process_visualization.py`
- [ ] BEV视角视频（含检测框）
- [ ] RGB前视视角视频（含检测框）
- [ ] OD感知结果JSON文件
- [ ] （可选）说明文档

祝作业顺利！
