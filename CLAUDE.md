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

**数据源质量评估**：
- HackerNews：高质量 AI 讨论，但需过滤非 AI 话题（隐私法规、硬件、游戏引擎等）
- GitHub Trending：官方项目（Google、Chrome、GitHub）质量高，小项目需评估实际价值
- TechCrunch/The Verge：行业新闻可靠，但需合并跨源重复报道
- Hugging Face：模型发布频繁，优先选择高 likes 和知名团队
- Reddit r/LocalLLaMA：社区热度高，反映真实用户关注点
- ArXiv：论文量大，优先选择 Agent、多模态、评估基准相关
- Product Hunt：噪音较多，需严格筛选 AI 相关且有实际价值的产品

**有效过滤规则**：
- 跨源去重：同一事件在多个来源出现时合并，标注所有来源
- AI 相关性：严格过滤纯硬件、隐私法规、游戏、加密货币等边缘话题
- 质量门槛：Product Hunt 无描述或描述模糊的产品直接跳过

### 趋势追踪

**2026-02-12 观察到的热点趋势**：

1. **中国 AI 模型爆发**：GLM-5（智谱）和 MiniMax 2.5 同日发布，标志着中国从对话模型转向 Agent 工作流，且 GLM-5 完全在华为芯片上训练，打破 NVIDIA 依赖

2. **Agent 能力评估成为焦点**：多篇论文聚焦 Agent 评估（CLI-Gym、GameDevBench、FormalJudge），反映行业从"能做什么"转向"如何评估和监督"

3. **MCP（Model Context Protocol）生态扩展**：Chrome DevTools MCP 发布，显示主流工具开始原生支持 AI Agent 集成

4. **AI 公司组织动荡**：OpenAI 解散任务对齐团队、xAI 大量核心成员离职，反映行业快速扩张带来的管理挑战

5. **AI 基础设施成本问题凸显**：Anthropic 承诺覆盖电价上涨、Z.ai 公开表示 GPU 短缺，算力和能源成为制约因素

6. **法律/医疗等专业领域突破**：GPT-5 超越联邦法官、LiveMedBench 医疗基准发布，AI 开始在高门槛专业领域超越人类

**持续关注项目**：
- GLM 系列（智谱 AI）：开源 MoE 架构领导者
- MCP 生态：Chrome、GitHub 等主流工具的 Agent 集成
- Claude Code 质量争议：社区反馈模型"降智"，需持续观察

### 执行日志

**2026-02-12**：
- 采集条目：200+ 条原始数据
- 过滤后：150+ 条 AI 相关
- 日报亮点：GLM-5 发布（中国 MoE 突破）、GPT-5 超越法官（专业领域突破）、xAI 人才流失（行业动荡）
- 推荐仓库：5 个（Google langextract、Chrome DevTools MCP、AI Engineering Hub、GitHub Agentic Workflows、Claude Code 插件）
- 关键发现：中国 AI 公司集中发力 Agent 工作流，MCP 生态快速扩展，AI 基础设施成本成为行业焦点
