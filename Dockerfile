FROM python:3.11-slim

WORKDIR /app

# 系统依赖 + Node.js (Claude Code CLI 需要)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git cron ca-certificates gnupg && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_20.x nodistro main" > /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && apt-get install -y nodejs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Claude Code CLI
RUN npm install -g @anthropic-ai/claude-code

# Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 非 root 用户 (Claude CLI 禁止 root + skip-permissions)
RUN useradd -m -s /bin/bash appuser && chown -R appuser:appuser /app

# 复制项目
COPY --chown=appuser:appuser . .

# Cron 调度
COPY cron/daily.cron /etc/cron.d/daily
RUN chmod 0644 /etc/cron.d/daily && crontab -u appuser /etc/cron.d/daily

RUN chmod +x scripts/run.sh

USER appuser

# Git 配置（必须在 USER appuser 之后，写入 appuser 的 home）
RUN git config --global user.email "daily-paper@ai.local" && \
    git config --global user.name "AI Daily Paper"

CMD ["cron", "-f"]
