# DriveTransformer 训练指南

## 概述

本指南介绍如何在 Bench2Drive 数据集上训练 DriveTransformer 模型。

## 目录结构

训练脚本会自动创建以下目录结构：

```
/root/project/shenlan_e2e/data/
├── bench2drive/
│   ├── v1/                  # 数据集软链接
│   └── maps/                # 地图数据
├── infos/                   # 预处理后的数据信息
└── split/                   # 训练/验证集划分
```

## 快速开始

### 1. 数据准备

数据已经准备好，位于 `Bench2Drive-mini/` 目录。训练脚本会自动创建软链接到 `data/bench2drive/v1/`。

### 2. 运行训练

#### 使用小型配置（推荐，显存占用低）

```bash
cd /root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer

# 单 GPU 训练
bash run_train.sh adzoo/drivetransformer/configs/drivetransformer/drivetransformer_small.py 1
```

#### 使用大型配置（需要大显存）

```bash
# 多 GPU 训练（例如 8 卡）
bash run_train.sh adzoo/drivetransformer/configs/drivetransformer/drivetransformer_large.py 8
```

### 3. 训练流程

训练脚本会自动完成以下步骤：

1. **检查数据目录** - 验证数据是否存在
2. **数据预处理** - 如果未预处理，自动运行预处理脚本
3. **模型训练** - 启动训练过程
4. **保存日志** - 训练日志保存在 `work_dirs/` 目录

## 配置说明

### 小型配置 (drivetransformer_small.py)

适合显存有限的情况，主要调整：

- **特征维度**: 768 → 256
- **Transformer 层数**: 12 → 6
- **Batch Size**: 10 → 2
- **Query 数量**: 大幅减少
- **记忆帧数**: 10 → 5
- **训练轮数**: 60 → 30

预计显存占用: ~8-12 GB (单卡)

### 大型配置 (drivetransformer_large.py)

原始配置，适合大显存 GPU：

- **特征维度**: 768
- **Transformer 层数**: 12
- **Batch Size**: 10
- **需要 8 卡训练**

预计显存占用: ~24+ GB (单卡)

## 训练输出

训练过程中会产生以下输出：

- **模型检查点**: `work_dirs/drivetransformer_small/epoch_*.pth`
- **训练日志**: `work_dirs/drivetransformer_small/logs/train.log`
- **配置文件**: `work_dirs/drivetransformer_small/drivetransformer_small.py`

## 监控训练

### 查看实时日志

```bash
tail -f work_dirs/drivetransformer_small/logs/train.log
```

### 使用 TensorBoard

训练日志支持 TensorBoard 可视化：

```bash
tensorboard --logdir=work_dirs/drivetransformer_small/
```

然后在浏览器中打开 `http://localhost:6006`

## 恢复训练

如果训练中断，可以从检查点恢复：

```bash
python adzoo/drivetransformer/train.py \
    adzoo/drivetransformer/configs/drivetransformer/drivetransformer_small.py \
    --resume-from work_dirs/drivetransformer_small/epoch_latest.pth \
    --gpus 1
```

## 注意事项

1. **数据预处理时间较长**，首次运行请耐心等待
2. **大型配置需要大显存**，建议使用小型配置测试
3. **确保有足够的磁盘空间**（至少 50GB）
4. **训练时间较长**，可以使用 `nohup` 或 `screen` 后台运行

## 常见问题

### Q: 显存不足怎么办？
A: 使用小型配置，或进一步降低 batch_size 和模型大小。

### Q: 如何修改学习率？
A: 在配置文件中修改 `optimizer` 部分的 `lr` 参数。

### Q: 训练很慢怎么办？
A: 可以减少数据量，或使用更多 GPU 进行分布式训练。

### Q: 如何验证模型？
A: 训练过程中会自动进行验证，也可以使用评估脚本单独评估。

## 技术支持

如有问题，请参考：
- DriveTransformer 原始文档
- mmdetection3d 文档
- 查看训练日志文件
