#!/bin/bash
set -e

DATE=$(date +%Y-%m-%d)
echo "=== AI Daily Paper — $DATE ==="

# Step 1: 采集数据
echo "[Step 1] 采集数据..."
python -m collectors.runner
echo "[Step 1] 完成: data/$DATE.json"

# Step 2: Claude 分析 + 日报 + 仓库研究
echo "[Step 2] Claude 分析..."
claude -p "$(cat prompts/PROMPT.md)"
echo "[Step 2] 完成"

echo "=== 全部完成 ==="
