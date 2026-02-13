#!/bin/bash
# 执行结果通知（通用 Webhook）
DATE=$1
STATUS=$2
DETAIL=$3

NOTIFICATION_WEBHOOK="${NOTIFICATION_WEBHOOK:-}"
if [ -z "$NOTIFICATION_WEBHOOK" ]; then
    echo "[Notify] 未配置 NOTIFICATION_WEBHOOK，跳过"
    exit 0
fi

curl -s -X POST -H 'Content-Type: application/json' \
    -d "{\"date\":\"$DATE\",\"status\":\"$STATUS\",\"detail\":\"$DETAIL\"}" \
    "$NOTIFICATION_WEBHOOK" || echo "[Notify] 发送失败"
