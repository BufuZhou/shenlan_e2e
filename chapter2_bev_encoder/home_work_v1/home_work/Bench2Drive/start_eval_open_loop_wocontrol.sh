#!/bin/bash

# 设置环境变量 - GPU 显存优化
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export CUDA_LAUNCH_BLOCKING=0
export TORCH_CUDA_ARCH_LIST="8.6"  # RTX 3050 的架构

# 设置环境变量
export CARLA_ROOT="/home/lifanjie/shenlan_e2e/carla"
export CARLA_SERVER="/home/lifanjie/shenlan_e2e/carla/CarlaUE4.sh"
export SCENARIO_RUNNER_ROOT="/home/lifanjie/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/scenario_runner"
export PYTHONPATH="/home/lifanjie/shenlan_e2e/carla/PythonAPI:/home/lifanjie/shenlan_e2e/carla/PythonAPI/carla:/home/lifanjie/shenlan_e2e/carla/PythonAPI/carla/dist/carla-0.9.15-py3.7-linux-x86_64.egg:/home/lifanjie/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer:/home/lifanjie/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer/adzoo:/home/lifanjie/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive:/home/lifanjie/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/leaderboard:/home/lifanjie/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/leaderboard/team_code:/home/lifanjie/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive:/home/lifanjie/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/scenario_runner"

# Python路径
PYTHON="/home/lifanjie/shenlan_e2e/drivetransformer/bin/python"
PROGRAM="leaderboard/leaderboard/leaderboard_evaluator.py"

cd /home/lifanjie/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive

# 创建输出目录
mkdir -p DriveTransformer_b2d_open_loop

echo "========================================"
echo "开环仿真 - 使用GT航点"
echo "Open-loop Simulation with GT Waypoints"
echo "========================================"
echo ""
echo "按 Ctrl+C 停止仿真"
echo "========================================"

# 执行命令
$PYTHON $PROGRAM \
    --routes=leaderboard/data/drivetransformer_bench2drive_dev10_open_loop.xml \
    --repetitions=1 \
    --track=SENSORS \
    --checkpoint=DriveTransformer_b2d_open_loop/eval_bench2drive_dev_10_open_loop.json \
    --agent=leaderboard/team_code/drivetransformer_vis_agent_open_loop_wocontrol.py \
    --agent-config=/home/lifanjie/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer/adzoo/drivetransformer/configs/drivetransformer/drivetransformer_large.py+/home/lifanjie/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer/ckpts/drivetransformer_large.pth \
    --debug=0 \
    --record="" \
    --port=30002 \
    --traffic-manager-port=50001 \
    --gpu-rank=0

echo ""
echo "========================================"
echo "仿真结束"
echo "========================================"