#!/bin/bash

# ========================================
# 清理 CARLA 进程和端口
# ========================================
echo "========================================"
echo "清理 CARLA 进程和端口..."
echo "========================================"

# 使用 clean_carla.sh 清理进程
bash /root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/tools/clean_carla.sh

# 等待一下确保进程完全退出
sleep 2

# 动态检测并清理所有 CARLA 相关端口
echo "检测 CARLA 相关端口..."

# 定义需要检查的端口范围
CARLA_PORTS=(30001 30002 30003 30004 30005 30006 30007 30008 30009 30010)
TM_PORTS=(50000 50001 50002 50003 50004 50005 50006 50007 50008 50009 50010)
ALL_PORTS=("${CARLA_PORTS[@]}" "${TM_PORTS[@]}")

# 检测哪些端口被占用
echo "扫描端口使用情况..."
occupied_ports=()
for port in "${ALL_PORTS[@]}"; do
    pid=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pid" ]; then
        echo "  ⚠️ 端口 $port 被进程 $pid 占用"
        occupied_ports+=($port)
    fi
done

if [ ${#occupied_ports[@]} -eq 0 ]; then
    echo "  ✓ 没有发现占用的 CARLA 端口"
else
    echo ""
    echo "开始清理 ${#occupied_ports[@]} 个被占用的端口..."
    
    # 清理每个被占用的端口
    for port in "${occupied_ports[@]}"; do
        echo ""
        echo "清理端口 $port:"
        
        # 多次尝试清理，确保端口完全释放
        for attempt in 1 2 3; do
            pid=$(lsof -ti:$port 2>/dev/null)
            if [ ! -z "$pid" ]; then
                echo "  第$attempt次尝试：清理占用端口 $port 的进程: $pid"
                kill -9 $pid 2>/dev/null
                sleep 1
            else
                echo "  ✓ 端口 $port 已释放"
                break
            fi
        done
        
        # 最后检查
        pid=$(lsof -ti:$port 2>/dev/null)
        if [ ! -z "$pid" ]; then
            echo "  ✗ 警告：端口 $port 仍被进程 $pid 占用"
        else
            echo "  ✓ 端口 $port 清理成功"
        fi
    done
fi

# 等待10秒，确认端口完全释放
echo ""
echo "等待10秒，确认所有端口完全释放..."
sleep 10

# 最终验证端口状态
echo "最终验证端口状态："
port_clean=true
for port in "${ALL_PORTS[@]}"; do
    pid=$(lsof -ti:$port 2>/dev/null)
    if [ ! -z "$pid" ]; then
        echo "  ✗ 错误：端口 $port 仍被进程 $pid 占用！"
        port_clean=false
    fi
done

if [ "$port_clean" = false ]; then
    echo ""
    echo "========================================"
    echo "错误：部分端口清理失败，无法启动仿真"
    echo "请手动检查并清理以下端口后重试："
    for port in "${ALL_PORTS[@]}"; do
        pid=$(lsof -ti:$port 2>/dev/null)
        if [ ! -z "$pid" ]; then
            echo "  - 端口 $port (进程 $pid)"
        fi
    done
    echo "========================================"
    exit 1
fi

echo ""
echo "✓ 所有 CARLA 端口已确认清理完成"

# 再次等待确保端口释放
sleep 1

echo "CARLA 进程清理完成"
echo "========================================"
echo ""

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

# 设置日志文件
LOG_FILE="simulation_$(date +%Y%m%d_%H%M%S).log"

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
echo "日志文件: $LOG_FILE"
echo "按 Ctrl+C 停止仿真"
echo "========================================"

# 执行命令，使用 script 命令确保完整日志记录
script -q -c "$PYTHON $PROGRAM \
    --routes=leaderboard/data/drivetransformer_bench2drive_dev10_open_loop.xml \
    --repetitions=1 \
    --track=SENSORS \
    --checkpoint=DriveTransformer_b2d_open_loop/eval_bench2drive_dev_10_open_loop.json \
    --agent=leaderboard/team_code/drivetransformer_vis_agent_open_loop_wocontrol.py \
    --agent-config=/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer/adzoo/drivetransformer/configs/drivetransformer/drivetransformer_large.py+/root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer/ckpts/drivetransformer_large.pth \
    --debug=0 \
    --record=\"\" \
    --port=30002 \
    --traffic-manager-port=50001 \
    --gpu-rank=0 \
    --enable-visualization \
    --visualization-save-path=\"$VISUALIZATION_SAVE_PATH\"" "$LOG_FILE" 2>&1

echo ""
echo "========================================"
echo "仿真结束"
echo "========================================"
echo ""
echo "提示：仿真完成后，运行以下命令生成视频和JSON文件："
echo "python tools/post_process_visualization.py --save_path $VISUALIZATION_SAVE_PATH"