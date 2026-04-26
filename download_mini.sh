#!/bin/bash

# 国内加速镜像
export HF_ENDPOINT=https://hf-mirror.com

# 安装依赖
if ! python -m pip show huggingface-hub > /dev/null 2>&1; then
  echo "Installing huggingface-hub..."
  python -m pip install -U huggingface-hub -i https://mirrors.aliyun.com/pypi/simple/
fi

# 登录
echo "=== 登录 HuggingFace ==="
hf auth login

mkdir -p Bench2Drive-mini

# 下载列表
files=(
"HardBreakRoute_Town01_Route30_Weather3.tar.gz"
"DynamicObjectCrossing_Town02_Route13_Weather6.tar.gz"
"Accident_Town03_Route156_Weather0.tar.gz"
"YieldToEmergencyVehicle_Town04_Route165_Weather7.tar.gz"
"ConstructionObstacle_Town05_Route68_Weather8.tar.gz"
"ParkedObstacle_Town10HD_Route371_Weather7.tar.gz"
"ControlLoss_Town11_Route401_Weather11.tar.gz"
"AccidentTwoWays_Town12_Route1444_Weather0.tar.gz"
"OppositeVehicleTakingPriority_Town13_Route600_Weather2.tar.gz"
"VehicleTurningRoute_Town15_Route443_Weather1.tar.gz"
)

# 循环下载（修复版 hf 命令）
for file in "${files[@]}"; do
  echo "===================================="
  echo "正在下载: $file"
  
  hf download \
    --repo-type dataset \
    --include "$file" \
    --local-dir Bench2Drive-mini \
    rethinklab/Bench2Drive
done

echo ""
echo "✅ 全部下载完成！"
echo "📂 保存路径: ./Bench2Drive-mini/"