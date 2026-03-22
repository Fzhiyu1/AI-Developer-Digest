# aquasecurity/trivy

- 仓库：<https://github.com/aquasecurity/trivy>
- 简介：Find vulnerabilities, misconfigurations, secrets, SBOM in containers, Kubernetes, code repositories, clouds and more
- 主要语言：Go
- Stars：33408
- Forks：126
- Open Issues：233
- Watchers：199
- License：Apache-2.0
- 创建时间：2019-04-11T01:01:07Z
- 最近更新时间：2026-03-22T04:08:28Z
- 默认分支：main
- Topics：containers, devsecops, docker, go, golang, hacktoberfest, iac, infrastructure-as-code, kubernetes, misconfiguration, security, security-tools, vulnerability, vulnerability-detection, vulnerability-scanners
- 官方主页：https://trivy.dev

## 这是什么
Find vulnerabilities, misconfigurations, secrets, SBOM in containers, Kubernetes, code repositories, clouds and more

## 从 README 看它的核心能力
- Container Image
- Filesystem
- Git Repository (remote)
- Virtual Machine Image
- Kubernetes
- OS packages and software dependencies in use (SBOM)
- Known vulnerabilities (CVEs)
- IaC issues and misconfigurations


## 活跃度判断
- 仓库仍然活跃：最近更新时间是 2026-03-22T04:08:28Z。
- 最近 5 条提交显示维护节奏仍在继续，说明并非“挂名上榜”。
- 最新 release：v0.69.3（2026-03-03T13:14:48Z）

## 最近提交
- 2026-03-19T04:49:26Z — `fix: remove os.Stdout from wazero module config (#10403)`
- 2026-03-19T04:31:54Z — `chore(deps): bump the common group across 1 directory with 22 updates (#10408)`
- 2026-03-19T03:01:43Z — `chore(deps): bump google.golang.org/grpc from 1.78.0 to 1.79.3 (#10407)`
- 2026-03-18T09:28:43Z — `fix(flag): validate template file extension (#10296)`
- 2026-03-18T05:20:17Z — `fix(sbom): preserve Red Hat BuildInfo when scanning SBOMs without layer info (#10378)`

## 为什么今天值得关注
- Trivy 长期是云原生安全扫描的事实标准之一，今天上榜说明安全仍是开发者优先级。
- 对 AI 系统尤其重要的是：当 agent 开始操作代码仓库、容器镜像和 Kubernetes 时，漏洞、SBOM、配置漂移和密钥泄漏会成为默认问题。
- 它不是“AI 原生”工具，但正是 AI 工程落地时最需要补齐的一层。

## 可跟进方向
- 关注 Trivy 对 AI 代码仓库、模型镜像、MCP 服务与 agent 工作流的扩展支持。
- 如果后续 AI 开发平台把 Trivy 之类扫描器嵌入默认流水线，这会是很强的落地信号。
