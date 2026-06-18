# Knowledge Project

自描述的知识项目管理方法论。让项目本身携带完整上下文——换 session、换 Agent、换人，打开就能继续。

## 安装

```bash
npx skills add briqt/knowledge-project -y -g
```

## 解决什么问题

你用 AI Agent 做各种事——写作、调研、写代码、管项目。积累了想法、经验、数据，但每次开新会话都在重建上下文："上次做到哪了？为什么选了这个方案？下一步干什么？"

这个 skill 定义了一套轻量规范：用 markdown + frontmatter 组织项目，让任何 Agent（Claude Code、Codex、OpenClaw…）打开项目目录就能理解全局并继续工作。不依赖特定平台或记忆服务，纯文件 + 约定。

## 核心机制

| 机制 | 做什么 |
|------|--------|
| OKF frontmatter | 文档自描述——type、description、tags，Agent 不读全文就能判断相关性 |
| log.md | 跨 session 上下文——进展、决策、阻塞、下一步，新 session 读尾部即可恢复 |
| 决策记录 | 可追溯——为什么选 A 不选 B，内联到相关文档 |
| Distill 流程 | 探索→沉淀——从试错中蒸馏出成果、路径、教训，丢弃噪音 |
| Self-Iteration | 自我改进——项目感知结构摩擦并提出优化 |

## 适用场景

- 团队文档仓库（如产品需求 + 设计文档 + 项目管理）
- 个人研究课题（调研→实验→结论的完整过程）
- AI 驱动的写作项目（世界观、大纲、章节、方法论）
- 任何需要跨多次 session 持续推进的工作

## 格式基础

基于 [Open Knowledge Format (OKF) v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)——Google 提出的开放知识表示格式。OKF 的核心就是 markdown + YAML frontmatter，零额外成本。

## License

MIT
