# 端到端自动驾驶学习项目

## 项目概述

本项目包含多个章节的端到端自动驾驶学习内容，每个章节有独立的项目和实验。

### 章节目录

- **第二章**: BEV Encoder - DriveTransformer (ICLR 2025)
  - 位置: `chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer`
  - 说明: 基于统一 Transformer 的可扩展端到端自动驾驶框架

---

## 🌍 公共环境配置

以下环境配置为所有章节项目共享，只需配置一次。

### 系统要求

- **操作系统**: Ubuntu 24.04 LTS
- **GPU**: NVIDIA GPU (支持CUDA 11.8+)
- **NVIDIA驱动**: 版本 >= 470.x (支持CUDA 11.8)
- **磁盘空间**: 至少20GB (包括CUDA Toolkit、依赖包和数据集)

### 核心技术栈

| 组件 | 版本 | 说明 |
|------|------|------|
| Python | 3.8 | 官方推荐版本 |
| CUDA Toolkit | 11.8 | 用于编译CUDA扩展 |
| PyTorch | 2.4.1+cu118 | 深度学习框架 |
| GCC | 9.5.0 | CUDA 11.8兼容的编译器 |
| MMCV | 0.0.1 | OpenMMLab计算机视觉库 |

### 当前环境状态 ✅

```bash
Python: 3.8.20
PyTorch: 2.4.1+cu118
CUDA: 11.8 (Toolkit)
GCC: 9.5.0
GPU: NVIDIA GeForce RTX 3050
虚拟环境: /home/lifanjie/shenlan_e2e/drivetransformer
```

---

## 🔧 公共环境安装指南

> **重要**: 此环境配置对所有章节项目通用，只需安装一次。

### 前置检查

在开始之前，请确认:

```bash
# 检查NVIDIA驱动
nvidia-smi

# 检查Python 3.8是否可用
python3.8 --version

# 检查磁盘空间
df -h /home
```

如果缺少Python 3.8，请先安装:

```bash
sudo apt-get update
sudo apt-get install -y python3.8 python3.8-venv python3.8-dev
```

### 步骤1: 创建Python 3.8虚拟环境

```bash
# 进入项目根目录
cd /home/lifanjie/shenlan_e2e

# 删除旧环境（如果存在）
rm -rf drivetransformer

# 使用Python 3.8创建新的虚拟环境
python3.8 -m venv drivetransformer

# 激活虚拟环境
source drivetransformer/bin/activate

# 验证Python版本
python --version  # 应显示 Python 3.8.20
```

### 步骤2: 升级pip并安装基础构建工具

```bash
# 升级pip到最新版本
pip install --upgrade pip

# 安装构建工具（编译CUDA扩展必需）
pip install packaging cython wheel
```

### 步骤3: 安装PyTorch with CUDA 11.8

```bash
# 安装PyTorch 2.4.1 with CUDA 11.8
# 下载大小约3-4GB，请耐心等待
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 验证PyTorch安装
python -c "import torch; print(f'PyTorch: {torch.__version__}'); print(f'CUDA: {torch.cuda.is_available()}')"
```

**预期输出**:
```
PyTorch: 2.4.1+cu118
CUDA: True
```

### 步骤4: 安装CUDA 11.8 Toolkit

> **为什么需要安装**: 系统可能只有旧版本CUDA（如10.0），但PyTorch 2.4.1需要CUDA 11.8来编译MMCV等库的CUDA扩展。

#### 4.1 下载CUDA 11.8安装包

```bash
# 下载CUDA 11.8安装包（约4GB，需要15-20分钟）
wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run -O /tmp/cuda_11.8.0_linux.run
```
#### 4.2 安装GCC 9（CUDA 11.8兼容性要求）

```bash
# CUDA 11.8需要GCC 9-11版本，Ubuntu 24.04默认是GCC 13
# 安装GCC 9
sudo apt-get install -y gcc-9 g++-9

# 设置GCC 9为默认编译器
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 90
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-9 90
sudo update-alternatives --set gcc /usr/bin/gcc-9
sudo update-alternatives --set g++ /usr/bin/g++-9

# 验证GCC版本
gcc --version  # 应显示: gcc-9 (Ubuntu 9.5.0-xxx)
```

