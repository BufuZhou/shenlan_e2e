#!/bin/bash

# 设置环境变量
export CARLA_ROOT="/root/project/shenlan_e2e/carla"
export CARLA_SERVER="/root/project/shenlan_e2e/carla/CarlaUE4.sh"
export SCENARIO_RUNNER_ROOT="/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/scenario_runner"
export PYTHONPATH="/root/project/shenlan_e2e/carla/PythonAPI:/root/project/shenlan_e2e/carla/PythonAPI/carla:/root/project/shenlan_e2e/carla/PythonAPI/carla:/root/project/shenlan_e2e/carla/PythonAPI/carla/dist/carla-0.9.15-py3.7-linux-x86_64.egg:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer/adzoo:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/leaderboard:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/leaderboard/team_code:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/scenario_runner:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work"

# 可视化相关配置
export ENABLE_VISUALIZATION=1  # 启用可视化
export VISUALIZATION_SAVE_PATH="/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/visualization_results"

# Python路径
PYTHON="python"
PROGRAM="leaderboard/leaderboard/leaderboard_evaluator.py"

cd /root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive

# 创建输出目录
mkdir -p DriveTransformer_b2d_open_loop
mkdir -p "$VISUALIZATION_SAVE_PATH"

echo "========================================"
echo "开环仿真 - 使用GT航点"
echo "Open-loop Simulation with GT Waypoints"
echo "========================================"
echo ""
echo "可视化结果将保存到: $VISUALIZATION_SAVE_PATH"
echo "按 Ctrl+C 停止仿真"
echo "========================================"

# 执行命令
$PYTHON $PROGRAM \
    --routes=leaderboard/data/drivetransformer_bench2drive_dev10_open_loop.xml \
    --repetitions=1 \
    --track=SENSORS \
    --checkpoint=DriveTransformer_b2d_open_loop/eval_bench2drive_dev_10_open_loop.json \
    --agent=leaderboard/team_code/drivetransformer_vis_agent_open_loop_wocontrol.py \
    --agent-config=/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer/adzoo/drivetransformer/configs/drivetransformer/drivetransformer_large.py+/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer/ckpts/drivetransformer_large.pth \
    --debug=0 \
    --record="" \
    --port=30002 \
    --traffic-manager-port=50001 \
    --gpu-rank=0 \
    --enable-visualization \
    --visualization-save-path="$VISUALIZATION_SAVE_PATH"

echo ""
echo "========================================"
echo "仿真结束"
echo "========================================"
echo ""
echo "提示：仿真完成后，运行以下命令生成视频和JSON文件："
echo "python tools/post_process_visualization.py --save_path $VISUALIZATION_SAVE_PATH"