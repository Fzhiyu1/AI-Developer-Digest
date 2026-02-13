#!/bin/bash
set -e

echo "=== AI Daily Paper — 仓库研究 ==="

DATE=$(date +%Y-%m-%d)
REPOS_FILE=$(ls -t data/*-repos.json 2>/dev/null | head -1)
if [ -z "$REPOS_FILE" ]; then
    echo "没有找到推荐仓库文件，跳过"
    exit 0
fi

echo "研究文件: $REPOS_FILE"
mkdir -p "repo-research/$DATE"

# 读取每个仓库，并行启动 Claude 研究
PIDS=()
REPOS=$(python3 -c "
import json
with open('$REPOS_FILE') as f:
    for r in json.load(f):
        print(r['repo'])
")

for REPO in $REPOS; do
    SAFE_NAME=$(echo "$REPO" | tr '/' '-')
    OUTPUT="repo-research/$DATE/$SAFE_NAME.md"
    echo "启动研究: $REPO"

    # 读取研究规范
    RESEARCH_SPEC=$(cat prompts/RESEARCH.md)

    # 构建 prompt：已有报告则增量更新，否则全新生成
    if [ -f "$OUTPUT" ]; then
        PROMPT="仓库 $REPO 已有研究报告：$OUTPUT

请先读取该报告，然后通过 GitHub API 查询最新数据：
- curl https://api.github.com/repos/$REPO
- curl https://api.github.com/repos/$REPO/commits?per_page=5

对比已有报告，补充新发现（新版本、新功能、star 变化、近期提交等）。
在报告末尾追加「## 更新记录」章节，标注日期和新发现。
如果没有显著变化，简要说明即可。

以下是研究规范，更新时同样遵守：
$RESEARCH_SPEC

将更新后的完整报告写回 $OUTPUT"
    else
        PROMPT="研究 GitHub 仓库 $REPO，使用 GitHub API（不要 clone）获取信息。

请通过以下方式收集信息：
- curl GitHub API: https://api.github.com/repos/$REPO
- curl README: https://raw.githubusercontent.com/$REPO/main/README.md (或 master)
- curl 目录结构: https://api.github.com/repos/$REPO/git/trees/main?recursive=1
- curl 最近提交: https://api.github.com/repos/$REPO/commits?per_page=10

$RESEARCH_SPEC

输出报告到 $OUTPUT"
    fi

    claude -p "$PROMPT" --model claude-opus-4-6 --dangerously-skip-permissions &

    PIDS+=($!)
done

echo "等待 ${#PIDS[@]} 个研究任务完成..."
FAIL=0
for PID in "${PIDS[@]}"; do
    wait "$PID" || ((FAIL++))
done

echo "=== 研究完成 (${#PIDS[@]} 个仓库, $FAIL 个失败) ==="
