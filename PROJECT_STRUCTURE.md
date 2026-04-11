# 项目管理指南

## 📁 项目结构

```
shenlan_e2e/
├── projects/                    # 项目代码目录
│   ├── drivetransformer/       # DriveTransformer主项目（ICLR 2025）
│   │   ├── adzoo/              # 算法工具库
│   │   ├── team_code/          # 核心代码
│   │   │   ├── drivetransformer_b2d_agent.py
│   │   │   ├── pid_controller.py
│   │   │   └── planner.py
│   │   ├── ckpts/              # 模型权重目录（不提交到git）
│   │   ├── docs/               # 项目文档
│   │   └── requirements.txt    # 项目依赖
│   └── bench2drive/            # Bench2Drive评估基准
│
├── experiments/                 # 实验记录（不提交到git）
│   ├── exp001_baseline/        # 基线实验
│   ├── exp002_improved/        # 改进实验
│   └── README.md               # 实验说明
│
├── models/                      # 模型权重存储（不提交到git）
│   └── drivetransformer/
│
├── data/                        # 数据集（软链接或说明文档）
│   └── README.md               # 数据下载说明
│
├── scripts/                     # 通用脚本
│   ├── setup.sh                # 环境设置
│   ├── train.sh                # 训练脚本
│   └── evaluate.sh             # 评估脚本
│
├── docs/                        # 项目文档
│   ├── INSTALL.md              # 安装指南
│   ├── DATA_PREP.md            # 数据准备
│   └── TRAIN_EVAL.md           # 训练和评估
│
├── .gitignore                   # Git忽略文件
├── README.md                    # 项目说明
├── PROJECT_STRUCTURE.md         # 本文件
└── requirements.txt             # 全局依赖（可选）
```

## 🔧 Git管理策略

### 分支管理

```bash
# 主要分支
main/master          # 稳定版本，可发布
dev                  # 开发主分支

# 功能分支
feature/data-prep    # 数据预处理功能
feature/training     # 训练流程改进
feature/evaluation   # 评估模块

# 实验分支
experiment/bev-v1    # BEV编码器v1实验
experiment/loss-v2   # 损失函数v2实验

# 修复分支
bugfix/carla-crash   # 修复CARLA崩溃问题
```

### 提交规范

```bash
# 格式: <type>: <description>

# 示例
git commit -m "feat: add BEV encoder module"
git commit -m "fix: resolve CUDA memory leak"
git commit -m "docs: update installation guide"
git commit -m "exp: baseline experiment results"

# Type类型:
# feat:     新功能
# fix:      bug修复
# docs:     文档更新
# style:    代码格式（不影响功能）
# refactor: 重构
# test:     测试相关
# chore:    构建过程或辅助工具变动
# exp:      实验记录
```

## 📦 大文件管理

### 不提交到Git的文件

以下文件/目录已在`.gitignore`中配置，不会提交：

1. **模型权重** (`*.pth`, `*.pt`, `ckpts/`)
   - 原因：文件太大（几GB）
   - 建议：使用云存储或单独仓库

2. **训练输出** (`outputs/`, `results/`, `tensorboard/`)
   - 原因：频繁变化，体积大
   - 建议：定期备份到外部存储

3. **数据集** (`data/`)
   - 原因：非常大（几十GB到几百GB）
   - 建议：使用软链接指向外部存储

4. **虚拟环境** (`drivetransformer/`, `venv/`)
   - 原因：可从requirements.txt重建
   - 建议：记录Python版本和关键包版本

### 推荐的大文件管理方案

#### 方案1: Git LFS (Large File Storage)
```bash
# 安装Git LFS
git lfs install

# 跟踪大文件类型
git lfs track "*.pth"
git lfs track "*.pt"

# 正常提交
git add models/model.pth
git commit -m "add pretrained model"
```

#### 方案2: 云存储 + 下载脚本
```bash
# 创建下载脚本
cat > scripts/download_models.sh << 'EOF'
#!/bin/bash
mkdir -p models/drivetransformer
wget https://your-storage.com/drivetransformer.pth -O models/drivetransformer/latest.pth
EOF

chmod +x scripts/download_models.sh
```

