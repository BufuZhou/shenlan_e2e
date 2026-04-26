#!/bin/bash

# 设置环境变量
export CARLA_ROOT="/root/project/shenlan_e2e/carla"
export CARLA_SERVER="/root/project/shenlan_e2e/carla/CarlaUE4.sh"
export SCENARIO_RUNNER_ROOT="/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/scenario_runner"
export PYTHONPATH="/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work:/root/project/shenlan_e2e/carla/PythonAPI:/root/project/shenlan_e2e/carla/PythonAPI/carla:/root/project/shenlan_e2e/carla/PythonAPI/carla/dist/carla-0.9.15-py3.7-linux-x86_64.egg:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/leaderboard:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/leaderboard/team_code:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive:/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/scenario_runner"

# 可视化相关配置
export VISUALIZATION_SAVE_PATH="/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/visualization_results_quick"
export SAVE_PATH="$VISUALIZATION_SAVE_PATH"

# Python路径
PYTHON="/root/miniconda3/envs/drivetransformer/bin/python"
PROGRAM="leaderboard/leaderboard/leaderboard_evaluator.py"

cd /root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive

# 创建输出目录
mkdir -p DriveTransformer_quick_eval
mkdir -p "$VISUALIZATION_SAVE_PATH"

# 设置日志文件
LOG_FILE="simulation_quick_eval_$(date +%Y%m%d_%H%M%S).log"

echo "========================================"
echo "Quick 模型闭环评测 - Quick Model Evaluation"
echo "========================================"
echo ""
echo "模型配置: drivetransformer_quick.py"
echo "可视化结果将保存到: $VISUALIZATION_SAVE_PATH"
echo "日志文件: $LOG_FILE"
echo ""
echo "注意: 请确保训练已完成，checkpoint 文件存在！"
echo "按 Ctrl+C 停止仿真"
echo "========================================"

# 查找最新的 checkpoint 文件
CHECKPOINT_DIR="/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer/adzoo/drivetransformer/work_dirs/drivetransformer/drivetransformer_quick"
LATEST_CHECKPOINT=$(ls -t "$CHECKPOINT_DIR"/iter_*.pth 2>/dev/null | head -n 1)

# 如果找不到 iter_*.pth，尝试找 epoch_*.pth
if [ -z "$LATEST_CHECKPOINT" ]; then
    LATEST_CHECKPOINT=$(ls -t "$CHECKPOINT_DIR"/epoch_*.pth 2>/dev/null | head -n 1)
fi

# 如果还是找不到，尝试 latest.pth
if [ -z "$LATEST_CHECKPOINT" ]; then
    if [ -f "$CHECKPOINT_DIR/latest.pth" ]; then
        LATEST_CHECKPOINT="$CHECKPOINT_DIR/latest.pth"
    fi
fi

if [ -z "$LATEST_CHECKPOINT" ]; then
    echo "错误: 未找到训练完成的 checkpoint 文件！"
    echo "请等待训练完成后再运行此脚本。"
    exit 1
fi

echo ""
echo "使用检查点: $LATEST_CHECKPOINT"
echo ""

# 执行命令，使用 script 命令确保完整日志记录
script -q -c "$PYTHON $PROGRAM \
    --routes=leaderboard/data/drivetransformer_bench2drive_dev4.xml \
    --repetitions=1 \
    --track=SENSORS \
    --checkpoint=DriveTransformer_quick_eval/eval_quick.json \
    --agent=leaderboard/team_code/drivetransformer_vis_agent.py \
    --agent-config=/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer/adzoo/drivetransformer/configs/drivetransformer/drivetransformer_quick.py+${LATEST_CHECKPOINT} \
    --debug=0 \
    --record=\"\" \
    --port=30001 \
    --traffic-manager-port=50000 \
    --gpu-rank=0" "$LOG_FILE" 2>&1

echo ""
echo "========================================"
echo "评测完成！"
echo "========================================"
echo ""
echo "接下来可以运行视频生成脚本："
echo "python /root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/tools/generate_video.py"
echo ""
echo "或者手动修改 generate_video.py 中的 case_name 参数后运行。"
