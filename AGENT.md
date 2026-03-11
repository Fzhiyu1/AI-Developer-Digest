# Agent 记忆与策略文件

> 本文件是 Agent 的持久化记忆。每次执行任务时先读取本文件，执行完毕后更新本文件。

## 项目结构

```
Ai-Daily-Paper/
├── AGENT.md           # 本文件 — Agent 记忆与策略
├── PROMPT.md          # 定时任务驱动提示词
├── START.md           # 定时任务启动提示词
├── index.md           # 报告总索引
├── README.md          # 项目说明
└── reports/
    ├── daily/         # 日报（YYYY-MM-DD.md）
    ├── weekly/        # 周报（YYYY-W{周数}.md）
    ├── monthly/       # 月报（YYYY-MM.md）
    └── yearly/        # 年报（YYYY.md）
```

## 搜索策略

### 信息源优先级

| 优先级 | 信息源 | 覆盖领域 | 备注 |
|--------|--------|----------|------|
| P0 | GitHub Trending | 开源项目 | 每日必查 |
| P0 | Hacker News | 综合新闻 | 每日必查 |
| P0 | Twitter/X AI 圈 | 实时动态 | 每日必查 |
| P1 | TechCrunch / The Verge | 行业新闻 | 每日必查 |
| P1 | Hugging Face | 模型/数据集 | 每日必查 |
| P1 | Product Hunt | 新产品 | 每日必查 |
| P2 | ArXiv (cs.AI, cs.CL, cs.LG) | 论文 | 有重大论文时关注 |
| P2 | Reddit (r/MachineLearning, r/LocalLLaMA) | 社区讨论 | 补充信息 |

### 关键词库

**核心关键词：**
- AI news today, 人工智能 今日新闻
- new AI open source project
- AI breakthrough
- LLM red team 0-day, LLM 漏洞披露
- github trending rss, GitHub Trending RSS
- 国内大模型动态, 国内 AI 模型发布
- DeepSeek, DeepSeek 发布, DeepSeek 模型
- 智谱, Zhipu, GLM, GLM-4, GLM-5, GLM 更新
- MiniMax, MiniMax 发布
- 通义千问, Qwen, 阿里云 通义
- 百度, 文心, ERNIE
- 字节, 豆包, 火山方舟
- 腾讯, 混元
- OpenAI News RSS, OpenAI acquisition
- Anthropic lawsuit Pentagon supply chain risk
- TechCrunch AI RSS, site:techcrunch.com 2026/03 AI
- huggingface papers trending githubStars

**自进化智能体：**
- self-evolving agent, recursive self-improvement
- 自进化智能体, AI agent framework
- meta-learning agent, agent-to-agent collaboration
- autonomous agent, self-improving AI
- agent teams, multi-agent coding
- Agent HQ, Codex agent
- Model Context Protocol, MCP server
- Developer Knowledge API
- agentic coding, coding agent toolchain
- skills catalog, agent memory plugin
- async agents, async agent workflows
- agentic workflows, agentic security
- Firefox security vulnerabilities, AI red team

**智能穿戴硬件：**
- AI wearable, AI glasses, AI earbuds
- 智能穿戴 AI, AI Pin, AI ring
- on-device LLM, edge AI hardware
- brain-computer interface consumer
- OpenAI hardware timeline, OpenAI io branding
- Qwen-Image-2.0
- Siri AI overhaul iOS 26.5
- MCP agent server

### 搜索优化记录

> 每次执行后，Agent 在此记录搜索效果和改进建议。
> 格式：`[日期] 发现/问题/改进`

