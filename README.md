# DriveTransformer 项目

## 系统环境配置

### 操作系统
- **Ubuntu版本**: Ubuntu 24.04.3 LTS (Noble Numbat)

### Python环境
- **推荐Python版本**: Python 3.9 或 Python 3.10（深度学习主流选择）
- **当前Python版本**: Python 3.10.20 ✅
- **虚拟环境**: drivetransformer (使用venv创建，Python 3.10)

### CUDA与深度学习框架
- **CUDA版本**: CUDA 12.8 (系统) / CUDA 12.1 (PyTorch)
- **NVIDIA驱动版本**: 570.211.01
- **PyTorch版本**: 2.5.1+cu121 ✅
- **xformers版本**: 0.0.28.post3 ✅
- **GPU设备**: NVIDIA GeForce RTX 3050

### 编译器
- **GCC版本**: GCC 13.3.0 (Ubuntu 13.3.0-6ubuntu2~24.04.1)

## 环境安装

### 1. 创建虚拟环境

```bash
# 使用Python 3.10创建虚拟环境
python3.10 -m venv drivetransformer

# 激活虚拟环境
source drivetransformer/bin/activate
```

### 2. 升级pip

```bash
pip install --upgrade pip
```

### 3. 安装PyTorch和xformers

```bash
# 安装PyTorch (CUDA 12.1)
pip install torch==2.5.1+cu121 torchvision==0.20.1+cu121 torchaudio==2.5.1+cu121 --index-url https://download.pytorch.org/whl/cu121

# 安装xformers（与PyTorch 2.5.1兼容的版本）
pip install xformers==0.0.28.post3
```

**注意**: 虽然系统CUDA版本是12.8，但PyTorch官方目前最高支持到cu121（CUDA 12.1），这通常是向下兼容的。

### 4. 验证安装

```bash
# 验证PyTorch安装
python -c "import torch; print(f'PyTorch版本: {torch.__version__}'); print(f'CUDA可用: {torch.cuda.is_available()}'); print(f'CUDA版本: {torch.version.cuda}')"
```

### 5. 安装其他依赖（根据项目需求）

```bash
# 示例：安装常用深度学习库
pip install numpy pandas matplotlib opencv-python
pip install transformers accelerate
pip install tqdm pyyaml
```

## 环境激活

```bash
# 激活虚拟环境
source drivetransformer/bin/activate

# 退出虚拟环境
deactivate
```

## 下一步

请根据项目需求安装必要的依赖包，例如：
```bash
pip install torch torchvision torchaudio
```
