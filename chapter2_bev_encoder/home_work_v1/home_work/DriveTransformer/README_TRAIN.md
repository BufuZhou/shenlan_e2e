# DriveTransformer 训练环境说明

## 环境配置完成 ✅

本文档说明如何开始训练 DriveTransformer 模型。

## 快速开始

### 方式一：交互式快速启动（推荐）

```bash
cd /root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer
bash quick_start.sh
```

脚本会提示您选择配置类型。

### 方式二：直接启动

```bash
cd /root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer

# 使用小型配置（推荐新手）
bash run_train.sh adzoo/drivetransformer/configs/drivetransformer/drivetransformer_small.py 1

# 使用大型配置（需要多卡大显存）
bash run_train.sh adzoo/drivetransformer/configs/drivetransformer/drivetransformer_large.py 8
```

## 已完成的配置

### 1. 数据准备 ✅

- [x] Bench2Drive-mini 数据已解压
- [x] 数据软链接已创建：`data/bench2drive/v1/`
- [x] 训练/验证集划分文件已复制：`data/split/bench2drive_base_train_val_split.json`
- [x] 地图目录已创建：`data/bench2drive/maps/`
- [x] 信息目录已创建：`data/infos/`

### 2. 训练脚本 ✅

- [x] 主训练脚本：`run_train.sh`
- [x] 快速启动脚本：`quick_start.sh`
- [x] 小型配置文件：`drivetransformer_small.py` (低显存)
- [x] 大型配置文件：`drivetransformer_large.py` (高显存)

### 3. 训练流程 ✅

训练脚本会自动处理以下步骤：

1. **检查数据** - 验证数据目录和文件
2. **数据预处理** - 如果未预处理，自动运行预处理脚本（耗时较长）
3. **启动训练** - 根据配置启动单卡或多卡训练
4. **保存结果** - 模型和日志保存到 `work_dirs/` 目录

## 配置对比

| 配置项 | 小型配置 | 大型配置 |
|--------|----------|----------|
| 特征维度 | 256 | 768 |
| Transformer层数 | 6 | 12 |
| Batch Size | 2 | 10 |
| GPU数量 | 1 | 8 |
| 预计显存 | ~8-12 GB | ~24+ GB |
| 训练轮数 | 30 | 60 |
| 适用场景 | 学习/测试 | 完整训练 |

## 数据目录结构

```
data/
├── bench2drive/
│   ├── v1/                      # Bench2Drive 数据集（软链接）
│   │   ├── Accident_Town03_Route156_Weather0/
│   │   ├── AccidentTwoWays_Town12_Route1444_Weather0/
│   │   └── ... (其他场景)
│   └── maps/                    # 地图数据目录
├── infos/                       # 预处理后的数据信息（自动生成）
└── split/                       # 数据集划分
    └── bench2drive_base_train_val_split.json
```

## 输出目录结构

训练后会在 `work_dirs/` 目录下生成：

```
work_dirs/drivetransformer_small/
├── epoch_*.pth                  # 模型检查点
├── drivetransformer_small.py    # 配置文件副本
├── logs/
│   └── train.log               # 训练日志
└── *.log                        # 其他日志文件
```

## 监控训练

### 实时查看日志

```bash
tail -f work_dirs/drivetransformer_small/logs/train.log
```

### TensorBoard 可视化

```bash
tensorboard --logdir=work_dirs/drivetransformer_small/
```

## 常见问题

### Q: 数据预处理需要多长时间？
A: 根据数据量和 CPU 核心数，通常需要 10-30 分钟。首次运行会自动执行。

### Q: 如何中断训练？
A: 按 `Ctrl+C` 可以安全中断，下次可以从检查点恢复。

### Q: 如何恢复训练？
A: 
```bash
python adzoo/drivetransformer/train.py \
    adzoo/drivetransformer/configs/drivetransformer/drivetransformer_small.py \
    --resume-from work_dirs/drivetransformer_small/epoch_latest.pth \
    --gpus 1
```

### Q: 显存不足怎么办？
A: 使用小型配置，或进一步减小 batch_size。

### Q: 训练可以后台运行吗？
A: 可以，使用 `nohup` 或 `screen`：
```bash
nohup bash run_train.sh adzoo/drivetransformer/configs/drivetransformer/drivetransformer_small.py 1 > train.out 2>&1 &
```

## 详细文档

更多详细信息请参考：
- [TRAINING_GUIDE.md](./TRAINING_GUIDE.md) - 完整训练指南

## 技术栈

- **深度学习框架**: PyTorch
- **训练框架**: mmdetection3d
- **数据集**: Bench2Drive-mini
- **模型**: DriveTransformer

## 下一步

1. 运行 `bash quick_start.sh` 开始训练
2. 监控训练日志
3. 训练完成后评估模型性能
4. 可视化训练结果

祝您训练顺利！ 🚀
