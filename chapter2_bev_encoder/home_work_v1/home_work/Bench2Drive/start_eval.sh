#!/bin/bash

# 设置环境变量
export CARLA_ROOT="/root/project/shenlan_e2e/carla"
export CARLA_SERVER="/root/project/shenlan_e2e/carla/CarlaUE4.sh"
export SCENARIO_RUNNER_ROOT="/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/scenario_runner"
export PYTHONPATH="/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work:/root/project/shenlan_e2e/carla/PythonAPI:/root/project/shenlan_e2e/carla/PythonAPI/carla:/root/project/shenlan_e2e/carla/PythonAPI/carla/dist/carla-0.9.15-py3.7-linux-x86_64.egg:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/leaderboard:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/leaderboard/team_code:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/scenario_runner"

# 可视化相关配置
export VISUALIZATION_SAVE_PATH="/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/visualization_results"
export SAVE_PATH="$VISUALIZATION_SAVE_PATH"  # 让 SAVE_PATH 指向可视化结果目录

# Python路径
PYTHON="/root/miniconda3/envs/drivetransformer/bin/python"
PROGRAM="leaderboard/leaderboard/leaderboard_evaluator.py"

cd /root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive

# 创建输出目录
mkdir -p DriveTransformer_b2d_only_traj
mkdir -p "$VISUALIZATION_SAVE_PATH"

# 设置日志文件
LOG_FILE="simulation_closed_loop_$(date +%Y%m%d_%H%M%S).log"

echo "========================================"
echo "闭环仿真 - Closed Loop Evaluation"
echo "========================================"
echo ""
echo "可视化结果将保存到: $VISUALIZATION_SAVE_PATH"
echo "日志文件: $LOG_FILE"
echo "按 Ctrl+C 停止仿真"
echo "========================================"

# 执行命令，使用 script 命令确保完整日志记录
script -q -c "$PYTHON $PROGRAM \
    --routes=leaderboard/data/drivetransformer_bench2drive_dev4.xml \
    --repetitions=1 \
    --track=SENSORS \
    --checkpoint=DriveTransformer_b2d_only_traj/eval_bench2drive_dev4.json \
    --agent=leaderboard/team_code/drivetransformer_vis_agent.py \
    --agent-config=/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer/adzoo/drivetransformer/configs/drivetransformer/drivetransformer_large.py+/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer/ckpts/drivetransformer_large.pth \
    --debug=0 \
    --record=\"\" \
    --port=30001 \
    --traffic-manager-port=50000 \
    --gpu-rank=0" "$LOG_FILE" 2>&1