#### 4.3 安装CUDA 11.8 Toolkit

```bash
# 只安装toolkit（不安装驱动，避免覆盖现有驱动）
sudo sh /tmp/cuda_11.8.0_linux.run --silent --toolkit --toolkitpath=/usr/local/cuda-11.8

# 安装过程约需5-10分钟，完成后设置环境变量
export CUDA_HOME=/usr/local/cuda-11.8
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

# 验证CUDA安装
nvcc --version  # 应显示: Cuda compilation tools, release 11.8
```

### 步骤5: 准备项目特定的依赖配置

> **注意**: 不同章节项目可能有不同的依赖版本要求，此步骤针对具体项目进行调整。

对于DriveTransformer项目，需要修改其requirements.txt以兼容Python 3.8:

```bash
# 编辑文件: chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer/requirements.txt

# 修改以下内容:
# numba==0.48.0        -> numba>=0.56.0
# numpy==1.21.1        -> numpy>=1.21.0,<1.25.0
```

### 步骤6: 安装具体章节项目

> **注意**: 每个章节项目需要单独安装，以下以第二章DriveTransformer为例。

#### 第二章: DriveTransformer 安装

```bash
# 进入项目目录
cd /home/lifanjie/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer

# 确保CUDA环境变量已设置
echo $CUDA_HOME  # 应显示: /usr/local/cuda-11.8

# 安装项目（使用--no-build-isolation以避免torch导入问题）
# 此步骤会编译MMCV的CUDA扩展，耗时约5-15分钟
pip install -e . --no-build-isolation
```

**安装过程中的注意事项**:
- 编译过程中可能长时间无输出，这是正常的
- 可以通过新终端运行 `ps aux | grep nvcc` 检查编译进程
- 不要中断安装过程，等待完成

#### 其他章节项目

如果有其他章节项目，按照各自项目的安装文档进行安装。通常步骤类似:

```bash
# 示例: 第三章项目（假设存在）
cd /home/lifanjie/shenlan_e2e/chapter3_xxx
pip install -e . --no-build-isolation
```

### 步骤7: 验证环境安装

```bash
# 验证所有关键组件
python -c "
import torch
import mmcv
print('='*50)
print('✅ 公共环境验证成功!')
print('='*50)
print(f'PyTorch: {torch.__version__}')
print(f'CUDA available: {torch.cuda.is_available()}')
print(f'CUDA version: {torch.version.cuda}')
print(f'MMCV: {mmcv.__version__}')
print(f'GPU: {torch.cuda.get_device_name(0)}')
print('='*50)
"

# 验证DriveTransformer模块（第二章特定）
python -c "import drivetransformer; print('✅ DriveTransformer (Chapter 2) installed successfully')"
```

**预期输出**:
```
==================================================
✅ 公共环境验证成功!
==================================================
PyTorch: 2.4.1+cu118
CUDA available: True
CUDA version: 11.8
MMCV: 0.0.1
GPU: NVIDIA GeForce RTX 3050
==================================================
✅ DriveTransformer (Chapter 2) installed successfully
```

---

## 📚 章节项目详情

### 第二章: BEV Encoder - DriveTransformer

**项目位置**: `chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer`

**项目简介**: 
DriveTransformer是一个基于统一Transformer架构的可扩展端到端自动驾驶框架，发表于ICLR 2025。该框架采用BEV（Bird's Eye View）编码器进行环境感知，实现了从传感器输入到控制输出的端到端学习。

**核心特性**:
- 🎯 统一的Transformer架构
- 🦅 BEV空间环境表示
- 🔄 可扩展的模块化设计
- 🏆 Bench2Drive闭环评估基准支持

#### 快速开始

