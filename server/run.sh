#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

# 检查 conda 环境
if [ -d "$HOME/miniconda3/envs/lowpower" ]; then
    source "$HOME/miniconda3/envs/lowpower/bin/activate"
elif command -v conda &>/dev/null && conda env list | grep -q lowpower; then
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate lowpower
fi

# 确保依赖安装
pip3 install -q -r requirements.txt --break-system-packages 2>/dev/null || pip3 install -q -r requirements.txt

# 启动服务
export DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY:-sk-fd59ba4f53954134ac48b08187b789b7}"
exec python3 -m uvicorn main:app --host 0.0.0.0 --port 8888 --reload
