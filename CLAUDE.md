# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

AI Daily Paper — AI 领域自动化信息采集与知识沉淀系统。通过 Docker 容器定时调度 Claude Code CLI，每日自动采集 AI 动态、生成结构化日报、深度分析 GitHub 仓库。

## 架构

Docker 容器（cron 调度）→ 数据采集（8 源）→ Claude Code CLI（日报 + 推荐仓库）→ 并行仓库研究

三步流水线（`scripts/run.sh`）：
1. **数据采集** — 8 个 Python 采集器并行拉取，输出 full + slim 双 JSON
2. **日报生成** — Claude Code CLI 读取 slim JSON，生成 Markdown 日报 + 推荐仓库列表
3. **仓库研究** — 并行启动多个 Claude 实例，通过 GitHub API 深度分析每个推荐仓库

## 关键路径

- `prompts/PROMPT.md` — 日报生成指令（分类、筛选、格式），修改此文件影响日报生成的全部行为
- `prompts/RESEARCH.md` — 仓库研究指令（7 个分析维度，含应用方向分析）
- `collectors/runner.py` — 采集入口，管理 8 个源的调度、重试、去重、输出
- `collectors/utils.py` — 公共工具（fetch_url、parse_rss、make_id 等）
- `scripts/run.sh` — Docker 容器内的每日执行入口（采集 → 日报 → 研究）
- `scripts/research.sh` — 仓库研究脚本（并行 Claude 实例 + GitHub API）

## 数据源

HackerNews、GitHub Trending、TechCrunch、The Verge、Hugging Face、Reddit、ArXiv、Product Hunt

## 产出

- `data/YYYY-MM-DD.json` — 完整采集数据
- `data/YYYY-MM-DD-slim.json` — 精简版（喂给 Claude）
- `data/YYYY-MM-DD-repos.json` — 推荐仓库列表
- `reports/YYYY-MM-DD.md` — AI 日报
- `repo-research/YYYY-MM-DD/*.md` — 仓库深度研究报告

## 开发

```bash
# 测试
.venv/bin/python -m pytest tests/ -q

# 本地采集
.venv/bin/python -m collectors.runner

# Docker 全链路
docker compose build
docker compose run --rm daily-paper bash scripts/run.sh

# 单独跑仓库研究
docker compose run --rm daily-paper bash scripts/research.sh
```

## 环境变量

- `ANTHROPIC_AUTH_TOKEN` — 必需，Claude Code CLI 认证
- `ANTHROPIC_BASE_URL` — 可选，API 代理地址
- `GITHUB_TOKEN` — 可选，避免 GitHub API 限流

---

## Agent 记忆（自动维护，勿手动清空）

以下内容由每日执行的 Agent 自动更新，用于积累经验和追踪趋势。

### 搜索策略

（Agent 会在此记录有效的搜索关键词、数据源质量评估、过滤规则等）

### 趋势追踪

（Agent 会在此记录近期 AI 领域热点趋势、持续关注的项目/话题）

### 执行日志

（Agent 会在此记录最近几次执行的摘要，便于发现模式和调整策略）
