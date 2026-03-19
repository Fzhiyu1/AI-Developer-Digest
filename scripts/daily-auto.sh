#!/bin/bash
set -e

cd /home/fzhiyu/.openclaw/workspace/AI-Developer-Digest

DATE=$(date +%Y-%m-%d)
echo "=== AI Daily Digest Auto Run - $DATE ==="

# Step 1: 采集数据
echo "[1/4] 数据采集..."
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
PYTHONPATH=. .venv/bin/python -m collectors.runner

# Step 2: 生成日报（通过 OpenClaw 调用我）
echo "[2/4] 生成日报..."
openclaw agent --session-id main --message "生成今天的 AI 开发者日报，读取 ~/.openclaw/workspace/AI-Developer-Digest/data/$DATE-slim.json，分析后写入 reports/$DATE.md" || echo "生成失败，跳过"

# Step 3: Git 提交
echo "[3/4] Git 提交..."
git add reports/ data/ 2>/dev/null || true
if ! git diff --cached --quiet; then
    git commit -m "AI Daily Digest $DATE"
    git push origin main 2>/dev/null || echo "推送失败"
fi

# Step 4: 发送到飞书
echo "[4/4] 发送到飞书..."
openclaw agent --session-id main --message "使用 message 工具发送 /home/fzhiyu/.openclaw/workspace/AI-Developer-Digest/reports/$DATE.md 给 user:ou_efe1b2383ca847d3a87ae3d66087aab7，channel=feishu，accountId=main；如果还有 /home/fzhiyu/.openclaw/workspace/AI-Developer-Digest/repo-research/$DATE/ 下的 .md 文件，也逐个发送，全部都明确使用 accountId=main" || echo "发送失败"

echo "=== 完成 ==="
