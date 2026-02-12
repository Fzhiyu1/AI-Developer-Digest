#!/bin/bash
set -e

echo "=== AI Daily Paper — 仓库研究 ==="

# 检查是否有推荐仓库
REPOS_FILE=$(ls -t data/*-repos.json 2>/dev/null | head -1)
if [ -z "$REPOS_FILE" ]; then
    echo "没有找到推荐仓库文件，跳过"
    exit 0
fi

echo "研究文件: $REPOS_FILE"
claude -p "$(cat prompts/RESEARCH.md)" --dangerously-skip-permissions
echo "=== 研究完成 ==="