[2026-02-06] 发现 OpenAI/Anthropic/GitHub 官方博客是最可靠的当日发布源；GitHub Trending 页面抓取受限，需使用 github-trending.today 作为备用；Product Hunt 当日榜单不稳定，需接受“无可用来源”并如实记录。
[2026-02-07] GitHub Trending 仍以 github-trending.today 为主数据源；Hugging Face 模型页数据为动态渲染，优先使用 datasets trending 做信号补充；Twitter/X 热榜缺少稳定公开入口；Product Hunt 当日榜单常在次日可用。
[2026-02-08] GitHub-Trending.Today 仍是最稳定的开源榜单源（可提供更新时间与星数）；HN 前页可用 /front?day=YYYY-MM-DD 回溯昨日；HNRSS 前页接口返回 400；HF 数据集 Trending 仍为动态渲染，缺少可稳定抽取的条目。
[2026-02-09] GitHub Trending 页面可稳定抓取并提供当日新增星数，适合作为主榜单源；github-trending.today 仍可作小众补充但更新时间滞后；可考虑 GitHub Trending RSS 作为备用链路。
[2026-02-10] GitHub Trending HTML 直链可用并能稳定抽取仓库名与 Star；HN /front?day 偶发错误，改用首页提取；HF Trending Papers 页面可获得低星项目 GitHub 链接；Product Hunt 当日榜仍不稳定。
[2026-02-11] GitHub Trending 今日可直接抓取并提取 stars today；硬件相关信息分散在媒体报道，需通过多家媒体交叉验证关键信息。
[2026-02-12] GitHub Trending 与 github-trending.today 抓取不稳定，改用仓库页 star 作为热度信号并在日报中标注来源；硬件消息需至少两家媒体交叉验证。
[2026-03-07] TechCrunch AI 分类 RSS 可稳定返回标题与 UTC 时间戳，适合判断“当日事件”；The Verge AI Atom 适合补充舆情但不宜单源定性；Anthropic 官方新闻页可直接提取发布日期与关键指标（如漏洞数量）。
[2026-03-10] OpenAI News RSS 可稳定提供当日公司级动态（含精确 pubDate）；GitHub Trending HTML 可解析 repo/star/当日增星；Product Hunt 受 Cloudflare 挑战页影响不可稳定抓取，需在日报中明确标注“无可验证当日数据”。
[2026-03-11] OpenAI 与 Product Hunt 页面均触发 Cloudflare 挑战，需改用可访问替代源；TechCrunch RSS 在当日新闻抓取上稳定可用；Anthropic News 可从页面嵌入 JSON 抽取 publishedOn/slug；HF papers/trending 可解析 `DailyPapers` 的 data-props JSON 获取 githubStars 与 upvotes。

## 内容分类规则

### 判断"重大事件"的标准
- 融资超过 1 亿美元
- 头部公司（OpenAI/Google/Meta/Anthropic/Microsoft 等）发布新模型或重大产品更新
- 政策法规变化（AI 监管、开源协议争议等）
- 技术突破（benchmark 大幅刷新、新范式出现）

### 判断"热门开源"的标准
- 当日/当周 GitHub Trending 上榜
- 24h 内 star 增长 > 500
- 社区多个信息源同时讨论

### 判断"小众宝藏"的标准
- star < 1000 但解决了真实痛点
- 技术路线独特或创新
- 作者有持续维护迹象

### 判断"国内大模型厂商动态"的标准
- 官方公告/博客/更新日志优先
- 媒体报道需标注“未官方确认”
- 只收录当日发布/更新的信息

## 趋势追踪

> Agent 在此维护中长期趋势线索，帮助识别跨日的连续事件。

