# Rowboat — 开源 AI 协作助手（带持久记忆）

> **仓库**：[rowboatlabs/rowboat](https://github.com/rowboatlabs/rowboat)
> **一句话概述**：本地优先的 AI 协作工具，连接邮件和会议笔记，构建长期知识图谱（Obsidian 兼容 Markdown），并基于上下文帮助用户完成工作（起草邮件、生成文档/PPT、会议准备等）。

---

## 1. 项目元信息

| 指标 | 数值 |
|------|------|
| Stars | 5,272 |
| Forks | 418 |
| Open Issues | 36 |
| Watchers | 38 |
| 许可证 | Apache-2.0 |
| 主语言 | TypeScript (96.5%) |
| 创建时间 | 2025-01-13 |
| 项目年龄 | 约 13 个月 |
| 最新版本 | v0.1.49 (2026-02-12) |
| 组织 | rowboatlabs (YC S24) |

---

## 2. 技术栈

- **前端**：Next.js + TypeScript（`apps/rowboat`，Web 版）、Electron（`apps/rowboatx` + `apps/x`，桌面版）
- **后端/CLI**：Node.js TypeScript（`apps/cli`，含 agent、知识图谱、MCP 集成）
- **Python SDK**：`apps/python-sdk`，提供编程接口
- **向量存储**：Qdrant（有独立 Dockerfile）
- **语音**：Deepgram API（可选，语音笔记转写）
- **集成**：Gmail、Granola、Fireflies（会议笔记）、MCP 协议扩展（Slack、Linear、GitHub 等）
- **LLM**：支持 BYOM（Bring Your Own Model）——Ollama/LM Studio 本地模型或任意 API 提供商
- **数据存储**：本地 Markdown 文件（Obsidian 兼容 vault），无专有格式

---

## 3. 项目结构

```
rowboat/
├── apps/
│   ├── rowboat/          # Next.js Web 应用（主界面）
│   │   ├── app/          # 页面、API 路由、组件
│   │   ├── src/          # 领域层（application/entities/infrastructure/interface-adapters）
│   │   └── di/           # 依赖注入
│   ├── rowboatx/         # Electron 桌面前端（Next.js）
│   ├── x/                # Electron 主进程/预加载/渲染器（monorepo，pnpm workspace）
│   │   ├── apps/main/    # Electron 主进程
│   │   ├── apps/preload/ # 预加载脚本
│   │   ├── apps/renderer/# 渲染进程
│   │   └── packages/     # core + shared 共享包
│   ├── cli/              # CLI 工具（agents、知识图谱、MCP、TUI）
│   └── python-sdk/       # Python SDK
├── docker-compose.yml    # Docker 编排（含 Qdrant）
├── build-electron.sh     # Electron 构建脚本
└── start.sh              # 启动脚本
```

架构采用 Clean Architecture 分层（entities → application → infrastructure → interface-adapters），依赖注入容器管理服务。

---

## 4. 核心功能

### 4.1 知识图谱（长期记忆）

Rowboat 的核心差异化在于持久化知识图谱，而非每次对话重新检索。连接邮件和会议笔记后，自动提取人物、项目、决策、承诺等实体，以 Markdown + backlinks 形式存储在本地 vault 中。用户可随时查看、编辑知识图谱内容。

README 原文描述：
> Rowboat maintains **long-lived knowledge** instead: context accumulates over time, relationships are explicit and inspectable, notes are editable by you, not hidden inside a model, everything lives on your machine as plain Markdown.

### 4.2 背景 Agent

可配置自动运行的后台 Agent，执行重复性任务：
- 自动起草邮件回复（基于历史上下文）
- 每日生成语音笔记（议程、优先级、会议）
- 定期生成项目更新
- 自动维护知识图谱

### 4.3 MCP 工具扩展

通过 Model Context Protocol 连接外部工具和服务，README 列举的集成包括：Exa（搜索）、Twitter/X、ElevenLabs（语音）、Slack、Linear/Jira、GitHub 等。CLI 层（`apps/cli/src/mcp/`）实现了 MCP 客户端。

---

## 5. 活跃度分析

**提交频率**：最近 10 次提交全部集中在 2026-02-12（同一天），包含功能开发、UI 调整、bug 修复，开发节奏密集。

**发版频率**：
- v0.1.49 — 2026-02-12
- v0.1.47 — 2026-02-10
- v0.1.46 — 2026-02-09
- v0.1.45 — 2026-02-06

近一周发布 4 个版本，每个版本含 14 个构建产物（Mac/Windows/Linux 多平台），迭代速度快。

**贡献者**（共 5 人）：

| 贡献者 | 提交数 | 角色推测 |
|--------|--------|----------|
| ramnique | 551 | 核心开发者/创始人 |
| akhisud3195 | 323 | 核心开发者 |
| arkml | 266 | 核心开发者 |
| tusharmagar | 164 | 前端/UI 开发 |
| takshakmudgal | 2 | 外部贡献 |

**Issue 状态**：36 个 open issue，近期活跃 issue 包括 onboarding 问题（#347）、Claude 订阅兼容性（#346）、重复思考修复（#334 PR）。

---

## 6. 亮点与不足

### 亮点

1. **知识图谱 vs 检索**：区别于 RAG 方案的"每次冷启动"，Rowboat 的持久知识图谱让上下文随时间积累，这是产品层面的核心创新。数据以 Obsidian 兼容 Markdown 存储，用户可直接在 Obsidian 中查看编辑，无锁定风险。

2. **BYOM + MCP 扩展性**：支持本地模型（Ollama/LM Studio）和任意 API 提供商，通过 MCP 协议可连接几乎任何外部工具。这让隐私敏感用户和企业都能使用。

3. **YC S24 背书 + 高发版频率**：Y Combinator S24 批次项目，13 个月内从 0 到 5.2K stars，近一周 4 个版本发布，团队执行力强。

### 不足

1. **核心团队极小**：仅 4 名活跃开发者（第 5 人仅 2 次提交），551 + 323 + 266 + 164 = 1,304 次提交集中在 4 人手中。对于一个包含 Web 应用 + Electron 桌面端 + CLI + Python SDK 的复杂项目，人力风险明显。

2. **依赖闭源 LLM 服务**：虽然支持 BYOM，但核心 Agent 功能的质量高度依赖 LLM 能力。本地小模型（如 Ollama 跑 7B）能否支撑知识图谱构建和复杂推理，README 未给出明确说明或基准测试。

3. **测试覆盖不明**：目录树中未见 `tests/`、`__tests__/`、`*.test.ts` 等测试目录或文件（至少在前两层结构中不可见）。对于 v0.1.49 且快速迭代的项目，缺乏可见的测试基础设施是质量风险。

---

## 7. 竞品对比

| 特性 | Rowboat | Mem0 | Khoj | Obsidian Copilot |
|------|---------|------|------|-----------------|
| GitHub Stars | 5.2K | 24K+ | 18K+ | 3K+ |
| 核心定位 | AI 协作助手 + 知识图谱 | AI 记忆层（API） | 自托管 AI 助手 | Obsidian 插件 |
| 知识图谱 | 原生支持，Markdown backlinks | 记忆存储，非图谱 | 向量检索为主 | 依赖 Obsidian vault |
| 桌面应用 | Electron（Mac/Win/Linux） | 无（API/SDK） | Web UI | Obsidian 插件 |
| 本地模型 | 支持（Ollama/LM Studio） | 部分支持 | 支持 | 支持 |
| 邮件/日历集成 | Gmail + 会议笔记 | 无 | Gmail/Outlook | 无 |
| MCP 扩展 | 支持 | 不支持 | 不支持 | 不支持 |
| 数据格式 | 纯 Markdown（Obsidian 兼容） | 专有存储 | 混合 | Markdown |
| 部署方式 | 桌面应用 / Docker | 云 API / 自托管 | Docker / 云 | Obsidian 插件 |

Rowboat 的独特定位在于：它不是一个记忆 API（Mem0）、不是一个通用 AI 助手（Khoj）、也不是一个编辑器插件（Obsidian Copilot），而是一个完整的"AI 协作工作流"——从数据采集（邮件/会议）到知识积累（图谱）到行动输出（文档/邮件/PPT）的闭环。

---

## 8. 应用方向分析

### 核心痛点

AI 助手每次对话都"失忆"，用户需要反复解释背景。Rowboat 通过持久知识图谱解决这个问题——上下文随时间积累而非每次重建。

### 最佳应用场景

**场景一：高频会议 + 邮件的知识工作者**
产品经理、项目经理、管理者等角色每天处理大量邮件和会议。Rowboat 自动从 Gmail 和会议笔记中提取关键信息（决策、承诺、待办），构建人物和项目关系图谱。会议前自动生成 brief（历史决策 + 未解决问题），会后自动捕获 action items。这类用户的痛点最强——信息分散在邮件、日历、笔记中，人工整理成本极高。

**场景二：需要长期上下文的内容生产**
咨询顾问、分析师等需要基于积累的上下文生成文档、报告、PPT。Rowboat 的知识图谱让 AI 生成的内容有真实的历史依据，而非泛泛而谈。PDF 幻灯片生成功能直接产出可用的交付物。

其他场景：团队知识管理（共享 vault）、个人 CRM（自动维护联系人关系和互动历史）。

### 价值分析

**个人开发者**：Rowboat 对纯编码场景价值有限（不是代码助手），但对需要管理多个项目、客户沟通、会议跟进的独立开发者/自由职业者有用。本地优先 + BYOM 意味着零额外成本（用 Ollama 跑本地模型）。主要价值在于减少"上下文切换"的认知负担。

**企业**：最大价值在于知识不外泄（本地存储 + 可选本地模型）。MCP 扩展可对接内部工具（Jira、Slack、CRM）。但当前缺乏多用户协作功能和权限管理，企业级部署需要等待产品成熟。YC 背景意味着团队有商业化路径，但 v0.1.x 版本号表明产品仍处于早期。

---

*报告生成时间：2026-02-13 | 数据来源：GitHub API*
