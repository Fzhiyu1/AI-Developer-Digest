# microsoft/markitdown

> Python tool for converting files and office documents to Markdown.

- **仓库**: https://github.com/microsoft/markitdown
- **Stars**: 104,690 ⭐
- **语言**: Python
- **标签**: markdown, pdf, microsoft-office, langchain, openai, autogen

## 项目简介

MarkItDown 是微软开源的文档转 Markdown 工具，支持将 PDF、Word、Excel、PowerPoint、图片、音频、HTML、ZIP 等几乎所有常见格式转换为 Markdown 文本。设计目标是为 LLM 和 RAG 管道提供统一的文档预处理层。

## 核心功能

- 支持格式：PDF、DOCX、XLSX、PPTX、HTML、CSV、JSON、XML、图片（含 EXIF/OCR）、音频（转录）、ZIP
- 可选 LLM 增强：传入 `llm_client` 后，图片和音频会调用模型生成描述
- 插件系统：支持自定义转换器，可扩展新格式
- CLI 工具：`markitdown file.pdf` 直接输出 Markdown
- 与 AutoGen、LangChain 等框架深度集成

## 为什么值得关注

RAG 和 AI Agent 的核心痛点之一是文档解析。MarkItDown 提供了一个微软背书、格式覆盖最全的开源方案，10万+ Star 说明社区认可度极高。对于需要处理企业文档的 AI 应用，这是目前最省心的选择之一。

## 快速使用

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("document.pdf")
print(result.text_content)
```

```bash
# CLI
pip install markitdown
markitdown document.docx
```
