# AionUi — 命令行 AI 工具的统一图形化协作平台

> 仓库：[iOfficeAI/AionUi](https://github.com/iOfficeAI/AionUi) · 许可证：Apache-2.0 · 当前版本：v1.8.8

## 1. 项目概述

AionUi 是一个开源桌面应用，为 Gemini CLI、Claude Code、Codex、Qwen Code、Goose CLI 等命令行 AI 工具提供统一的图形化界面，支持多会话、文件管理、远程 WebUI 访问和定时任务。

## 2. 技术栈

| 层级 | 技术 |
|------|------|
| 框架 | Electron 37 + Electron Forge |
| 前端 | React 19 + TypeScript 5.8 + UnoCSS |
| UI 组件 | Arco Design (字节跳动) |
| 数据库 | better-sqlite3（本地存储） |
| 编辑器 | Monaco Editor + CodeMirror |
| AI SDK | @anthropic-ai/sdk、@google/genai、openai |
| 构建 | Webpack（通过 Electron Forge 插件） |
| 测试 | Jest 30 + ts-jest |
| 渠道集成 | Grammy (Telegram)、Lark SDK (飞书) |
| 其他 | MCP SDK、sharp（图像处理）、docx/xlsx/pptx 文档生成 |

语言占比：TypeScript 89.2%、Python 8.2%、JavaScript 1.8%、CSS 0.7%

## 3. 项目结构

```
AionUi/
├── src/                    # 核心源码（Electron 主进程 + 渲染进程）
├── assistant/              # 内置 AI 助手定义（Markdown 文件）
├── skills/                 # 可扩展技能系统（pptx、docx、mermaid 等）
├── config/                 # 应用配置
├── scripts/                # 构建与部署脚本
├── tests/                  # Jest 测试
├── public/                 # 静态资源
├── resources/              # 图片、图标等
├── homebrew/               # Homebrew 发布配置
├── .claude/skills/         # Claude Code 技能定义
├── .gemini/                # Gemini CLI 配置
├── .github/workflows/      # CI/CD（构建发布 + AI 代码审查）
├── electron-builder.yml    # 跨平台打包配置
└── forge.config.ts         # Electron Forge 配置
```

## 4. 核心功能

### 4.1 多 Agent 模式（ACP — Agent Communication Protocol）

通过 ACP 协议统一管理多种命令行 AI 工具。自动检测本地已安装的 CLI 工具，在同一界面中切换使用。内置 Gemini CLI，开箱即用。

从最近提交可见 ACP 层的活跃开发：
- `fix(acp): prevent orphan CLI processes on conversation kill` — 解决会话关闭时子进程泄漏
- `fix(acp): prevent CodeBuddy CLI from freezing Electron via SIGTTOU` — 处理 CLI 工具与 Electron 进程组的信号冲突
- `feat: integrate Mistral Vibe CLI` — 持续扩展支持的 CLI 工具

### 4.2 远程访问与渠道集成

提供 WebUI 模式，支持从任意设备通过浏览器访问。集成 Telegram Bot（Grammy 框架）和飞书 Bot（Lark SDK），实现跨平台消息交互。Express 5 提供后端 API 服务，含速率限制和 JWT 认证。

### 4.3 文件预览与办公自动化

内置 9+ 格式预览面板（PDF、Word、Excel、PPT、代码、Markdown、图片、HTML、Diff），AI 生成文件后即时查看。依赖 docx、xlsx-republish、pptx2json、mammoth 等库实现文档读写。支持定时任务（croner 库），实现无人值守的自动化工作流。

## 5. 活跃度

| 指标 | 数据 |
|------|------|
| Stars | 15,497 |
| Forks | 1,175 |
| Open Issues | 102 |
| Watchers | 72 |
| 项目年龄 | 约 6 个月（创建于 2025-08-07） |
| 最新版本 | v1.8.8（2026-02-12 发布） |
| 最近 5 个版本 | v1.8.4→v1.8.8，跨度 4 天（02-08 至 02-12），几乎日更 |

近 10 次提交（截至 2026-02-13）涉及至少 3 位活跃开发者：
- **piorpua (zynx)** — 核心维护者，负责 ACP 层、模型选择器重构、版本发布
- **IceyLiu (瓦砾)** — 合并 PR、代码审查
- **YW1975 (さだはる)** — 外部贡献者，修复孤儿进程问题

PR 编号已达 #851，说明项目有大量外部贡献。GitHub Actions 配置了 Gemini 和 GPT 自动代码审查，CI/CD 流程成熟。

## 6. 亮点与不足

### 亮点

1. **CLI 工具统一入口的差异化定位**：市场上没有其他项目同时支持 Gemini CLI、Claude Code、Codex、Qwen Code、Goose CLI、Mistral Vibe 等 7+ 种 CLI 工具的图形化管理。ACP 协议层的抽象设计使新增 CLI 后端成本较低（从提交记录看，集成 Mistral Vibe 是单个 PR）
2. **发布节奏极快**：5 天内发布 5 个版本（v1.8.4-v1.8.8），每个版本都有实质性功能（AWS Bedrock 支持、安全设置页、Diff 渲染等），说明团队执行力强
3. **完整的远程访问方案**：WebUI + Telegram + 飞书三通道覆盖，配合定时任务功能，真正实现 7×24 小时远程 AI 助手。这是纯 CLI 工具无法提供的能力

### 不足

1. **核心维护者集中度高**：近 10 次提交中 piorpua 参与了 7 次（含合并），IceyLiu 参与 2 次。虽然有外部 PR，但核心架构决策高度依赖 1-2 人，存在 bus factor 风险
2. **102 个 Open Issues 与快速发版的矛盾**：几乎日更的发版节奏下仍积累了 102 个未关闭 issue，暗示可能存在功能扩张快于质量收敛的问题。测试框架虽已配置（Jest 30），但 tests/ 目录在项目树中占比不明
3. **重度依赖外部 AI 服务 API**：dependencies 中包含 @anthropic-ai/sdk、@google/genai、openai 三大 SDK，加上 MCP SDK。任何一家 API 变更都可能影响核心功能。内置 Gemini CLI 依赖 Google 账号认证，免费额度受限于 Google 政策变化

## 7. 竞品对比

| 维度 | AionUi | Claude Desktop (Cowork) | Open WebUI |
|------|--------|------------------------|------------|
| Stars | 15.5K | 官方闭源 | 70K+ |
| 平台 | macOS / Windows / Linux | 仅 macOS | Web（需自部署） |
| CLI 工具支持 | 7+ 种（Gemini CLI、Claude Code、Codex 等） | 仅 Claude Code | 无（纯 API 调用） |
| 模型支持 | 多平台 API + 本地 Ollama | 仅 Claude | 多平台 API + Ollama |
| 远程访问 | WebUI + Telegram + 飞书 | 无 | 原生 Web |
| 文件预览 | 9+ 格式内置预览 | 基础文件操作 | 无 |
| 定时任务 | 支持 | 不支持 | 不支持 |
| 费用 | 免费开源（API 费用自付） | $100/月订阅 | 免费开源 |
| 定位 | CLI AI 工具的图形化协作层 | Claude 官方桌面端 | 通用 LLM 聊天界面 |

AionUi 的核心差异在于"CLI 工具图形化"这一独特定位。Open WebUI 侧重 API 直连的聊天体验，不涉及 CLI 工具管理；Claude Desktop 仅服务 Claude 生态。AionUi 填补了"已有 CLI 工具用户需要更好交互体验"这一空白。

## 8. 应用方向分析

### 核心痛点

命令行 AI 工具（Claude Code、Gemini CLI 等）功能强大但交互体验差：会话无法持久化、不支持多任务并行、文件操作不直观、无法远程访问。AionUi 在不替换底层工具的前提下，叠加图形化、持久化、远程化能力。

### 最佳应用场景

**场景一：多 AI 工具重度用户的统一工作台**
同时使用 Claude Code 写代码、Gemini CLI 做分析、Codex 做补全的开发者，不再需要在多个终端窗口间切换。AionUi 提供统一的会话管理、历史记录和文件预览，减少上下文切换成本。定时任务功能还能让 AI 在非工作时间自动执行批量任务（如代码审查、数据处理）。

**场景二：团队/个人的远程 AI 助手**
将 AionUi 部署在服务器或家庭 NAS 上，通过 WebUI 或 Telegram 从任何设备访问。适合需要随时调用 AI 能力但不想在每台设备上配置 CLI 工具的场景。飞书集成特别适合国内企业团队协作。

其他场景：办公自动化（文档生成、文件整理）、AI 图像生成的可视化工作流。

### 对个人开发者的价值

免费开源，零订阅成本（对比 Claude Desktop $100/月）。内置 Gemini CLI 开箱即用，降低入门门槛。本地 SQLite 存储保证数据隐私，适合处理敏感项目代码。

### 对企业的价值

飞书集成和 WebUI 远程访问适合团队共享 AI 能力。Apache-2.0 许可证允许商业使用和二次开发。但当前缺乏多用户权限管理和审计日志，企业级部署需要额外定制。102 个 Open Issues 和快速迭代节奏意味着稳定性需要自行验证。
