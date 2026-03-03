# AIRI - 自托管 AI 虚拟伴侣

**项目地址**: https://github.com/moeru-ai/airi  
**Stars**: 21,402 (+1,412 今日)  
**语言**: TypeScript  
**许可证**: Apache-2.0

---

## 一句话简介

自托管的 AI 虚拟伴侣/数字生命容器，支持实时语音对话、玩 Minecraft/Factorio，对标 Neuro-sama。

---

## 核心能力

### 🎮 游戏能力
- **Minecraft** - 完整支持
- **Factorio** - 开发中，已有 PoC 演示
- 实时语音对话 + 游戏操控同时进行

### 💬 多平台聊天
- Telegram
- Discord
- Web 界面

### 🧠 记忆系统
- 纯浏览器数据库支持（DuckDB WASM | pglite）
- Memory Alaya（开发中）

### 🎙️ 本地推理
- 纯浏览器 WebGPU 本地推理
- 支持 NVIDIA CUDA 和 Apple Metal 原生加速

---

## 技术栈

AIRI 从第一天起就基于 Web 技术构建：

| 技术 | 用途 |
|------|------|
| **WebGPU** | GPU 加速推理 |
| **WebAudio** | 音频输入输出 |
| **Web Workers** | 多线程处理 |
| **WebAssembly** | 高性能计算 |
| **WebSocket** | 实时通信 |

---

## 桌面版优势

虽然浏览器版本展示了 Web 技术的极限，桌面版默认使用原生加速：

- **NVIDIA CUDA** - Nvidia GPU 加速
- **Apple Metal** - Mac GPU 加速
- 基于 HuggingFace candle 项目
- 无需复杂依赖管理

---

## 为什么选择 Web 技术

1. **跨平台** - 浏览器、桌面、移动端（PWA 支持）
2. **易扩展** - 插件系统，社区可贡献功能
3. **灵活性** - TCP 连接等非 Web 功能可通过桌面版实现

---

## 灵感来源

深受 **Neuro-sama** 启发。Neuro-sama 是目前最好的 AI 虚拟主播，能玩游戏、聊天、与观众互动。但它是闭源的，直播结束后无法继续互动。

AIRI 提供另一种可能：**让你拥有自己的数字生命，随时随地，完全自主。**

---

## 寻找的贡献者

项目正在早期阶段，欢迎：

| 角色 | 相关技术 |
|------|---------|
| Live2D 建模师 | - |
| VRM 建模师 | - |
| VRChat 头像设计师 | - |
| 计算机视觉 | CV |
| 强化学习 | RL |
| 语音识别 | ASR |
| 语音合成 | TTS |
| ONNX Runtime | - |
| Transformers.js | - |
| vLLM | - |
| WebGPU | - |
| Three.js | - |
| WebXR | - |

---

## 快速开始

```bash
# 访问在线演示
https://airi.moeru.ai

# 加入 Discord 社区
https://discord.gg/TgQ3Cu2F7A
```

---

## 开发日志

- **2026.02.16** - DevLog 更新
- **2026.01.01** - DevLog 更新
- **2025.10.20** - DevLog 更新
- 更多见 [文档站](https://airi.moeru.ai/docs/en/)

---

## 为什么值得关注

这是一个**开源版的 Neuro-sama**，技术栈现代化（Vue.js + TypeScript），支持 WebGPU 本地推理，跨平台运行。对于对 AI 伴侣、虚拟主播、游戏 AI Agent 感兴趣的开发者，这是最好的学习和贡献项目。

项目还有一个完整的子项目组织 [@proj-airi](https://github.com/proj-airi)，涵盖 RAG、记忆系统、嵌入式数据库、图标、Live2D 工具等。

---

*研究日期: 2026-03-03*