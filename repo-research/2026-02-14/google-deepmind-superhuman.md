# google-deepmind/superhuman 深度研究报告

> 研究日期：2026-02-14 | 数据来源：GitHub API

## 1. 项目概述

Google DeepMind Superhuman Reasoning 团队的开源项目集合，包含 IMO 数学竞赛基准测试（IMO Bench）和 AI 数学研究 Agent（Aletheia）的 prompt、输出及数据集，是 DeepMind 在 AI 超人类数学推理领域的核心公开成果。

## 2. 技术栈

- 主要语言：TeX（论文和数学证明的排版）
- 数据格式：CSV（基准测试数据集）
- 依赖模型：Gemini Deep Think（Aletheia 的底层推理引擎）
- 关联项目：alphageometry、alphageometry2（几何推理，独立仓库）
- 许可证：Apache 2.0（代码）+ CC-BY 4.0（数据和论文材料）

## 3. 项目结构

```
superhuman/
├── README.md
├── imobench/                    # IMO 数学基准测试套件
│   ├── README.md
│   ├── answerbench_v2.csv       # 400 道简答题（v2 修正版）
│   ├── proofbench.csv           # 60 道证明题
│   ├── gradingbench.csv         # 1000 条人工评分数据（~11MB）
│   └── imgs/                    # 评估结果可视化图表
├── aletheia/                    # 数学研究 Agent 输出
│   ├── README.md
│   ├── Aletheia.pdf             # Agent 系统论文（~2MB）
│   ├── Erdos/                   # Erdős 开放问题研究
│   ├── BKKKZ26/                 # 快速收敛级数无理性证明
│   ├── F26/                     # 算术 Hirzebruch 比例原理
│   ├── FYZ26/                   # 非平凡特征权计算
│   ├── ACGKMP/                  # 强多项式迭代鲁棒马尔可夫链
│   └── LeeSeo26/                # 独立集下界推广
└── CONTRIBUTING.md, LICENSE
```

## 4. 核心功能

### 4.1 IMO Bench — AI 数学推理基准测试

三个子基准构成完整评估闭环：
- IMO-AnswerBench：400 道 IMO 级别简答题，覆盖代数、组合、几何、数论四大领域
- IMO-ProofBench：60 道需要完整证明的竞赛题，由专家审核
- IMO-GradingBench：1000 条人工评分样本，用于训练和评估自动评分系统

README 中的引用方式：
```
IMO-AnswerBench: answerbench_v2.csv
IMO-ProofBench: proofbench.csv
IMO-GradingBench: gradingbench.csv
```

### 4.2 Aletheia — AI 数学研究 Agent

由 Gemini Deep Think 驱动的数学研究 Agent，能够迭代生成、验证和修订数学解答。已产出 6 个研究级数学成果，每个均附带完整的 TeX 源码、PDF 输出和对应的 ArXiv 论文链接。

关键成果包括：
- 对 Erdős 开放问题的半自主案例研究（ArXiv: 2601.22401）
- Erdős-1051 的推广——证明特定快速收敛级数的无理性（ArXiv: 2601.21442）
- Feng-Yun-Zhang 算术 Hirzebruch 比例原理的特征权计算（ArXiv: 2601.23245）

### 4.3 AlphaGeometry 系列（外部链接）

README 引用了 AlphaGeometry（Nature 论文）和 AlphaGeometry2（2024 IMO 银牌），代码在独立仓库，本仓库作为 Superhuman Reasoning 团队的统一入口。

## 5. 活跃度

| 指标 | 数值 |
|------|------|
| Stars | 392 |
| Forks | 29 |
| Watchers | 15 |
| Open Issues/PRs | 9 |
| Contributors | 4 |
| 项目年龄 | ~3.5 个月（创建于 2025-10-29） |
| 最近提交 | 2026-02-13（修复 answerbench 数据） |

提交时间线（最近 10 次）：
- 2026-02-13：修复 answerbench 题目 + 发布 answerbench_v2.csv（Junsu Kim）
- 2026-02-11：添加 Aletheia 论文 + 更新主 README（Thang Luong，团队负责人）
- 2026-02-02~04：密集添加 Aletheia 研究成果（Erdos、BKKKZ26、F26、FYZ26、ACGKMP、LeeSeo26）（Yuri Chervonyi）

