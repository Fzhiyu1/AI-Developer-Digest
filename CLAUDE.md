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

**2026-02-15 观察到的热点趋势**：

1. **OpenAI 安全承诺系统性瓦解**：从使命宣言删除"safely"（HN 338 分）+ 任务对齐团队解散（02-12）+ 政策高管被解雇 + AI 安全领导者辞职转行。四个独立事件在一周内形成完整叙事链，OpenAI 的安全优先级正经历从人事到话语体系的全面降级

2. **AI 从推理跨入科学发现**：GPT-5.2 在理论物理中推导出新结果（HN 384 分），这是大模型首次产出原创性科学发现而非复现已知结论。如果经同行评审验证，将重新定义 AI 在基础研究中的角色

3. **学术诚信遭遇 AI 攻击**：ICML 审稿论文中发现大规模 prompt injection（Reddit 331 分），嵌入文本试图操纵 LLM 审稿工具。学术审稿系统的信任基础正在被动摇

4. **Agent 失控事件进入行业反思阶段（第三天）**：02-13 的 Agent 攻击性文章事件持续发酵，受害者发布后续（HN 207 分），评论文章将讨论从个案升级为行业反思（HN 189 分）。OpenAI 同日移除因谄媚引发诉讼的 GPT-4o 版本

5. **中国模型采用瓶颈突破**：GLM-5 下载量从 1,548 暴涨至 13,875（+795%），02-13 日报指出的"likes 增长但下载停滞"困境在两天内被打破。MiniMax-M2.5 权重正式上线 HF（344 likes，75 下载）

6. **开源与闭源智能差距创历史新低**：Reddit 讨论（224 分）+ SWE-rebench 1 月结果（195 分），GLM-5 和 Opus 4.6 同台竞技，开源权重模型正在快速缩小与闭源模型的差距

7. **基准可信度危机**：RLVR 训练数据检测论文 + Benchmark Health Index 元评估框架 + ICML prompt injection 事件，三条线索指向同一问题——AI 评估体系本身需要被评估

**持续关注项目**：
- GLM-5：下载量 1,548→13,875（+795%），采用瓶颈突破，继续观察增长曲线
- MiniMax M2.5：权重已上线 HF（75 下载），SWE-Bench 80.2%，观察采用加速
- THUDM/slime：4,095 stars，GLM 团队 RL Scaling 框架，v0.2.2 活跃开发
- Kimi-K2.5：685K 下载（+5.9%），持续领跑 HF 热门模型
- Agent 安全研究：从学术论文（02-13）到现实事件反思（02-14），形成完整闭环
- OpenAI 安全退化：使命宣言 + 团队解散 + 人事变动，持续追踪后续影响
- SynkraAI/aios-core：447 stars，AI 编排全栈开发，新方向
- Cohere IPO：$240M ARR，企业 AI 赛道商业化验证

### 执行日志

**2026-03-16**：
- 采集条目：123 条原始数据，去重后 121 条
- 日报亮点：Claude Code 仿冒搜索结果、Agent 红队 playground、ByteDance 暂停 Seedance 2.0、即兴演员训练情绪 AI、Spotify AI DJ 口碑反噬
- 推荐仓库：5 个（shareAI-lab/learn-claude-code、shanraisshan/claude-code-best-practice、abhigyanpatwari/GitNexus、topoteretes/cognee、voidzero-dev/vite-plus）
- 趋势判断：Agent 工程开始从“能力展示”转向“安全、上下文管理、工作流方法论”；AI coding 生态明显进入 best practice 沉淀阶段；本地/开源工具仍在以成本和可控性吸引开发者
- 过滤经验：今天 HN 上高热的机器学习可视化教程、LLM 架构图谱有参考价值，但更适合作为背景信号而非主新闻；Product Hunt 里安全、memory、local-first 方向质量明显高于泛 AI 包装产品


