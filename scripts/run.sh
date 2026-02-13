#!/bin/bash
set -e

# 失败时发送通知
trap 'bash /app/scripts/notify.sh "$(date +%Y-%m-%d)" "failed" "执行失败，检查日志"' ERR

# 加载环境变量（修复 cron 环境变量丢失）
if [ -f "/app/.env" ]; then
    set -a
    source /app/.env
    set +a
fi

DATE=$(date +%Y-%m-%d)
echo "=== AI Daily Paper — $DATE ==="

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

echo "=== 全部完成 ==="

# Step 4: 自动提交产出
echo "[Step 4] Git 提交..."
cd /app
git add reports/ repo-research/ CLAUDE.md 2>/dev/null || true
if git diff --cached --quiet; then
    echo "[Step 4] 无新改动"
else
    git commit -m "daily: AI Daily Paper — $DATE"
    if git remote get-url origin &>/dev/null; then
        git push origin main 2>/dev/null && echo "[Step 4] 已推送" || echo "[Step 4] 推送失败"
    fi
fi

# Step 5: 通知
bash scripts/notify.sh "$DATE" "success" "日报已生成"
