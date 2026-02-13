# Personal AI Infrastructure (PAI)

> 个人 Agentic AI 基础设施框架，通过模块化 Packs 系统为 Claude Code 等 AI 编码助手添加持久记忆、目标导向、技能路由和自我改进能力。

## 项目概述

PAI（Personal AI Infrastructure）由安全研究者 Daniel Miessler 创建，定位为"构建在 Claude Code 之上的个人 AI 操作系统"。核心理念是将通用 AI 助手转变为了解用户目标、偏好和历史的个性化 AI 系统。项目从 2025 年 9 月启动，经历 6 个大版本迭代，当前 v2.5.0（2026-01-31 发布）。

- GitHub: `danielmiessler/Personal_AI_Infrastructure`
- Stars: 7,644 | Forks: 1,097 | Open Issues: 122
- License: MIT | 语言: TypeScript
- 创建时间: 2025-09-08 | 最近推送: 2026-02-10

## 技术栈

| 层级 | 技术 |
|------|------|
| 运行时 | Bun (TypeScript 执行) |
| 主语言 | TypeScript, Bash, Python |
| AI 平台 | Claude Code (主要), 兼容 OpenCode/Cursor/Windsurf |
| 语音 | ElevenLabs TTS |
| 浏览器自动化 | Playwright |
| 安装 | AI 辅助安装（DA 读取 Pack 自动配置） |

## 项目结构

```
PAI/
├── Packs/                  # 23 个模块化能力包（核心）
│   ├── pai-core-install/   # 核心技能、身份、记忆系统
│   ├── pai-hook-system/    # 事件驱动自动化 + 安全验证
│   ├── pai-voice-system/   # ElevenLabs 语音通知
│   ├── pai-observability-server/  # 实时监控仪表盘
│   ├── pai-statusline/     # 终端状态栏
│   └── pai-*-skill/        # 18 个技能包（研究、安全、创作等）
├── Bundles/                # 包的策划集合
│   └── Official/           # 官方 PAI Bundle
├── Releases/               # 版本发布（v2.3, v2.4, v2.5）
├── Tools/                  # 验证、备份、模板工具
├── .claude/                # Claude Code 配置目录
└── Plans/                  # 项目规划文档
```

总计 5,191 个文件，仓库体积 ~270MB（含大量图片资源）。

## 核心功能

### 1. TELOS 目标系统

PAI 的核心差异化在于"以人为中心"的目标系统。通过 10 个 Markdown 文件定义用户身份：

```
TELOS/
├── MISSION.md      # 人生使命
├── GOALS.md        # 当前目标
├── PROJECTS.md     # 活跃项目
├── BELIEFS.md      # 核心信念
├── MODELS.md       # 思维模型
├── STRATEGIES.md   # 执行策略
├── NARRATIVES.md   # 个人叙事
├── LEARNED.md      # 经验教训
├── CHALLENGES.md   # 当前挑战
└── IDEAS.md        # 想法库
```

DA（Digital Assistant）在每次交互中参考这些文件，使响应与用户长期目标对齐。

### 2. Pack 模块化系统

每个 Pack 是自包含的能力单元，包含代码、工作流、安装指令和验证测试。安装方式为"AI 辅助安装"——将 Pack 目录交给 DA，DA 自动读取并配置。

5 个基础设施包 + 18 个技能包，覆盖：
- 安全侦察（recon, redteam, osint）
- 研究分析（research, firstprinciples, council）
- 创作工具（art, prompting, createcli）
- 系统维护（system, algorithm, upgrade）

### 3. 三层记忆架构

```
Hot  → 当前会话上下文（即时可用）
Warm → 近期交互历史（跨会话持久化）
Cold → 长期知识库（经验、决策、学习）
```

每次交互生成信号（评分、情感、成功/失败），反馈到记忆系统驱动持续改进。v2.5 引入"Thinking Tools with Justify-Exclusion"机制，要求 DA 主动解释为什么不使用某个能力。

## 活跃度

| 指标 | 数据 |
|------|------|
| 项目年龄 | ~17 个月（2025-09-08 创建，距今 2026-02-13） |
| 发布节奏 | 5 个版本 / 2.5 个月（v2.0 到 v2.5，2025-12-28 至 2026-01-31） |
| 最近提交 | 2026-02-10（10 个 PR 同日合并） |
| Contributors | 486 次提交来自 danielmiessler，其余贡献者均 ≤3 次 |
| Watchers | 126 |
| 社区 | GitHub Discussions + Discord（UL Community） |

版本迭代极快：v2.0（2025-12-28）→ v2.5（2026-01-31），34 天内 5 个大版本。最近一批提交（2026-02-10）全部是社区 PR 修复（Windows 兼容、路径修正、文档更新），说明社区参与度在上升。

