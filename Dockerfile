FROM python:3.11-slim

WORKDIR /app

# 安装 Claude Code CLI
RUN apt-get update && apt-get install -y curl git && \
    curl -fsSL https://claude.ai/install.sh | sh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目
COPY . .

# 安装 cron
RUN apt-get update && apt-get install -y cron && \
    apt-get clean && rm -rf /var/lib/apt/lists/*
COPY cron/daily.cron /etc/cron.d/daily
RUN chmod 0644 /etc/cron.d/daily && crontab /etc/cron.d/daily

RUN chmod +x scripts/run.sh

CMD ["cron", "-f"]
