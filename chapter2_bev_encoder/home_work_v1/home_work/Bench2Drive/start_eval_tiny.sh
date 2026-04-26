#!/bin/bash

# 设置环境变量
export CARLA_ROOT="/root/project/shenlan_e2e/carla"
export CARLA_SERVER="/root/project/shenlan_e2e/carla/CarlaUE4.sh"
export SCENARIO_RUNNER_ROOT="/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/scenario_runner"
export PYTHONPATH="/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work:/root/project/shenlan_e2e/carla/PythonAPI:/root/project/shenlan_e2e/carla/PythonAPI/carla:/root/project/shenlan_e2e/carla/PythonAPI/carla/dist/carla-0.9.15-py3.7-linux-x86_64.egg:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/leaderboard:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/leaderboard/team_code:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/scenario_runner"

# Python路径
PYTHON="/root/miniconda3/envs/drivetransformer/bin/python"
PROGRAM="leaderboard/leaderboard/leaderboard_evaluator.py"

cd /root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive

# 执行命令
$PYTHON $PROGRAM \
    --routes=leaderboard/data/drivetransformer_bench2drive_dev4.xml \
    --repetitions=1 \
    --track=SENSORS \
    --checkpoint=DriveTransformer_b2d_only_traj/eval_bench2drive_dev_4.json \
    --agent=leaderboard/team_code/drivetransformer_vis_agent.py \
    --agent-config=DriveTransformer/adzoo/drivetransformer/configs/drivetransformer/drivetransformer_tiny.py+DriveTransformer/ckpts/iter_93750.pth \
    --debug=0 \
    --record="" \
    --port=30001 \
    --traffic-manager-port=50000 \
    --gpu-rank=0