## 亮点与不足

### 亮点

1. **架构设计成熟** — User/System 分离确保升级不破坏用户配置，Pack 系统实现真正的模块化，16 条设计原则（UNIX 哲学、Spec/Test First 等）体现工程素养
2. **目标导向的差异化** — TELOS 系统将 AI 助手从"工具执行者"提升为"目标伙伴"，这是目前同类项目中独有的设计
3. **安全意识内建** — Hook 系统默认验证命令安全性，无需 `--dangerously-skip-permissions`；包含 recon、redteam、osint 等安全技能包，反映作者安全背景

### 不足

1. **单人维护风险高** — 486/~500 次提交来自 danielmiessler 一人，其余贡献者合计 <20 次提交。项目复杂度（5,191 文件、23 个 Pack）与维护人力严重不匹配
2. **强依赖闭源服务** — 核心功能依赖 Claude Code（Anthropic 闭源产品），语音依赖 ElevenLabs API。虽声称"平台无关"，但 Pack 系统深度绑定 `.claude/` 目录结构和 Claude Code 的 hook/skill 机制
3. **缺乏自动化测试** — 仓库中未见测试目录或 CI 测试配置（`.github/` 仅有 Actions 配置用于 Node 兼容性）。23 个 Pack 的验证依赖"AI 辅助安装后人工检查"，无回归测试保障

## 竞品对比

| 特性 | PAI | [fabric](https://github.com/danielmiessler/fabric) (同作者) | [aider](https://github.com/paul-gauthier/aider) | [open-interpreter](https://github.com/OpenInterpreter/open-interpreter) |
|------|-----|--------|-------|------------------|
| Stars | 7.6K | 30K+ | 25K+ | 55K+ |
| 定位 | 个人 AI 操作系统 | AI Prompt 模式库 | AI 结对编程 | 自然语言计算机控制 |
| 持久记忆 | 三层记忆架构 | 无 | 有（仓库级） | 有限 |
| 目标系统 | TELOS（10 维度） | 无 | 无 | 无 |
| 模块化 | Pack 系统（23 包） | Pattern 系统 | 插件 | 技能系统 |
| 平台依赖 | Claude Code 为主 | 多模型 | 多模型 | 多模型 |
| 安装复杂度 | 高（需 Bun + Claude Code） | 低（pip install） | 低（pip install） | 低（pip install） |

PAI 的独特价值在于"目标导向 + 持久记忆 + 模块化技能"的组合，但安装门槛和平台依赖是明显短板。fabric 作为同作者的前作，定位互补（fabric 提供 prompt 模式，PAI 提供运行基础设施）。

## 应用方向分析

### 核心痛点

AI 编码助手（Claude Code、Cursor 等）是无状态的——每次对话从零开始，不了解用户的长期目标、偏好和工作历史。PAI 试图在这些工具之上构建"个性化层"，让 AI 助手真正成为了解你的长期伙伴。

### 最佳应用场景

**场景一：重度 Claude Code 用户的效率倍增器**

对于每天使用 Claude Code 数小时的开发者，PAI 的记忆系统和技能路由能显著减少重复上下文输入。TELOS 目标文件让 DA 在每次交互中自动对齐长期项目方向，Hook 系统自动化安全检查和会话管理。适合有明确长期项目（如独立开发者构建 SaaS）的用户。

**场景二：安全研究者的 AI 工作台**

PAI 内置 recon、redteam、osint、privateinvestigator 四个安全技能包，加上 council（多 Agent 辩论）和 firstprinciples（第一性原理分析），构成完整的安全研究工作流。这反映了作者 Daniel Miessler 的安全背景（fabric 项目同样源于安全社区）。

其他场景：内容创作者（art + prompting 技能包）、团队共享 AI 基础设施（Bundle 系统支持统一配置分发）。

### 个人开发者 vs 企业

**个人开发者**：PAI 最大价值是将零散的 AI 使用习惯系统化。TELOS 迫使你明确目标，记忆系统积累经验，技能包标准化常见工作流。但安装和维护成本不低——需要理解 Bun、TypeScript、Claude Code hook 机制，适合愿意投入时间"调教"AI 的技术用户。

**企业**：当前阶段不适合企业直接采用。单人维护、无测试覆盖、强依赖 Claude Code 闭源服务是主要风险。但 Pack 架构和 User/System 分离的设计思路值得企业 AI 基础设施团队参考——特别是"如何让 AI 助手在组织级别保持一致性同时允许个人定制"这一问题。

---

*数据采集时间: 2026-02-13 | 数据来源: GitHub API*
