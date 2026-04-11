# microsoft/markitdown - 为 LLM 优化的文档转 Markdown 工具

**GitHub**: https://github.com/microsoft/markitdown  
**Stars**: 99,707 ⭐  
**类型**: Python 工具库  
**发布日期**: 2026-04-11

---

## 📋 项目概述

MarkItDown 是 Microsoft 开源的轻量级 Python 工具，专门用于将各种文件格式转换为 Markdown，以便 LLM 和文本分析管道使用。与传统的文档转换工具（如 textract）不同，MarkItDown 专注于保留重要的文档结构和内容（标题、列表、表格、链接等），同时保持 Markdown 的简洁性。

### 核心特点

- **LLM 优化**: 输出格式专为 LLM 消费设计，而非人类阅读
- **广泛格式支持**: PDF、PowerPoint、Word、Excel、图片、音频、HTML、CSV、JSON、XML、ZIP、YouTube、EPub 等
- **零依赖核心**: 基础功能无需额外依赖
- **模块化设计**: 可选依赖按需安装
- **MCP 集成**: 提供 Model Context Protocol 服务器

---

## 🎯 为什么选择 Markdown？

1. **接近纯文本**: 最小化标记，保持可读性
2. **LLM 原生支持**: GPT-4o 等主流模型"原生说 Markdown"
3. **Token 高效**: Markdown 约定高度 token 高效
4. **结构保留**: 在简洁性和结构性之间取得平衡

---

## 🚀 支持的格式

### 文档类

- **PDF**: 文本提取 + 可选 OCR（通过插件）
- **PowerPoint (.pptx)**: 幻灯片内容 + 可选图片描述（LLM Vision）
- **Word (.docx)**: 文档结构 + 内容
- **Excel (.xlsx, .xls)**: 表格数据

### 媒体类

- **图片**: EXIF 元数据 + OCR + LLM 图片描述
- **音频 (.wav, .mp3)**: EXIF 元数据 + 语音转录

### 结构化数据

- **HTML**: 网页内容提取
- **CSV/JSON/XML**: 结构化数据转换
- **ZIP**: 递归处理压缩包内容

### 其他

- **YouTube URLs**: 视频转录
- **EPub**: 电子书内容
- **Outlook 邮件**: 邮件内容提取

---

## 💡 核心功能

### 1. 模块化依赖

```bash
# 安装所有功能
pip install 'markitdown[all]'

# 按需安装
pip install 'markitdown[pdf, docx, pptx]'
```

可选依赖组：
- `[pptx]` - PowerPoint
- `[docx]` - Word
- `[xlsx]` - Excel
- `[xls]` - 旧版 Excel
- `[pdf]` - PDF
- `[outlook]` - Outlook 邮件
- `[az-doc-intel]` - Azure Document Intelligence
- `[audio-transcription]` - 音频转录
- `[youtube-transcription]` - YouTube 转录

### 2. LLM Vision 集成

```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(
    llm_client=client, 
    llm_model="gpt-4o",
    llm_prompt="optional custom prompt"
)
result = md.convert("example.jpg")
print(result.text_content)
```

### 3. Azure Document Intelligence

```bash
markitdown path-to-file.pdf -o document.md -d \
  -e "<document_intelligence_endpoint>"
```

### 4. 插件系统

**markitdown-ocr 插件**：
- 为 PDF、DOCX、PPTX、XLSX 添加 OCR 支持
- 使用 LLM Vision 提取嵌入图片中的文本
- 无需额外 ML 库或二进制依赖

```python
from markitdown import MarkItDown
from openai import OpenAI

md = MarkItDown(
    enable_plugins=True,
    llm_client=OpenAI(),
    llm_model="gpt-4o",
)
result = md.convert("document_with_images.pdf")
```

### 5. MCP 服务器

MarkItDown 提供 MCP 服务器，可与 Claude Desktop 等 LLM 应用集成：

```bash
# 安装 MCP 服务器
npm install -g @markitdown/mcp

# 在 Claude Desktop 中配置
```

---

## 🔧 使用场景

### 1. RAG 管道

将企业文档转换为 Markdown，构建向量数据库：

```python
from markitdown import MarkItDown

md = MarkItDown()
documents = []

for file in ["report.pdf", "slides.pptx", "data.xlsx"]:
    result = md.convert(file)
    documents.append(result.text_content)

# 送入向量数据库
```

### 2. 文档分析

批量分析文档内容：

