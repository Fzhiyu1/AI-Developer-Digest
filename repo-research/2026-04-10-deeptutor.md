# HKUDS/DeepTutor - 代理原生个性化学习助手深度分析

**项目地址**: https://github.com/HKUDS/DeepTutor  
**Star 数**: 14,870⭐  
**分析日期**: 2026-04-10  
**开发者**: 香港大学数据科学团队（HKUDS）

---

## 📋 项目概述

DeepTutor 是一个代理原生（Agent-Native）的个性化学习助手，由香港大学数据科学团队开发。它不是简单的问答机器人，而是一个完整的学习生态系统，集成了多种学习模式、知识管理、持久化记忆和自主 TutorBot。

项目在 2025 年 12 月 29 日首次发布，仅 39 天就达到 10k stars，2026 年 4 月 4 日发布 v1.0.0，标志着架构的全面重写和"代理原生"理念的确立。

---

## 🎯 核心特性

### 1. 统一聊天工作区 - 五种模式，一个线程

DeepTutor 的最大创新是**模式融合**：五种学习模式共享同一个对话上下文。

| 模式 | 功能 |
|------|------|
| **Chat** | 流畅的工具增强对话，支持 RAG 检索、网络搜索、代码执行、深度推理、头脑风暴、论文搜索 |
| **Deep Solve** | 多代理问题解决：计划 → 调查 → 解决 → 验证，每步都有精确的来源引用 |
| **Quiz Generation** | 基于知识库生成评估题，内置验证 |
| **Deep Research** | 将主题分解为子主题，派发并行研究代理（RAG + Web + 学术论文），生成完整引用的报告 |
| **Math Animator** | 将数学概念转化为视觉动画和故事板（基于 Manim） |

**关键优势**：从快速聊天开始 → 遇到难题升级到 Deep Solve → 生成测验题自测 → 启动 Deep Research 深入研究 - **全程不丢失任何消息**。

### 2. 个人 TutorBots - 不是聊天机器人，是自主导师

