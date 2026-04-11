# NousResearch/hermes-agent - 自我改进的 AI 代理深度分析

**项目地址**: https://github.com/NousResearch/hermes-agent  
**Star 数**: 44,401⭐  
**分析日期**: 2026-04-10  
**开发者**: Nous Research

---

## 📋 项目概述

Hermes Agent 是由 Nous Research 开发的自我改进型 AI 代理，它是**唯一内置学习循环的代理系统**。与传统的无状态 AI 助手不同，Hermes 能够：

- 从经验中创建技能
- 在使用过程中改进技能
- 主动提醒自己持久化知识
- 搜索自己的历史对话
- 跨会话构建用户模型

最重要的是，Hermes 不绑定到你的笔记本电脑 - 它可以运行在 $5 的 VPS、GPU 集群或无服务器基础设施上，闲置时几乎零成本。你可以从 Telegram 与它对话，而它在云端 VM 上工作。

---

## 🎯 核心特性

### 1. 闭环学习系统

Hermes 的最大创新是**闭环学习**：

```
经验 → 技能创建 → 使用中改进 → 主动提醒 → 知识持久化 → 跨会话召回
```

- **代理策划的记忆** - 定期提醒自己记录重要信息
- **自主技能创建** - 完成复杂任务后自动生成技能
- **技能自我改进** - 在使用过程中优化技能
- **FTS5 会话搜索** - 全文搜索历史对话，LLM 总结用于跨会话召回
- **Honcho 辩证用户建模** - 构建深化的用户理解模型
- **兼容 agentskills.io 开放标准**

### 2. 真正的终端界面

完整的 TUI（文本用户界面）：
- 多行编辑
- 斜杠命令自动补全
- 对话历史
- 中断和重定向
- 流式工具输出

### 3. 多平台存在

一个网关进程支持所有平台：
- Telegram
- Discord
- Slack
- WhatsApp
- Signal
- CLI

语音备忘录转录，跨平台对话连续性。

### 4. 计划自动化

内置 cron 调度器，支持任何平台交付：
- 每日报告
- 夜间备份
- 每周审计

全部用自然语言定义，无人值守运行。

### 5. 委托与并行化

- 为并行工作流生成隔离的子代理
- 编写通过 RPC 调用工具的 Python 脚本
- 将多步骤管道折叠为零上下文成本的回合

### 6. 随处运行

六种终端后端：
- **本地** - 直接在你的机器上
- **Docker** - 容器化环境
- **SSH** - 远程服务器
- **Daytona** - 无服务器持久化
- **Singularity** - HPC 环境
- **Modal** - 无服务器 GPU

Daytona 和 Modal 提供无服务器持久化 - 代理环境在闲置时休眠，按需唤醒，会话间成本几乎为零。

### 7. 研究就绪

- 批量轨迹生成
- Atropos RL 环境
- 轨迹压缩，用于训练下一代工具调用模型

---

## 🏗️ 技术架构

### 模型灵活性

Hermes 支持任何 LLM 提供商：
- Nous Portal
- OpenRouter（200+ 模型）
- z.ai/GLM
- Kimi/Moonshot
- MiniMax
- OpenAI
- 或你自己的端点

使用 `hermes model` 切换 - 无需代码更改，无锁定。

### 工具系统

40+ 内置工具，工具集系统，终端后端支持。

### 技能系统

- **程序性记忆** - 技能是代理的"肌肉记忆"
- **Skills Hub** - 社区技能库
- **创建技能** - 代理可以自己创建和改进技能

### 记忆系统

- **持久化记忆** - 跨会话保留信息
- **用户档案** - 构建用户偏好和习惯的模型
- **最佳实践** - 自动应用学到的经验

### MCP 集成

连接任何 MCP（Model Context Protocol）服务器以扩展能力。

---

## 🚀 安装与使用

### 快速安装

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

支持 Linux、macOS、WSL2 和 Android（通过 Termux）。

### 基本命令

```bash
hermes                    # 启动交互式 CLI
hermes model              # 选择 LLM 提供商和模型
hermes tools              # 配置启用的工具
hermes config set         # 设置配置值
hermes gateway            # 启动消息网关（Telegram、Discord 等）
hermes setup              # 运行完整设置向导
hermes claw migrate       # 从 OpenClaw 迁移
hermes update             # 更新到最新版本
hermes doctor             # 诊断问题
```

### 跨平台命令

| 操作 | CLI | 消息平台 |
|------|-----|---------|
| 开始聊天 | `hermes` | 运行 `hermes gateway setup` + `hermes gateway start`，然后发送消息 |
| 新对话 | `/new` 或 `/reset` | `/new` 或 `/reset` |
| 更换模型 | `/model [provider:model]` | `/model [provider:model]` |
| 设置个性 | `/personality [name]` | `/personality [name]` |
| 重试/撤销 | `/retry`, `/undo` | `/retry`, `/undo` |
| 压缩上下文 | `/compress`, `/usage` | `/compress`, `/usage` |
| 浏览技能 | `/skills` 或 `/<skill-name>` | `/skills` 或 `/<skill-name>` |
| 中断工作 | Ctrl+C 或发送新消息 | `/stop` 或发送新消息 |

