#!/bin/bash
set -e

# 加载环境变量（修复 cron 环境变量丢失）
if [ -f "/app/.env" ]; then
    set -a
    source /app/.env
    set +a
fi

DATE=$(date +%Y-%m-%d)
echo "=== AI Daily Paper [TEST] — $DATE ==="

# 清理今日已有产出，确保全链路重新生成
echo "[清理] 删除今日已有文件..."
rm -f "data/$DATE.json" "data/$DATE-slim.json"
rm -f "data/$DATE-repos.json"
rm -f "reports/$DATE.md"
rm -rf "repo-research/$DATE"
echo "[清理] 完成"

# Step 1: 采集数据
echo "[Step 1] 采集数据..."
python -m collectors.runner
echo "[Step 1] 完成: data/$DATE.json + data/$DATE-slim.json"

# Step 2: Claude 分析 + 日报
echo "[Step 2] Claude 分析..."
claude -p "$(cat prompts/PROMPT.md)" --model claude-opus-4-6 --dangerously-skip-permissions
echo "[Step 2] 完成"

# Step 3: 仓库深度研究（并行）
echo "[Step 3] 仓库研究..."
bash scripts/research.sh
echo "[Step 3] 完成"

echo "=== 全部完成 [TEST] ==="