```bash
# 1. 激活环境
source /home/lifanjie/shenlan_e2e/drivetransformer/bin/activate

# 2. 进入项目目录
cd /home/lifanjie/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer

# 3. 查看项目文档
cat docs/INSTALL.md      # 详细安装说明
cat docs/DATA_PREP.md    # 数据准备指南
cat docs/TRAIN_EVAL.md   # 训练和评估说明
```

#### 训练模型

```bash
# 单卡训练
bash adzoo/drivetransformer/dist_train.sh \
  adzoo/drivetransformer/configs/drivetransformer/drivetransformer_large.py 1

# 多卡训练（8卡）
bash adzoo/drivetransformer/dist_train.sh \
  adzoo/drivetransformer/configs/drivetransformer/drivetransformer_large.py 8
```

#### 评估模型

参考 `docs/TRAIN_EVAL.md` 中的开环和闭环评估流程。

#### 相关文档

- [INSTALL.md](chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer/docs/INSTALL.md) - 详细安装指南
- [DATA_PREP.md](chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer/docs/DATA_PREP.md) - 数据准备
- [TRAIN_EVAL.md](chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer/docs/TRAIN_EVAL.md) - 训练和评估
- [Bench2Drive](chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive) - 闭环评估基准

---

### 后续章节

> 待添加...

---

## ❓ 常见问题解答

### 公共环境问题

**Q1: CUDA版本不匹配错误**

**错误信息**: 
```
RuntimeError: The detected CUDA version (10.0) mismatches the version that was used to compile PyTorch (11.8)
```

**原因**: 系统CUDA Toolkit版本与PyTorch编译时使用的CUDA版本不一致。

**解决方案**: 按照"步骤4"安装CUDA 11.8 Toolkit并设置环境变量。

```bash
# 检查当前CUDA版本
nvcc --version

# 如果不是11.8，按照步骤4重新安装
export CUDA_HOME=/usr/local/cuda-11.8
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH
```

**Q2: GCC版本过高导致编译失败**

**错误信息**: 
```
Unsupported gpu architecture 'compute_86'
或
#error -- unsupported GNU version!
```

**原因**: CUDA 11.8只支持GCC 9-11，而Ubuntu 24.04默认是GCC 13。

**解决方案**: 安装GCC 9并设置为默认编译器。

```bash
# 安装GCC 9
sudo apt-get install -y gcc-9 g++-9

# 设置为默认
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 90
sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-9 90
sudo update-alternatives --set gcc /usr/bin/gcc-9
sudo update-alternatives --set g++ /usr/bin/g++-9

# 验证
gcc --version  # 应显示 9.5.0
```

**Q3: 编译过程长时间无输出**

**现象**: 执行 `pip install -e .` 后，终端长时间没有任何输出。

**原因**: MMCV的CUDA扩展正在后台编译，编译过程通常不会实时输出进度。

**解决方案**: 
1. **耐心等待**: 编译通常需要5-15分钟
2. **检查进程**: 在新终端运行以下命令确认编译正在进行
   ```bash
   ps aux | grep nvcc
   # 如果看到nvcc进程，说明编译正常进行
   ```
3. **不要中断**: 即使看起来"卡住"了，也不要Ctrl+C中断

**正常现象**: 
- CPU使用率高
- 内存占用增加
- nvcc进程在运行

**Q4: typing_extensions卸载失败**

**错误信息**: 
```
ERROR: Cannot uninstall 'typing_extensions'. It is a distutils installed project...
```

**原因**: pip无法安全卸载由distutils安装的包。

**解决方案**:

```bash
# 手动删除冲突的包信息
rm -rf drivetransformer/lib/python3.8/site-packages/typing_extensions-*.dist-info

# 重新安装
pip install -e . --no-build-isolation
```

**Q5: numba或numpy版本冲突**

**错误信息**: 
```
ModuleNotFoundError: No module named 'distutils.msvccompiler'
或
RuntimeWarning: NumPy X.X.X may not yet support Python 3.8
```

**原因**: requirements.txt中的版本与Python 3.8不兼容。

