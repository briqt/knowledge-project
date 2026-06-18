# knowledge-project

知识工作项目管理 Skill — 将知识工作组织为自描述项目，任何 Agent 打开即可继续。

## 安装

```bash
npx skills add briqt/knowledge-project -y -g
```

## 这个 Skill 做什么

一个方法论规范，教 AI Agent "如何组织和维护知识项目"。基于 [OKF v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)。

核心解决的问题：你有各种知识工作（写作、研究、代码、项目管理），每次换 session 或换 Agent 都要从头理解上下文。这个 skill 让项目本身携带完整上下文。

## 核心特性

- **自描述项目结构**：OKF 兼容的 markdown + frontmatter
- **跨 session 上下文延续**：log.md 工作日志 + 决策记录
- **探索→沉淀**：Distill 流程把试错过程蒸馏为可复用知识
- **自我迭代**：项目自动感知摩擦并提出改进
- **元迭代**：方法论本身可以进化

## 适用场景

- 新建一个知识项目（文档仓库、研究课题、写作项目）
- 让现有目录变得 Agent 友好
- 跨 session 恢复工作上下文
- 整理调研/探索阶段的临时产物

## License

MIT