```bash
for file in *.pdf; do
    markitdown "$file" | llm "summarize this document"
done
```

### 3. 知识库构建

将各种格式的知识库文档统一转换为 Markdown：

```python
import os
from markitdown import MarkItDown

md = MarkItDown(enable_plugins=True)

for root, dirs, files in os.walk("knowledge_base"):
    for file in files:
        if file.endswith(('.pdf', '.docx', '.pptx')):
            path = os.path.join(root, file)
            result = md.convert(path)
            # 保存为 Markdown
            with open(f"{path}.md", "w") as f:
                f.write(result.text_content)
```

### 4. AI Agent 工具

作为 AI Agent 的文档读取工具：

```python
# 在 MCP 服务器中使用
# Claude Desktop 可以直接调用 MarkItDown 读取文档
```

---

## 🆚 与竞品对比

### vs textract

| 特性 | MarkItDown | textract |
|------|-----------|----------|
| 输出格式 | Markdown（结构化） | 纯文本 |
| LLM 优化 | ✅ | ❌ |
| 依赖管理 | 模块化可选 | 全量依赖 |
| 图片描述 | LLM Vision | ❌ |
| 音频转录 | ✅ | ❌ |
| MCP 集成 | ✅ | ❌ |

### vs pypandoc

| 特性 | MarkItDown | pypandoc |
|------|-----------|----------|
| 目标用户 | LLM/AI 管道 | 人类阅读 |
| 格式保真度 | 适度（LLM 友好） | 高（人类友好） |
| Token 效率 | 高 | 中 |
| 安装复杂度 | 低 | 高（需 Pandoc） |

---

## 📊 技术架构

### 核心设计

1. **DocumentConverter 接口**: 统一的文档转换接口
2. **流式处理**: 从文件流读取，无临时文件
3. **插件系统**: 可扩展的转换器
4. **渐进式增强**: 基础功能 + 可选增强

### 0.0.1 → 0.1.0 重大变更

- **依赖重组**: 按功能分组的可选依赖
- **流式 API**: `convert_stream()` 现在需要二进制流
- **DocumentConverter 重构**: 从文件路径改为文件流

---

## 🎯 适用场景

### ✅ 适合

- RAG 系统的文档预处理
- LLM 应用的文档读取
- AI Agent 的文档工具
- 批量文档分析
- 知识库构建

### ❌ 不适合

- 高保真文档转换（供人类阅读）
- 复杂排版保留
- 精确格式还原

---

## 🔮 未来展望

### 潜在发展方向

1. **更多格式支持**: Notion、Confluence、Google Docs
2. **增强 OCR**: 更好的表格识别、公式提取
3. **多模态理解**: 图表、图形的语义理解
4. **流式输出**: 大文档的流式 Markdown 生成
5. **缓存优化**: 重复文档的转换缓存

### 生态系统

- **MCP 服务器**: 与更多 LLM 应用集成
- **插件市场**: 社区贡献的转换器
- **云服务**: 托管的文档转换 API

---

## 💼 商业价值

### 对企业

- **降低 RAG 成本**: 统一的文档预处理管道
- **提升 AI 效率**: LLM 友好的输入格式
- **简化集成**: 零依赖核心 + 模块化扩展

### 对开发者

- **快速原型**: 几行代码实现文档读取
- **灵活扩展**: 插件系统支持自定义转换器
- **生态兼容**: MCP 协议集成主流 AI 工具

---

## 🎓 学习资源

- **官方文档**: https://github.com/microsoft/markitdown
- **PyPI**: https://pypi.org/project/markitdown/
- **MCP 服务器**: https://github.com/microsoft/markitdown/tree/main/packages/markitdown-mcp
- **示例插件**: https://github.com/microsoft/markitdown/tree/main/packages/markitdown-sample-plugin

---

## 🏆 关键洞察

1. **Markdown 是 LLM 的通用语**: 主流模型都"说"Markdown
2. **模块化优于全量**: 按需安装依赖降低复杂度
3. **流式优于批量**: 无临时文件提升性能
4. **插件优于内置**: 社区扩展优于官方全包
5. **MCP 是未来**: 标准化的 AI 工具协议

---

**总结**: MarkItDown 是 Microsoft 为 AI 时代打造的文档转换工具，专注于 LLM 友好的 Markdown 输出。其模块化设计、插件系统和 MCP 集成使其成为构建 RAG 系统和 AI Agent 的理想选择。随着 AI 应用的普及，这类"AI 原生"工具将成为基础设施的重要组成部分。
