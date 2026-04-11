# shanraisshan/claude-code-best-practice - Claude Code 最佳实践指南

**GitHub**: https://github.com/shanraisshan/claude-code-best-practice  
**Stars**: 35,765 ⭐  
**类型**: 文档/最佳实践集合  
**发布日期**: 2026-04-11

---

## 📋 项目概述

这是一个社区驱动的 Claude Code 最佳实践集合，由 Shayan Raisshan 维护，汇集了 Claude Code 团队成员（Boris Cherny、Thariq 等）和社区贡献者的实战经验。口号是"从 vibe coding 到 agentic engineering"。

---

## 🏗️ 核心功能体系

### 五大核心概念

| 概念 | 位置 | 描述 |
|------|------|------|
| **Subagents** | `.claude/agents/<name>.md` | 独立上下文中的自主 Actor，有自定义工具、权限、模型和持久身份 |
| **Commands** | `.claude/commands/<name>.md` | 注入现有上下文的知识，用户调用的提示模板 |
| **Skills** | `.claude/skills/<name>/SKILL.md` | 可配置、可预加载、自动发现，支持上下文分叉和渐进式披露 |
| **Hooks** | `.claude/hooks/` | 在 agentic 循环外运行的用户定义处理器 |
| **MCP Servers** | `.claude/settings.json` | 连接外部工具、数据库和 API |

### 编排模式

所有主要工作流都收敛于同一架构模式：

```
Research → Plan → Execute → Review → Ship
```

Command → Agent → Skill 的组合模式是最推荐的编排方式。

---

## 💡 核心最佳实践

### Prompting

- **挑战 Claude**："grill me on these changes and don't make a PR until I pass your test"
- **优雅重构**：在平庸修复后说"knowing everything you know now, scrap this and implement the elegant solution"
- **不要微管理**：粘贴 bug，说"fix"，不要指定如何修复

### Planning/Specs

- 始终从 plan mode 开始
- 让 Claude 用 `AskUserQuestion` 工具采访你，然后新建 session 执行
- 制定分阶段的门控计划，每个阶段有多种测试
- 原型优于 PRD：构建 20-30 个版本而不是写规格

### CLAUDE.md

- 每个文件保持在 200 行以内
- 用 `<tag>` 包裹领域特定规则防止被忽略
- 单体仓库使用多个 CLAUDE.md（祖先 + 后代加载）
- 用 `.claude/rules/` 拆分大型指令
- 任何开发者都应能运行 Claude 并说"run the tests"就能成功

### Agents

- 使用特性专用子 Agent（额外上下文）+ Skills（渐进式披露）
- 说"use subagents"来投入更多算力
- 用 tmux + git worktrees 实现并行开发
- 利用测试时算力：一个 Agent 制造 bug，另一个（同模型）找 bug

### Skills

- 用 `context: fork` 在隔离子 Agent 中运行 skill
- 在每个 skill 中构建 Gotchas 部分——最高信号内容
- skill description 是触发器，不是摘要——为模型写（"什么时候应该触发？"）
- 不要在 skills 中陈述显而易见的事情
- 不要在 skills 中限制 Claude——给目标和约束，不要逐步指令

### Hooks

- 用 PostToolUse hook 自动格式化代码
- 通过 hook 将权限请求路由到 Opus——让它扫描攻击并自动批准安全的
- 用 Stop hook 在每轮结束时推动 Claude 继续或验证工作

### Workflows

- 在 50% 时手动 `/compact`，避免 agent dumb zone
- 用 `/model` 选择模型，Opus 用于 plan mode，Sonnet 用于代码
- 始终使用 thinking mode 和 Explanatory 输出风格
- 用 `Esc Esc` 或 `/rewind` 撤销而不是在同一上下文中修复

### Git/PR

- 保持 PR 小而专注（p50 为 118 行）
- 始终 squash merge——干净的线性历史
- 至少每小时提交一次

---

## 🆕 新功能（2026）

| 功能 | 状态 | 描述 |
|------|------|------|
| **Ultraplan** | Beta | 云端草稿计划，浏览器审查，内联注释 |
| **Claude Code Web** | Beta | 云端基础设施运行任务，无需本地设置 |
| **Agent SDK** | GA | Python/TypeScript SDK 构建生产 AI Agent |
| **No Flicker Mode** | Beta | 无闪烁全屏渲染，鼠标支持 |
| **Computer Use** | Beta | 让 Claude 控制 macOS 屏幕 |
| **Auto Mode** | Beta | 后台安全分类器替代手动权限提示 |
| **Channels** | Beta | 从 Telegram/Discord/Webhook 推送事件到运行中的 session |
| **Code Review** | Beta | 多 Agent PR 分析，捕获 bug 和安全漏洞 |
| **Voice Dictation** | Beta | 20 语言支持的语音输入 |
| **Agent Teams** | Beta | 多 Agent 并行处理同一代码库 |
| **Remote Control** | GA | 从任何设备继续本地 session |

---

## 📊 与其他框架对比

| 框架 | Stars | 独特性 |
|------|-------|--------|
| Everything Claude Code | 148k | 本能评分、AgentShield、多语言规则 |
| **claude-code-best-practice** | **35k** | **社区实践集合、持续更新** |
| Superpowers | 143k | TDD-first、Iron Laws、整体计划审查 |
| Spec Kit | 87k | 规格驱动、宪法、22+ 工具 |
| BMAD-METHOD | 44k | 完整 SDLC、Agent 角色、22+ 平台 |

---

## 🔮 关键洞察

1. **Skills > Commands > Agents**：对于可重用工作流，Skills 是最佳选择
2. **上下文管理是核心**：50% 时 compact，避免 agent dumb zone
3. **测试时算力**：多 Agent 协作比单 Agent 更可靠
4. **原型优于规格**：低成本构建多个版本
5. **Hooks 是自动化的关键**：PostToolUse 格式化、Stop 验证

---

**总结**: 这是目前最全面的 Claude Code 实践指南，持续跟踪官方团队的最新建议和社区经验。对于任何认真使用 Claude Code 的开发者来说，这是必读资源。