基于 [nanobot](https://github.com/HKUDS/nanobot) 构建的持久化代理系统：

- **灵魂模板** - 通过可编辑的 Soul 文件定义个性、语气和教学哲学（苏格拉底式、鼓励型、严格型）
- **独立工作区** - 每个 bot 有自己的目录，独立的记忆、会话、技能和配置
- **主动心跳** - bot 不仅响应，还会主动发起：学习检查、复习提醒、计划任务
- **完整工具访问** - 每个 bot 都能使用 DeepTutor 的完整工具包
- **技能学习** - 通过添加技能文件教 bot 新能力
- **多渠道存在** - 连接到 Telegram、Discord、Slack、飞书、企业微信、钉钉、Email
- **团队与子代理** - 在单个 bot 内生成后台子代理或编排多代理团队

```bash
deeptutor bot create math-tutor --persona "Socratic math teacher who uses probing questions"
deeptutor bot create writing-coach --persona "Patient, detail-oriented writing mentor"
```

### 3. AI Co-Writer - AI 是一等公民的协作者

不是侧边栏，不是事后补充，而是**内置在编辑器中的 AI 协作者**：

- 完整的 Markdown 编辑器
- 选择任何文本 → 重写/扩展/缩短
- 可选从知识库或网络获取上下文
- 非破坏性编辑流程，完整的撤销/重做
- 每篇文章都可以保存到笔记本，反馈到学习生态系统

### 4. 引导式学习 - 将材料转化为结构化学习旅程

将个人材料转化为多步骤学习路径：

1. **设计学习计划** - 从材料中识别 3-5 个渐进的知识点
2. **生成交互页面** - 每个知识点变成丰富的可视化 HTML 页面（解释、图表、示例）
3. **启用上下文问答** - 在每个步骤旁边聊天以深入探索
4. **总结进度** - 完成后收到学习总结

会话是持久化的 - 随时暂停、恢复或重访任何步骤。

### 5. 知识中心 - RAG 就绪的文档集合

- **知识库** - 上传 PDF、TXT、Markdown 文件创建可搜索的 RAG 集合，增量添加文档
- **笔记本** - 跨会话组织学习记录，从 Chat、Guided Learning、Co-Writer、Deep Research 保存见解到分类的彩色笔记本

知识库不是被动存储 - 它**主动参与**每次对话、每次研究会话和每条学习路径。

### 6. 持久化记忆 - 构建你的活档案

DeepTutor 通过两个互补维度维护对你的持久化理解：

- **摘要** - 学习进度的运行摘要：学过什么、探索了哪些主题、理解如何发展
- **档案** - 学习者身份：偏好、知识水平、目标、沟通风格 - 通过每次交互自动细化

记忆在所有功能和所有 TutorBot 之间共享。使用越多，个性化和效果越好。

### 7. 代理原生 CLI - 每个能力都在一个命令之外

完整的 CLI 原生支持：
- 人类友好的丰富终端输出
- AI 代理和管道的结构化 JSON 输出
- 将 [SKILL.md](https://github.com/HKUDS/DeepTutor/blob/main/SKILL.md) 交给任何工具使用代理，它可以自主操作 DeepTutor

```bash
deeptutor run chat "Explain Fourier transform" -t rag --kb textbook
deeptutor run deep_solve "Prove that √2 is irrational" -t reason
deeptutor run deep_research "Attention mechanisms in transformers"
deeptutor kb create my-kb --doc textbook.pdf
```

---

## 🏗️ 技术架构

### 代理原生架构（v1.0.0 重写）

DeepTutor 2.0 采用两层插件模型：

1. **工具层（Tools）** - 原子能力（RAG 检索、网络搜索、代码执行）
2. **能力层（Capabilities）** - 编排工具的工作流（Chat、Deep Solve、Deep Research）

这种分离使得：
- 工具可以在不同能力间重用
- 能力可以灵活组合工具
- 易于扩展和定制

### 支持的 LLM 提供商（30+）

| 提供商 | Binding | 默认 URL |
|--------|---------|---------|
| OpenAI | openai | https://api.openai.com/v1 |
| Anthropic | anthropic | https://api.anthropic.com/v1 |
| Gemini | gemini | https://generativelanguage.googleapis.com/v1beta/openai/ |
| DeepSeek | deepseek | https://api.deepseek.com |
| Moonshot (Kimi) | moonshot | https://api.moonshot.ai/v1 |
| Ollama | ollama | http://localhost:11434/v1 |
| OpenRouter | openrouter | https://openrouter.ai/api/v1 |
| 智谱 AI (GLM) | zhipu | https://open.bigmodel.cn/api/paas/v4 |
| 通义千问 | dashscope | https://dashscope.aliyuncs.com/compatible-mode/v1 |
| ... | ... | ... |

支持任何 OpenAI 兼容的自定义端点。

### 支持的网络搜索提供商

- **Brave** - 推荐，有免费层
- Tavily
- Jina
- SearXNG（自托管，无需 API 密钥）
- DuckDuckGo（无需 API 密钥）
- Perplexity

### RAG 管道

基于 [LlamaIndex](https://github.com/run-llama/llama_index)：
- 文档索引和检索
- 增量文档上传
- 灵活的 RAG 管道导入
- 支持 Docling 和 MinerU 解析器

---

## 🚀 安装与部署

### 选项 A：引导式安装（推荐）

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor
conda create -n deeptutor python=3.11 && conda activate deeptutor
python scripts/start_tour.py
```

引导式安装提供：
- **Web 模式** - 选择依赖配置，安装所有内容，启动临时服务器，在浏览器中完成四步设置向导（LLM、Embedding、搜索提供商），实时连接测试，完成后自动重启
- **CLI 模式** - 完全交互式终端流程：选择配置、安装依赖、配置提供商、验证连接、应用

### 选项 B：Docker 部署

```bash
git clone https://github.com/HKUDS/DeepTutor.git
cd DeepTutor
cp .env.example .env
# 编辑 .env 填写必需字段

# 拉取官方镜像（推荐）
docker compose -f docker-compose.ghcr.yml up -d

# 或从源码构建
docker compose up -d
```

官方镜像发布到 [GitHub Container Registry](https://github.com/HKUDS/DeepTutor/pkgs/container/deeptutor)，支持 linux/amd64 和 linux/arm64。

数据持久化通过 Docker volumes：
- `/app/data/user` → `./data/user` - 设置、记忆、工作区、会话、日志
- `/app/data/knowledge_bases` → `./data/knowledge_bases` - 上传的文档和向量索引

### 选项 C：仅 CLI

```bash
pip install -e ".[cli]"
deeptutor chat  # 交互式 REPL
```

---

## 💡 创新点与优势

### 1. 模式融合 - 打破工具孤岛

传统学习工具是孤立的：聊天是聊天，问题解决是问题解决，研究是研究。DeepTutor 的统一工作区让你在**同一个对话线程**中无缝切换模式。

这模拟了人类学习的自然流程：从简单问题开始，遇到难题深入研究，然后测试理解。

### 2. TutorBot - 从工具到导师

大多数 AI 学习助手是被动的工具。TutorBot 是**主动的导师**：
- 设置提醒
- 主动检查学习进度
- 学习新技能
- 跨会话记住你

每个 TutorBot 是独立的代理实例，有自己的个性和记忆。

### 3. 代理原生设计

DeepTutor 从一开始就为 AI 代理设计：
- 完整的 CLI 接口
- 结构化的 JSON 输出
- SKILL.md 文档让其他代理可以操作它
- 两层插件架构易于扩展

### 4. 知识生态系统

知识不是静态存储，而是**活跃的生态系统**：
- 上传的文档参与对话
- 对话见解保存到笔记本
- 笔记本反馈到引导式学习
- 所有内容都可以被 RAG 检索

### 5. 开源与社区驱动

- MIT 许可证（TutorBot 部分）/ Apache-2.0（核心）
- 活跃的 Discord 社区
- 持续的更新（v1.0.0-beta.4 在 2026-04-10 发布）
- 来自 HKUDS 生态系统（LightRAG、AutoAgent、AI-Researcher）

---

## 🎯 使用场景

### 学生

- 个性化学习路径
- 作业辅导（Deep Solve）
- 论文研究（Deep Research）
- 考试准备（Quiz Generation）

### 自学者

- 构建个人知识库
- 系统化学习新主题
- 跟踪学习进度

### 研究人员

- 文献综述（Deep Research + 论文搜索）
- 概念理解（Math Animator）
- 知识管理（笔记本）

### 教育工作者

- 创建学习材料（Co-Writer）
- 生成评估题（Quiz Generation）
- 个性化学生辅导（TutorBot）

---

## 📊 与竞品对比

| 特性 | DeepTutor | ChatGPT | Claude | Perplexity |
|------|-----------|---------|--------|------------|
| 多模式融合 | ✅ 5 种模式 | ❌ 单一聊天 | ❌ 单一聊天 | ⚠️ 搜索+聊天 |
| 持久化记忆 | ✅ 跨会话 | ⚠️ 有限 | ⚠️ 有限 | ❌ 无 |
| 知识库 | ✅ RAG 集成 | ⚠️ 文件上传 | ⚠️ 文件上传 | ❌ 无 |
| TutorBot | ✅ 多实例代理 | ❌ 无 | ❌ 无 | ❌ 无 |
| CLI 原生 | ✅ 完整 CLI | ❌ 仅 Web | ❌ 仅 Web | ❌ 仅 Web |
| 开源 | ✅ 完全开源 | ❌ 闭源 | ❌ 闭源 | ❌ 闭源 |
| 自托管 | ✅ 支持 | ❌ 无 | ❌ 无 | ❌ 无 |

---

## 🔮 未来展望

### 路线图

- 🔜 **认证与登录** - 多用户支持的可选登录页面
- 🔜 **主题与外观** - 多样化主题选项和可定制 UI
- 🔜 **LightRAG 集成** - 集成 [LightRAG](https://github.com/HKUDS/LightRAG) 作为高级知识库引擎
- 🔜 **文档站点** - 全面的文档页面，包含指南、API 参考和教程

### 潜在发展方向

1. **移动应用** - 原生 iOS/Android 应用
2. **协作学习** - 多用户学习小组
3. **游戏化** - 学习成就、进度追踪、排行榜
4. **更多 TutorBot 模板** - 预构建的专业导师（编程、数学、语言）

---

## 🎓 关键启示

1. **学习工具应该是生态系统，而非孤立工具** - 模式融合是未来
2. **AI 导师应该主动，而非被动** - TutorBot 的心跳系统展示了这一点
3. **知识应该流动，而非静止** - 从文档到对话到笔记本的循环
4. **代理原生设计很重要** - CLI 和 JSON 输出让 AI 可以操作 AI
5. **开源和自托管是教育工具的关键** - 隐私和控制很重要

---

## 🔗 相关资源

- **项目主页**: https://github.com/HKUDS/DeepTutor
- **Discord**: https://discord.gg/eRsjPgMU4t
- **SKILL.md**: https://github.com/HKUDS/DeepTutor/blob/main/SKILL.md
- **HKUDS 生态系统**:
  - [LightRAG](https://github.com/HKUDS/LightRAG) - 简单快速的 RAG
  - [AutoAgent](https://github.com/HKUDS/AutoAgent) - 零代码代理框架
  - [AI-Researcher](https://github.com/HKUDS/AI-Researcher) - 自动化研究
  - [nanobot](https://github.com/HKUDS/nanobot) - 超轻量级 AI 代理

---

## 📝 总结

DeepTutor 不仅仅是一个学习助手 - 它是一个**完整的个性化学习生态系统**。

通过模式融合、主动 TutorBot、知识生态系统和代理原生设计，DeepTutor 将 AI 辅助学习从"问答工具"提升到"智能学习伙伴"。

对于认真对待学习的学生、自学者、研究人员和教育工作者，DeepTutor 提供了一个开源、可自托管、功能强大的解决方案。

**推荐指数**: ⭐⭐⭐⭐⭐ (5/5)  
**适用人群**: 学生、自学者、研究人员、教育工作者  
**学习成本**: 中等（功能丰富但界面友好）  
**回报**: 极高（真正的个性化学习体验）

**核心优势**: 模式融合、TutorBot、知识生态系统、开源  
**独特卖点**: 唯一将 5 种学习模式融合在统一工作区的开源学习助手

**特别推荐**: 如果你正在构建个人知识库、系统化学习新领域，或需要一个能记住你、与你一起成长的学习伙伴，DeepTutor 是最佳选择。
