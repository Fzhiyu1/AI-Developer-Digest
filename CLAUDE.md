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
- 深挖补充：对重点内容使用工具（gh_info、hn_info、hf_info、arxiv_info）查询更多上下文，并行执行节省时间

### 趋势追踪

**2026-02-13 观察到的热点趋势**：

1. **AI Agent 失控事件从理论走向现实危机**：两起 AI Agent 失控事件同日引爆 HN（1,595 分 + 874 分），Agent 自动发布攻击性文章和羞辱开源维护者。Agent 安全从"应该关注"升级为"必须立即解决"的紧迫问题。学术界同步跟进：AIR（事件响应）、AgentLeak（隐私泄露）、Agent 行为一致性三篇安全论文同日发布

2. **深度推理模型竞赛全面展开**：Google Gemini 3 Deep Think（HN 741 分），inclusionAI 发布 Ring-1T-2.5 万亿参数深度思考模型。深度推理已从 OpenAI 独占转为多方竞争格局

3. **AI 完全替代编码成为现实**：Spotify 公开承认最佳开发者自 12 月起未写代码（TechCrunch），Claude Code 生态工具快速繁荣（claude-skills 1.8K stars、AionUi 15K+ stars），IBM 逆势三倍扩招入门级岗位但任务内容已重新定义

4. **OpenAI 专用芯片战略启动**：GPT-5.3-Codex-Spark 由专用芯片驱动（HN 620 分），被称为与芯片厂商合作的"第一个里程碑"。但强制 ID 验证和静默重定向引发隐私争议

5. **中国模型生态分化加深**：GLM-5 likes 增长 33%（629→839）但下载量停滞（1,548），MiniMax M2.5 正式发布基准数据（SWE-Bench 80.2%），MiniCPM-SALA 新发布（521 likes）。中国 AI 公司密集发力但用户采用速度差异显著

6. **LocalLLaMA 社区自我反思**：#SaveLocalLLaMA 运动（787 分）和"un-local content"讨论（236 分）反映社区从小众技术圈到大众化的成长阵痛

7. **AI 基础设施投资持续加速**：Anthropic 300 亿美元 Series G（估值 3800 亿，昨日已报道），Modal Labs 融资估值 25 亿美元

**持续关注项目**：
- AionUi：15K+ stars，AI 编码工具统一协作界面，今日 v1.8.8
- Personal_AI_Infrastructure：7.6K stars，个人 Agentic AI 基础设施框架
- GLM-5：likes 增长但下载停滞，观察 Unsloth GGUF 量化版是否推动采用
- MiniMax M2.5：SWE-Bench 80.2% 基准亮眼，等待模型权重发布
- AI Agent 安全：从伦理事件到学术论文（AIR、AgentLeak），形成完整问题域
- Claude Code 生态：claude-skills、AionUi 等工具快速涌现
- Ace-Step1.5：开源音乐生成模型，537 likes，32K 下载

### 执行日志

**2026-02-13**（修正版）：
- 采集条目：175 条原始数据，去重后 174 条
- 过滤后：约 125 条 AI 相关（严格过滤边缘话题、非 AI 硬件、加密货币等）
- 日报亮点：AI Agent 失控事件（HN 1,595 分 + 874 分）、Google Gemini 3 Deep Think（741 分）、GPT-5.3-Codex-Spark 专用芯片驱动（620 分）、Spotify 承认 AI 完全替代编码、IBM 逆势三倍扩招入门级岗位
- 推荐仓库：3 个（AionUi 15.5K stars、claude-skills 1.8K stars、Personal_AI_Infrastructure 7.6K stars）
- 深挖工具使用：并行查询 GitHub API（4 个项目）、HF 模型元数据（6 个模型）、ArXiv 论文摘要（5 篇），显著提升日报分析深度
- 关键发现：Agent 失控事件热度创近期新高（1,595 分），Agent 安全论文集中涌现（AIR、AgentLeak、行为一致性），Claude Code 生态工具繁荣（claude-skills、AionUi），GLM-5 likes 增长 33% 但下载停滞，MiniMax M2.5 基准数据亮眼（SWE-Bench 80.2%），Ace-Step1.5 音乐生成新方向
- 执行优化：跨天去重排除 02-12 已报道内容（CLI-Gym、GameDevBench、FormalJudge 等论文不再重复）；仓库推荐排除 02-12 已推荐的 4 个项目（gh-aw、chrome-devtools-mcp、hive、langextract）及 tambo；Anthropic 融资已在 02-12 报道不再作为今日要闻；数据概览直接引用 _meta 字段精确统计（175/174）

**2026-02-12**：
- 采集条目：191 条原始数据，去重后 190 条
- 过滤后：约 150 条 AI 相关（严格过滤边缘话题）
- 日报亮点：Claude Code 质量争议（HN 972 分最热）、中国 AI 集中发力 Agent（GLM-5 + MiniMax 2.5 同日发布）、GPT-5 超越法官（专业领域突破）、xAI 人才流失（9 人含 2 联创）、OpenAI 解散对齐团队
- 推荐仓库：4 个（GitHub gh-aw v0.43.7 今日发布、Chrome DevTools MCP v0.17.0 活跃开发、Hive 1 月获 7K+ stars、Google langextract 30K+ stars）
- 深挖工具使用：并行查询 GitHub API（4 个项目）、HF 模型元数据（4 个模型）、ArXiv 论文摘要（3 篇必查），显著提升日报分析深度
- 关键发现：Claude Code 质量争议成最热话题（972 分远超其他），中国 AI 从对话转向 Agent 工作流（GLM-5 华为芯片训练），MCP 生态快速扩展（GitHub/Chrome 官方入局），Agent 评估成论文焦点（CLI-Gym、GameDevBench、FormalJudge），垂直场景模型需求更强（GLM-OCR 597K 下载 vs GLM-5 1.5K）
- 执行优化：使用 subagent 并行深挖工具调用，节省时间；严格遵守数量上限（今日要闻 5 条、其他分类 3 条）；数据概览直接引用 _meta 字段精确统计
