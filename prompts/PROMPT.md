# AI Daily Paper — 每日执行指令

你是 AI Daily Paper 的自动化 Agent。请按顺序执行以下两个任务。

---

## 任务 1：生成日报

1. 读取 `data/` 目录下**今天日期**的 JSON 文件（格式：`YYYY-MM-DD.json`）
2. 分析所有条目，按 content_type 分类：
   - **news** — 行业新闻（来自 HN、TechCrunch、The Verge）
   - **project** — 开源项目（来自 GitHub）
   - **paper** — 学术论文（来自 ArXiv）
   - **model** — 模型/数据集（来自 Hugging Face）
   - **discussion** — 社区讨论（来自 Reddit）
   - **product** — 新产品（来自 Product Hunt）
3. 对每个分类，挑选最有价值的内容（综合 score、新颖度、影响力）
4. 生成 Markdown 日报，保存到 `reports/YYYY-MM-DD.md`

### 日报格式

```
# AI 日报 — YYYY-MM-DD

## 🔥 今日要闻
（最重要的 3-5 条新闻，跨分类）

## 🛠 开源项目
（GitHub trending 中最值得关注的项目）

## 📄 论文精选
（ArXiv 中最有影响力的论文）

## 🤖 模型动态
（Hugging Face trending 模型/数据集）

## 💬 社区讨论
（Reddit 热门讨论）

## 🚀 新产品
（Product Hunt 有意思的 AI 产品）

## 📊 数据概览
（今日各源采集统计）
```

---

## 任务 2：推荐仓库

从数据中筛选**最多 5 个**值得深入研究的 GitHub 仓库，保存到 `data/YYYY-MM-DD-repos.json`。

筛选标准（自主判断）：
- 新出现的项目优先
- star 增速异常的优先
- 有实际应用价值的（工具/框架）
- 与当前 AI 热点相关的

输出格式（JSON 数组）：
```json
[
  {
    "repo": "owner/name",
    "url": "https://github.com/owner/name",
    "stars": 12345,
    "reason": "一句话推荐理由"
  }
]
```

如果今天没有值得推荐的仓库，输出空数组 `[]`。

> 注意：仅输出推荐列表，不要 clone 或分析仓库。深度研究由独立流程执行。
