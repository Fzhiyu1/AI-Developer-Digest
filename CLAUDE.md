# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

AI Daily Paper — AI 领域自动化信息采集与知识沉淀系统。通过 Docker 容器定时调度 Claude Code CLI，每日自动采集 AI 动态、生成结构化日报、深度分析 GitHub 仓库。

## 架构

Docker 容器（cron 调度）→ Claude Code CLI（执行 prompts/PROMPT.md）→ 产出报告 + 仓库研究 + 更新 Agent 记忆

两个核心模块：
1. **日报生成** — Claude Code CLI 执行多源搜索、分类、生成 Markdown 日报，触发周报/月报/年报汇总
2. **仓库研究** — Python 脚本从日报提取 GitHub 链接，clone 仓库并分析技术栈/活跃度/架构

## 关键路径

- `prompts/PROMPT.md` — Agent 完整执行流程（8 步），修改此文件影响日报生成的全部行为
- `agent/AGENT.md` — Agent 自维护的记忆文件（搜索策略、关键词库、趋势追踪），每次执行后自动更新，**不要手动清空**
- `repo-research/scripts/repo_research.py` — 仓库研究脚本（Python 3.9+），唯一的代码文件
- `scripts/run.sh` — Docker 容器内的每日执行入口

## 项目管理

- **计划追踪**：`docs/plans/ProjectPlan/` — 基于 AgentPlan 方法论的 Sprint 驱动计划系统，入口为 `INDEX.md`
- **技术探索**：`docs/exploration/` — 话题驱动的调研文档，记录方案对比和决策过程

## 环境变量

- `ANTHROPIC_API_KEY` — 必需
- `GITHUB_TOKEN` — 可选，避免 GitHub API 限流