**解决方案**: 修改对应项目的requirements.txt文件。

```bash
# 对于DriveTransformer项目
# 编辑: chapter2_bev_encoder/home_work_v1/home_work/DriveTransformer/requirements.txt

# 修改:
# numba==0.48.0  ->  numba>=0.56.0
# numpy==1.21.1  ->  numpy>=1.21.0,<1.25.0
```

---

## 🛠️ 环境管理

### 日常使用

```bash
# 每次使用前激活环境
cd /home/lifanjie/shenlan_e2e
source drivetransformer/bin/activate

# 如果使用CUDA且未永久设置环境变量
export CUDA_HOME=/usr/local/cuda-11.8
export PATH=$CUDA_HOME/bin:$PATH
export LD_LIBRARY_PATH=$CUDA_HOME/lib64:$LD_LIBRARY_PATH

# 退出环境
deactivate
```

### 环境重置

如果环境出现问题，可以完全重置:

```bash
# 1. 删除虚拟环境
cd /home/lifanjie/shenlan_e2e
rm -rf drivetransformer

# 2. 重新创建环境
python3.8 -m venv drivetransformer
source drivetransformer/bin/activate

# 3. 重新安装（按照上述步骤2-7）
pip install --upgrade pip
pip install packaging cython wheel
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# ... 继续其他步骤
```

### 检查环境状态

```bash
# 检查当前Python版本
python --version

# 检查PyTorch和CUDA
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"

# 检查CUDA Toolkit
nvcc --version

# 检查GCC版本
gcc --version

# 检查已安装的包
pip list | grep -E "torch|mmcv|numpy|numba"
```

---

## 📖 学习资源

### 官方文档

- [DriveTransformer Paper](https://arxiv.org/abs/xxxx.xxxxx) - ICLR 2025论文
- [OpenMMLab](https://openmmlab.com/) - MMCV和MMDetection3D官方文档
- [CARLA Simulator](https://carla.org/) - 自动驾驶模拟器
- [Bench2Drive](https://github.com/ai4ce/Bench2Drive) - 闭环评估基准

### 相关教程

- PyTorch官方教程: https://pytorch.org/tutorials/
- CUDA编程指南: https://docs.nvidia.com/cuda/
- BEV感知综述: https://arxiv.org/abs/xxxx.xxxxx

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进本项目。

### 提交问题

1. 描述清楚问题现象
2. 提供错误日志
3. 说明环境配置（Python版本、PyTorch版本等）
4. 提供复现步骤

### 代码规范

- 遵循PEP 8 Python代码规范
- 添加必要的注释和文档字符串
- 保持代码简洁和可读性

---

## 📄 许可证

本项目仅供学习和研究使用。

---

## 📞 联系方式

如有问题，请通过以下方式联系:
- 提交GitHub Issue
- 发送邮件至: [your-email@example.com]

---

**最后更新**: 2026-04-11

ckpts:

https://drive.google.com/file/d/1wAXFWfjJm0cmP_pmgTkwxTUEs6Zu5j6i/view

https://huggingface.co/rethinklab/Bench2DriveZoo/blob/main/resnet50-19c8e357.pth

# 一定要在conda环境中运行
conda activate drivetransformer

# 调试用，实际仿真用不到
./CarlaUE4.sh -carla-rpc-port=30002 -vulkan -RenderOffScreen -nosound

(drivetransformer) root@9gpu-com:~/project/shenlan_e2e# python3 carla_record_video.py

./chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/start_eval_open_loop_wocontrol.sh
./chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/start_eval.sh

carla 程序
ps aux | grep -i carla | grep -v grep

清除carla
bash /root/project/shenlan_e2e/chapter2_bev_encoder/home_work_v1/home_work/Bench2Drive/tools/clean_carla.sh
清理相关carla占用端口
netstat -tuln | grep -E "30002|50001"
carla仿真失败，一个很重要的原因就是因为这个。


# 下载训练数据
./download_mini.sh