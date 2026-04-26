#!/usr/bin/env bash

# ============================================================================
# 快速启动训练脚本
# ============================================================================
# 一键启动 DriveTransformer 训练
# ============================================================================

set -e

# 进入项目目录
cd /root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer

echo "============================================"
echo "  DriveTransformer 快速启动"
echo "============================================"
echo ""
echo "请选择训练配置："
echo "1) 小型配置 (单卡, ~8GB 显存)"
echo "2) 大型配置 (多卡, ~24GB+ 显存)"
echo ""
read -p "请输入选项 (1/2, 默认 1): " choice

case ${choice:-1} in
    1)
        echo ""
        echo "使用小型配置..."
        echo ""
        bash run_train.sh adzoo/drivetransformer/configs/drivetransformer/drivetransformer_small.py 1
        ;;
    2)
        echo ""
        read -p "请输入 GPU 数量 (默认 8): " gpus
        echo ""
        echo "使用大型配置，${gpus:-8} GPU..."
        echo ""
        bash run_train.sh adzoo/drivetransformer/configs/drivetransformer/drivetransformer_large.py ${gpus:-8}
        ;;
    *)
        echo "无效选项，退出"
        exit 1
        ;;
esac
