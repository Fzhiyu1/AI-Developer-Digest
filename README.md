# AI Daily Paper

AI 领域自动化信息采集与知识沉淀系统。

每日自动采集 AI 领域动态，生成结构化日报，深度分析开源仓库，构建可检索的知识库。

## 这个项目解决什么问题

AI 行业每天产生大量信息——新模型发布、开源项目涌现、融资并购、政策变动。手动跟踪这些信息：

- **耗时**：每天需要 1-2 小时浏览 GitHub、Hacker News、Twitter、TechCrunch 等多个平台
- **遗漏**：信息源分散，难以全面覆盖，容易错过重要事件
- **浅尝辄止**：看到有趣的开源项目，收藏了但从未深入研究
- **缺乏积累**：信息流过即忘，无法形成可追溯的知识体系

本项目将这些工作交给 AI 自动完成，人只需要阅读产出。

## 核心能力

### 1. 多源信息采集

从 8 个信息源自动采集，按优先级覆盖：

| 优先级 | 信息源 | 覆盖领域 |
|--------|--------|----------|
| P0 | GitHub Trending | 开源项目 |
| P0 | Hacker News | 综合新闻 |
| P0 | Twitter/X AI 圈 | 实时动态 |
| P1 | TechCrunch / The Verge | 行业新闻 |
| P1 | Hugging Face | 模型/数据集 |
| P1 | Product Hunt | 新产品 |
| P2 | ArXiv | 论文 |
| P2 | Reddit | 社区讨论 |

### 2. 结构化日报

采集到的信息按 6 个维度分类输出：

- **重大事件** — 融资、新模型发布、政策变动、技术突破
- **热门开源项目** — GitHub Trending 或 24h Star > 500
- **小众宝藏项目** — Star < 1000 但解决真实痛点
- **国内大模型动态** — DeepSeek / 智谱 / 阿里 / 百度 / 字节等
- **自进化智能体** — Agent 框架、MCP、多代理协作
- **智能穿戴硬件** — AI 设备、可穿戴 AI、脑机接口

### 3. 多层级报告体系

```
日报（每日）→ 周报（每周日）→ 月报（每月末）→ 年报（12.31）
```

每一层都是对下层的**汇总提炼**，而非简单拼接。

### 4. 仓库深度研究

自动从日报中提取 GitHub 链接，clone 到本地并分析：

- 技术栈与语言分布
- 架构信息（从 README 提取）
- 社区活跃度（Star / Fork / Commit 频率 / Issue 数）
- 最新 Release 与更新时间
- 目录结构概览

每个仓库生成独立的研究报告，持续追踪更新。

### 5. 自我优化

Agent 每次执行后自动更新策略文件（AGENT.md）：

- 记录哪些搜索词有效、哪些需要替换
- 扩展关键词库
- 追踪中长期趋势
- 优化分类规则

系统会随着使用越来越精准。

## 架构

```
┌─────────────────────────────────────────────┐
│              Docker Container                │
│                                              │
│  ┌─────────┐    ┌──────────────────────┐     │
│  │  cron   │───→│  Claude Code CLI      │     │
│  │ 每日9:00 │    │  执行 PROMPT.md 流程  │     │
│  └─────────┘    └──────────┬───────────┘     │
│                            │                  │
│              ┌─────────────┼──────────┐       │
│              ▼             ▼          ▼       │
│        生成日报      仓库研究    更新记忆      │
│              │             │          │       │
│              ▼             ▼          ▼       │
│  ┌───────────────────────────────────────┐   │
│  │           持久化存储 (Volume)           │   │
│  │  reports/  repo-research/  AGENT.md   │   │
│  └───────────────────────────────────────┘   │
│                      │                        │
│                      ▼                        │
│              git commit & push                │
└─────────────────────────────────────────────┘
```

核心思路：Docker 只负责**环境和调度**，Claude Code CLI 作为执行引擎完成信息采集、分析和报告生成。

## 项目结构

```
AI-Daily-Paper-v1/
├── Dockerfile                         # 容器构建
├── docker-compose.yml                 # 服务编排
├── crontab                            # 定时任务配置
├── scripts/
│   └── run.sh                         # 每日执行入口
│
├── prompts/
│   ├── PROMPT.md                      # Agent 执行流程指令
│   └── START.md                       # 启动提示词
│
├── agent/
│   └── AGENT.md                       # Agent 记忆与策略（自维护）
│
├── reports/                           # 报告输出
│   ├── daily/                         # 日报 — YYYY-MM-DD.md
│   ├── weekly/                        # 周报 — YYYY-W{周数}.md
│   ├── monthly/                       # 月报 — YYYY-MM.md
│   └── yearly/                        # 年报 — YYYY.md
│
├── repo-research/                     # 仓库研究子系统
│   ├── config/repos.json              # 关注仓库配置
│   ├── cache/                         # 运行状态与 registry
│   ├── repos/                         # 本地镜像仓库
│   ├── scripts/repo_research.py       # 仓库研究脚本
│   ├── reports/                       # 研究报告（按日期分组）
│   └── index.md                       # 仓库研究索引
│
├── index.md                           # 报告总索引
└── README.md
```

## 快速开始

### 环境变量

```bash
cp .env.example .env
```

```env
ANTHROPIC_API_KEY=sk-ant-...        # 必需 — Claude API Key
GITHUB_TOKEN=ghp_...                # 可选 — 避免 GitHub API 限流
```

### 启动服务

```bash
docker compose up -d
```

服务启动后将按 cron 配置自动执行，默认每日 09:00。

### 手动触发

```bash
docker compose exec app /scripts/run.sh
```

## 数据流

```
信息源（GitHub / HN / Twitter / ...）
        │
        ▼
   Claude Code CLI 采集与分析
        │
        ├──→ reports/daily/YYYY-MM-DD.md     日报
        │         │
        │         ├──→ reports/weekly/        周报（每周日汇总）
        │         ├──→ reports/monthly/       月报（每月末汇总）
        │         └──→ reports/yearly/        年报（年末汇总）
        │
        ├──→ 提取 GitHub 链接
        │         │
        │         ▼
        │    repo-research/
        │    ├── repos/          clone 到本地
        │    └── reports/        生成研究报告
        │
        ├──→ index.md            更新总索引
        └──→ AGENT.md            更新策略记忆
```

## 行为约束

1. **不编造** — 搜索不到就标注"今日无相关动态"，绝不捏造信息
2. **标注来源** — 每条信息附带来源链接
3. **事实与观点分离** — 事实陈述和分析判断明确区分
4. **时效性优先** — 只报道当日发生的事件
5. **信号 > 噪音** — 宁可少报，不可注水

## 许可证

MIT