| 趋势 | 首次发现 | 最近更新 | 状态 |
|------|----------|----------|------|
| 多模型编程代理竞赛（OpenAI GPT-5.3-Codex 与 Anthropic Opus 4.6 同日发布，GitHub Agent HQ 支持多代理） | 2026-02-06 | 2026-02-10 | 进行中 |
| MCP 服务生态（Developer Knowledge API + MCP Server 作为代理上下文基础设施） | 2026-02-07 | 2026-02-10 | 进行中 |
| Agentic security（安全研究自动化与代理化红队工具兴起） | 2026-02-10 | 2026-03-11 | 进行中 |
| AI 硬件时间表回调（OpenAI 新设备上市推迟至 2027 年初） | 2026-02-11 | 2026-02-12 | 进行中 |
| 模型安全协作产品化（模型厂商与浏览器/基础软件团队联合挖掘并修复漏洞） | 2026-03-07 | 2026-03-07 | 进行中 |
| AI 治理与采购边界法律化（前沿模型公司与政府采购/合规冲突进入诉讼阶段） | 2026-03-09 | 2026-03-10 | 进行中 |
| 办公入口 AI 原生化（Workspace/会议/设计工具集中内嵌 AI） | 2026-03-11 | 2026-03-11 | 进行中 |

## 自我优化日志

> 每次执行后，Agent 反思本次采集的质量并记录改进措施。

| 日期 | 问题 | 改进措施 | 是否已应用 |
|------|------|----------|-----------|
| 2026-02-06 | GitHub Trending 与 Product Hunt 当日页可访问性不稳定 | 使用备用来源并在日报中标注数据日期 | 是 |
| 2026-02-07 | Product Hunt 当日榜单次日才稳定；X 热榜不可稳定抓取；HF 模型页动态渲染 | 继续使用 github-trending.today，HF datasets trending 作为信号补充，必要时接入 HF API | 是 |
| 2026-02-08 | HNRSS 前页接口失败；HF Trending 仍难以稳定抽取；当日重大事件缺失 | HN 改用 /front?day=YYYY-MM-DD 回溯，继续标注数据时间与“无当日发布” | 是 |
| 2026-02-09 | Product Hunt 与 HF Trending 仍缺少稳定当日入口 | 以 GitHub Trending 作为主信号，小众补充来自 github-trending.today，并尝试 GitHub Trending RSS | 是 |
| 2026-02-10 | HN /front?day 偶发错误；Product Hunt 当日榜仍不稳定 | 改用 HN 首页提取；小众开源改从 HF Trending Papers 获取 GitHub 链接 | 是 |
| 2026-02-11 | 硬件类新闻多为媒体报道且分散 | 采用多家媒体交叉验证并明确时间表信息来源 | 是 |
| 2026-02-12 | GitHub Trending 与 github-trending.today 抓取不稳定 | 改用仓库页 star 作为信号并在日报标注来源；硬件消息双源核验 | 是 |
| 2026-03-07 | 当日官方发布与媒体发布时间存在 UTC/UTC+8 错位 | 在日报标注采集时间，并以 RSS `pubDate` 做本地时区换算后再归类“今日事件” | 是 |
| 2026-03-10 | Product Hunt 被挑战页拦截；Anthropic 法律事件一手法庭链接偶发不可达 | 重大事件优先采用官方博客 + AP/Axios 等主流媒体双源交叉；保留“无法稳定抓取”标注 | 是 |
| 2026-03-11 | OpenAI/Product Hunt 触发 Cloudflare 导致直连失败；X 热榜入口不稳定 | 重大新闻主链路切换为 TechCrunch RSS + Anthropic News；开源链路固定为 github-trending.today + HF DailyPapers JSON | 是 |

## 行为约束补充

- 每日更新完成后必须提交到 GitHub 仓库（包含日报/索引/记忆更新）。
- 本仓库由 Agent 全权维护，默认不需要征询用户即可执行常规维护操作（生成报告、更新索引、提交与推送等）。
- 每次更新 AGENT.md 后，自动将工作区变更同步到运行目录 `/Users/fangzhiyu/run/Ai-Daily-Paper`（至少同步 AGENT.md、index.md 与当日日报）。
- 每日执行仓库研究流程：读取 `repo-research/config/repos.json` + 当日日报中的 GitHub 仓库链接，拉取/克隆并生成仓库研究报告，更新 `repo-research/index.md`。