核心贡献者：ychervonyi（9 次提交，主力）、dawsenhwang（6 次，committer 角色）、nurijunsu（2 次）、lmthang（1 次，Thang Luong 本人）。团队规模小但均为 Google 内部员工（@google.com 邮箱），通过 Google 内部 Piper 系统同步代码。

Issue 状态：9 个 open，全部来自外部贡献者（Ashutosh0x），包括添加 CI、HuggingFace 数据集卡片、Python 库封装等 PR，目前均未获回复或合并。

## 6. 亮点与不足

### 亮点

1. 学术影响力极高：IMO Bench 论文已发表于 EMNLP 2025，Aletheia 的 6 个研究成果均有对应 ArXiv 论文，是目前 AI 数学推理领域最权威的公开基准之一
2. 数据质量经过迭代验证：answerbench_v2.csv 是根据清华、MIT、Caltech、首尔国立大学等多所高校研究者的反馈修正的，说明基准已被广泛使用并形成反馈闭环
3. Aletheia 产出了原创数学成果：不是复现已知结论，而是在 Erdős 开放问题等研究前沿产出了新结果，这在 AI 辅助科学发现领域具有里程碑意义

### 不足

1. 社区互动几乎为零：9 个外部 PR/Issue 全部无回复（最早的 PR 已挂 2 天），Google 团队仅通过内部 Piper 单向推送代码，不接受外部贡献的信号明显
2. 完全依赖闭源模型：Aletheia 依赖 Gemini Deep Think，仓库仅提供 prompt 和输出，无法独立复现。对于基准测试，评估其他模型可行，但 Aletheia 的核心能力不可复制
3. 无可执行代码：整个仓库是数据集 + TeX 文件 + PDF，没有任何可运行的代码、脚本或工具。外部贡献者尝试添加 Python 库封装（PR #5-#9）但未获回应

## 7. 竞品对比

| 项目 | Stars | 内容类型 | 难度级别 | 自动评分 | 可执行代码 |
|------|-------|----------|----------|----------|------------|
| google-deepmind/superhuman | 392 | IMO 级基准 + AI 研究输出 | 研究级/竞赛级 | GradingBench 支持 | 无 |
| openai/simple-evals (MATH) | ~2K | 多领域评估框架 | 本科~竞赛 | 内置 | Python 框架 |
| hendrycks/math (MATH dataset) | ~1.5K | 12.5K 数学题 | 高中~本科 | 答案匹配 | Python 加载器 |
| TIGER-AI-Lab/TheoremQA | ~300 | 定理应用题 | 本科~研究生 | 答案匹配 | Python 评估 |

关键差异：superhuman 定位在数学推理的最高难度层级（IMO 竞赛 + 研究前沿），其他基准主要覆盖本科到竞赛入门级别。但 superhuman 缺乏可执行的评估框架，使用门槛较高。

## 8. 应用方向分析

### 核心痛点

AI 数学推理能力缺乏高难度、高质量的评估标准。现有基准（MATH、GSM8K）已被主流模型接近饱和，无法区分顶尖模型的推理能力差异。IMO Bench 填补了这一空白。

### 最佳应用场景

**场景一：顶尖推理模型的能力评估**
IMO-AnswerBench 的 400 道题和 IMO-ProofBench 的 60 道证明题，是目前区分 Gemini Deep Think、GPT-5.2、Claude Opus 等顶尖模型数学推理能力的最佳公开基准。GradingBench 的 1000 条人工评分数据可用于训练自动评分器，解决证明题评估的核心难题。

**场景二：AI 辅助数学研究的方法论参考**
Aletheia 的 prompt 和输出提供了"AI 如何参与研究级数学"的完整案例。研究者可以参考其迭代生成-验证-修订的工作流，将类似方法应用于其他基础科学领域。

其他场景：数学竞赛训练（题目难度适合 IMO 选手备赛）、自动评分系统研发（GradingBench 提供训练数据）。

### 价值分析

**对个人开发者/研究者**：IMO Bench 是免费可用的高质量数学推理基准，可直接用于论文中的模型评估。Aletheia 的 prompt 设计思路对构建自己的数学推理 Agent 有参考价值，但由于依赖 Gemini Deep Think，无法直接复用。

**对企业/AI 实验室**：IMO Bench 可作为内部模型迭代的高难度评估标准，帮助识别推理能力的瓶颈。GradingBench 对开发数学教育产品（自动批改证明题）有直接商业价值。但需注意数据集规模有限（400+60+1000），不足以单独支撑大规模训练。