---

## 💡 创新点与优势

### 1. 真正的学习能力

大多数 AI 代理是无状态的 - 每次对话都从零开始。Hermes 通过闭环学习系统：
- **记住经验** - 不仅仅是对话历史，而是提炼的知识
- **创建技能** - 将复杂任务转化为可重用的技能
- **自我改进** - 技能在使用中不断优化

### 2. 基础设施灵活性

Hermes 打破了"AI 助手绑定笔记本电脑"的限制：
- 在 $5 VPS 上运行，从手机访问
- 无服务器部署，闲置时零成本
- GPU 集群支持，处理重型任务

### 3. 多渠道统一

一个代理实例，多个访问点：
- 在 Telegram 上快速提问
- 在 Discord 上团队协作
- 在 CLI 上深度工作

所有对话共享同一个记忆和上下文。

### 4. 从 OpenClaw 无缝迁移

对于 OpenClaw 用户，Hermes 提供自动迁移：

```bash
hermes claw migrate
```

迁移内容：
- SOUL.md（个性文件）
- 记忆（MEMORY.md 和 USER.md）
- 技能（用户创建的技能）
- 命令白名单
- 消息设置
- API 密钥
- TTS 资源

### 5. 研究友好

Hermes 不仅是生产工具，也是研究平台：
- 批量轨迹生成用于训练
- Atropos RL 环境集成
- 轨迹压缩技术

---

## 🎯 使用场景

### 个人助手

- 跨设备访问（笔记本、手机、平板）
- 记住你的偏好和习惯
- 主动提醒和计划任务

### 开发助手

- 代码生成和审查
- 调试和问题解决
- 文档编写

### 研究工具

- 文献搜索和总结
- 数据分析
- 实验设计

### 团队协作

- 在 Discord/Slack 上作为团队成员
- 共享知识库
- 自动化工作流

---

## 📊 与竞品对比

| 特性 | Hermes Agent | OpenClaw | Claude Code | Codex |
|------|-------------|----------|-------------|-------|
| 学习循环 | ✅ 内置 | ⚠️ 部分 | ❌ 无 | ❌ 无 |
| 多平台 | ✅ 6+ 平台 | ✅ 多平台 | ❌ 仅 Web | ❌ 仅终端 |
| 无服务器 | ✅ Daytona/Modal | ❌ 无 | ❌ 无 | ❌ 无 |
| 技能系统 | ✅ 自动创建 | ✅ 手动创建 | ❌ 无 | ⚠️ 有限 |
| 用户建模 | ✅ Honcho | ⚠️ 基础 | ❌ 无 | ❌ 无 |
| 开源 | ✅ MIT | ✅ 开源 | ❌ 闭源 | ❌ 闭源 |

---

## 🔮 未来展望

### 潜在发展方向

1. **更强的学习能力** - 从用户反馈中学习，而不仅仅是经验
2. **多代理协作** - Hermes 实例之间的协作
3. **企业功能** - 团队管理、审计、合规
4. **移动原生应用** - 专用的 iOS/Android 应用

### 挑战

1. **复杂性** - 功能丰富意味着学习曲线陡峭
2. **资源消耗** - 持久化记忆和技能系统需要存储和计算
3. **隐私** - 跨会话记忆引发隐私考虑

---

## 🎓 关键启示

1. **学习能力是下一代 AI 代理的关键** - 无状态代理已经不够用了
2. **基础设施灵活性很重要** - 不应该绑定到特定设备或平台
3. **多渠道访问是必需的** - 用户希望在任何地方与代理交互
4. **开源和可扩展性** - 社区驱动的发展比闭源更有活力

---

## 🔗 相关资源

- **项目主页**: https://github.com/NousResearch/hermes-agent
- **文档**: https://hermes-agent.nousresearch.com/docs/
- **Discord**: https://discord.gg/NousResearch
- **Skills Hub**: https://agentskills.io
- **Nous Research**: https://nousresearch.com

---

## 📝 总结

Hermes Agent 代表了 AI 代理的下一个进化阶段：**从工具到伙伴**。

通过内置学习循环、跨会话记忆、多平台存在和基础设施灵活性，Hermes 不仅仅是一个 AI 助手 - 它是一个**与你一起成长的智能伙伴**。

对于希望拥有真正个性化、持续改进的 AI 助手的用户，Hermes 提供了一个开源、灵活、功能强大的解决方案。

**推荐指数**: ⭐⭐⭐⭐⭐ (5/5)  
**适用人群**: 高级用户、开发者、研究人员、需要持久化 AI 助手的任何人  
**学习成本**: 中高（功能丰富，需要时间掌握）  
**回报**: 极高（真正的个性化和持续改进）

**核心优势**: 学习能力、基础设施灵活性、多平台支持  
**独特卖点**: 唯一内置学习循环的开源 AI 代理
