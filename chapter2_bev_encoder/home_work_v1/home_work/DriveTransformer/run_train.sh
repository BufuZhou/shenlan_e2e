#!/usr/bin/env bash

# ============================================================================
# DriveTransformer 训练脚本
# ============================================================================
# 使用方法:
#   bash run_train.sh [配置文件] [GPU数量]
#   例如: bash run_train.sh drivetransformer_large.py 1
# ============================================================================

set -e

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 默认配置
CFG=${1:-"adzoo/drivetransformer/configs/drivetransformer/drivetransformer_large.py"}
GPUS=${2:-1}

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}DriveTransformer 训练脚本${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}配置文件: ${CFG}${NC}"
echo -e "${YELLOW}GPU 数量: ${GPUS}${NC}"
echo ""

# 检查配置文件是否存在
if [ ! -f "$CFG" ]; then
    echo -e "${RED}错误: 配置文件不存在: $CFG${NC}"
    exit 1
fi

# 检查数据目录
echo -e "${YELLOW}检查数据目录...${NC}"
if [ ! -d "data/bench2drive/v1" ]; then
    echo -e "${RED}错误: 数据目录不存在: data/bench2drive/v1${NC}"
    exit 1
fi

if [ ! -d "data/split" ]; then
    echo -e "${RED}错误: 数据分割文件目录不存在: data/split${NC}"
    exit 1
fi

# 检查是否需要预处理数据
INFO_DIR="data/infos"
if [ ! -d "$INFO_DIR" ] || [ -z "$(ls -A $INFO_DIR 2>/dev/null)" ]; then
    echo -e "${YELLOW}数据未预处理，开始预处理...${NC}"
    echo ""
    
    cd adzoo/drivetransformer/mmdet3d_plugin/datasets
    python preprocess_bench2drive_drivetransformer.py --workers 4
    cd ../../../../
    
    echo -e "${GREEN}数据预处理完成！${NC}"
    echo ""
else
    echo -e "${GREEN}数据已预处理，跳过预处理步骤${NC}"
    echo ""
fi

# 设置环境变量
export WORK_DIR=$(echo ${CFG%.*} | sed -e "s/configs/work_dirs/g")/
export PYTHONPATH="$PWD:$PYTHONPATH"

# 创建工作目录
if [ ! -d "${WORK_DIR}logs" ]; then
    mkdir -p ${WORK_DIR}logs
fi

echo -e "${YELLOW}工作目录: ${WORK_DIR}${NC}"
echo ""

# 开始训练
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}开始训练${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

if [ "$GPUS" -eq 1 ]; then
    # 单 GPU 训练
    echo -e "${YELLOW}使用单 GPU 训练${NC}"
    python adzoo/drivetransformer/train.py $CFG --gpus 1 2>&1 | tee ${WORK_DIR}logs/train.log
else
    # 多 GPU 分布式训练
    echo -e "${YELLOW}使用 ${GPUS} GPU 分布式训练${NC}"
    
    GPUS_PER_NODE=$(($GPUS<8?$GPUS:8))
    NNODES=`expr $GPUS / $GPUS_PER_NODE`
    MASTER_PORT=${MASTER_PORT:-35201}
    MASTER_ADDR=${MASTER_ADDR:-"127.0.0.1"}
    RANK=${RANK:-0}
    
    python -m torch.distributed.launch \
        --nproc_per_node=${GPUS_PER_NODE} \
        --master_addr=${MASTER_ADDR} \
        --master_port=${MASTER_PORT} \
        --nnodes=${NNODES} \
        --node_rank=${RANK} \
        adzoo/drivetransformer/train.py \
        $CFG \
        --launcher pytorch \
        2>&1 | tee ${WORK_DIR}logs/train.log
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}训练完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${YELLOW}日志文件: ${WORK_DIR}logs/train.log${NC}"
echo -e "${YELLOW}模型保存位置: ${WORK_DIR}${NC}"