#### 方案3: DVC (Data Version Control)
```bash
# 安装DVC
pip install dvc

# 初始化
dvc init

# 跟踪大文件
dvc add models/drivetransformer.pth

# 提交
git add models/drivetransformer.pth.dvc .gitignore
git commit -m "add model checkpoint"
```

## 📝 实验管理

### 实验记录模板

在 `experiments/expXXX_description/README.md` 中记录：

```markdown
# Experiment XXX: [实验名称]

## 日期
2026-04-11

## 目标
[实验目的]

## 配置
- Model: DriveTransformer-Large
- Dataset: Bench2Drive
- Batch Size: 8
- Learning Rate: 1e-4
- Epochs: 50

## 修改内容
1. 修改了BEV编码器的注意力机制
2. 调整了损失函数权重

## 结果
- Driving Score: XX.XX
- Route Completion: XX.XX%
- Infraction Penalty: X.XX

## 结论
[实验结论和下一步计划]
```

### 实验目录结构

```
experiments/exp001_baseline/
├── config.yaml           # 实验配置
├── logs/                 # 训练日志
├── checkpoints/          # 检查点
├── metrics.json          # 评估指标
├── tensorboard/          # TensorBoard日志
└── README.md             # 实验说明
```

## 🚀 工作流程建议

### 日常开发流程

```bash
# 1. 更新到最新开发分支
git checkout dev
git pull origin dev

# 2. 创建功能分支
git checkout -b feature/your-feature

# 3. 开发和测试
# ... 编写代码 ...

# 4. 提交更改
git add .
git commit -m "feat: your feature description"

# 5. 推送到远程
git push origin feature/your-feature

# 6. 创建Pull Request合并到dev
```

### 实验流程

```bash
# 1. 基于dev创建实验分支
git checkout -b experiment/exp001

# 2. 进行实验
python train.py --config configs/exp001.yaml

# 3. 记录实验结果
# 在 experiments/exp001/ 中保存结果

# 4. 提交实验代码（不包括大文件）
git add .
git commit -m "exp: baseline experiment setup"

# 5. 如果实验成功，合并到dev
git checkout dev
git merge experiment/exp001
```

## 📚 文档维护

### 必须维护的文档

1. **README.md**: 项目概述、快速开始
2. **INSTALL.md**: 详细安装步骤
3. **DATA_PREP.md**: 数据准备流程
4. **TRAIN_EVAL.md**: 训练和评估指南
5. **PROJECT_STRUCTURE.md**: 本文件，项目结构说明

### 文档更新时机

- 添加新功能时
- 修改配置时
- 发现常见问题时
- 实验流程变更时

## 🔐 敏感信息管理

### 不要提交的内容

- API密钥
- 数据库密码
- 个人访问令牌
- `.env` 文件

### 使用方法

```bash
# 创建 .env.example 作为模板
cat > .env.example << 'EOF'
API_KEY=your_api_key_here
DATA_PATH=/path/to/data
EOF

# 添加到 .gitignore
echo ".env" >> .gitignore

# 使用时复制并填写
cp .env.example .env
# 编辑 .env 填入真实值
```

## 💡 最佳实践

1. **频繁提交**: 小的、原子化的提交更容易追踪
2. **清晰的commit message**: 说明做了什么和为什么
3. **定期备份**: 重要实验结果备份到外部存储
4. **版本标签**: 重要里程碑打tag
   ```bash
   git tag -a v1.0.0 -m "First stable release"
   git push origin v1.0.0
   ```
5. **Code Review**: 合并前进行代码审查
6. **持续集成**: 考虑设置CI/CD自动测试

## 🆘 常见问题

### Q: 误提交了大文件怎么办？
```bash
# 从git历史中移除
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch models/*.pth' \
  --prune-empty --tag-name-filter cat -- --all
```

### Q: 如何查看某个文件的修改历史？
```bash
git log --follow -- path/to/file.py
git blame path/to/file.py  # 查看每行最后修改
```

### Q: 如何回退到之前的版本？
```bash
git log                    # 查看commit历史
git reset --hard <commit-hash>  # 回退（谨慎使用）
git revert <commit-hash>       # 创建新的回退提交（推荐）
```

## 📞 需要帮助？

遇到问题时：
1. 查看项目文档
2. 搜索issues和discussions
3. 联系项目维护者
4. 参考原论文和官方实现