**2026-02-14**：
- 采集条目：169 条原始数据，去重后 167 条
- 过滤后：约 100 条 AI 相关（严格过滤隐私法规、Ring 监控、Meta 面部识别等边缘话题）
- 日报亮点：GPT-5.2 物理新发现（HN 384 分）、OpenAI 删除"safely"（HN 338 分）、ICML prompt injection（Reddit 331 分）、GLM-5 下载暴涨 9 倍、MiniMax-M2.5 权重上线
- 推荐仓库：4 个（THUDM/slime 4.1K、SynkraAI/aios-core 447、google-deepmind/superhuman 388、cheahjs/free-llm-api-resources 10.7K）
- 深挖工具使用：并行查询 GitHub API（5 个项目）、HF 模型元数据（6 个模型）、ArXiv 论文摘要（8 篇）
- 关键发现：GLM-5 采用瓶颈突破（下载 +795%），OpenAI 安全承诺系统性瓦解（四事件一周内形成叙事链），基准可信度危机（三条独立线索汇聚），开源闭源差距创新低
- 跨天去重：排除 02-12/02-13 已报道论文（AIR、AgentLeak、When Agents Disagree、Voxtral Realtime 等）、已推荐仓库（AionUi、rowboat、claude-skills、Personal_AI_Infrastructure 等 8 个）；Agent 失控事件作为延续报道处理；prev_seen 标记的 HF 模型仅在有数据变化时报道
- 执行环境：系统 python3 + PYTHONPATH=/app，ArXiv API 频繁限流需等待

**2026-02-13**：
- 采集条目：175 条原始数据，去重后 174 条
- 过滤后：约 120 条 AI 相关（严格过滤边缘话题）
- 日报亮点：AI Agent 失控双事件（HN 1,626 + 877 分）、Gemini 3 Deep Think（762 分）、GPT-5.3-Codex-Spark（637 分）、Spotify 承认 AI 完全替代编码、Anthropic 300 亿 Series G
- 推荐仓库：4 个（AionUi 15.5K、rowboat 5.3K、claude-skills 1.8K、Personal_AI_Infrastructure 7.6K）
- 深挖工具使用：并行查询 GitHub API（5 个项目）、HF 模型元数据（7 个模型）、ArXiv 论文摘要（8 篇）
- 关键发现：Agent 失控事件与安全论文同日共振（现实+学术），Claude Code 生态工具繁荣，GLM-5 likes +35% 但下载停滞，Voxtral Realtime 开创流式 ASR 赛道
- 跨天去重：排除 02-12 已报道论文（CLI-Gym、GameDevBench、FormalJudge）、已推荐仓库（gh-aw、chrome-devtools-mcp、hive、langextract）；Anthropic 融资作为延续报道处理；Product Hunt 质量不达标整节省略
- 执行环境：.venv Python 3.14 在 sandbox 中不可执行，改用系统 python3 + PYTHONPATH=/app

**2026-02-12**：
- 采集条目：191 条原始数据，去重后 190 条
- 过滤后：约 150 条 AI 相关（严格过滤边缘话题）
- 日报亮点：Claude Code 质量争议（HN 972 分最热）、中国 AI 集中发力 Agent（GLM-5 + MiniMax 2.5 同日发布）、GPT-5 超越法官（专业领域突破）、xAI 人才流失（9 人含 2 联创）、OpenAI 解散对齐团队
- 推荐仓库：4 个（GitHub gh-aw v0.43.7 今日发布、Chrome DevTools MCP v0.17.0 活跃开发、Hive 1 月获 7K+ stars、Google langextract 30K+ stars）
- 深挖工具使用：并行查询 GitHub API（4 个项目）、HF 模型元数据（4 个模型）、ArXiv 论文摘要（3 篇必查），显著提升日报分析深度
- 关键发现：Claude Code 质量争议成最热话题（972 分远超其他），中国 AI 从对话转向 Agent 工作流（GLM-5 华为芯片训练），MCP 生态快速扩展（GitHub/Chrome 官方入局），Agent 评估成论文焦点（CLI-Gym、GameDevBench、FormalJudge），垂直场景模型需求更强（GLM-OCR 597K 下载 vs GLM-5 1.5K）
- 执行优化：使用 subagent 并行深挖工具调用，节省时间；严格遵守数量上限（今日要闻 5 条、其他分类 3 条）；数据概览直接引用 _meta 字段精确统计
