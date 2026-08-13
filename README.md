# knowledge-project

一个 skill，指导你的知识项目如何自我维护：用 markdown + frontmatter 约定文件结构、元数据、工作日志和迭代流程，使项目目录对人和 AI Agent 都可读可续、跨 session 可接续。

方法论本体在 [`skills/SKILL.md`](skills/SKILL.md)（安装后由 Agent 加载运行）；格式底座基于 [OKF v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)。

## 安装

```bash
npx skills add briqt/knowledge-project -g -y
```

## 包含什么

一个 SKILL.md，约定了：

- **项目结构**：最小 3 文件（CLAUDE.md + log.md + 内容），按规模渐进扩展；规则变多时分常驻/任务/理由三层加载
- **Frontmatter**：OKF 兼容，`type` 必填，其余按需
- **工作日志**（log.md）：追加式记录进展/决策/下一步，跨 session 恢复上下文
- **决策记录**：多方案取舍时记录理由，内联到相关文档
- **Seed 与自足档位**：核心规则内联进项目，产出物不反向依赖本 skill——skill 不在场也照常工作
- **Distill 流程**：从探索阶段的临时产物中蒸馏出值得保留的部分
- **Self-Iteration**：项目结构的自我改进触发条件和流程，含规则的准入/退出与门禁有效性
- **Meta-Iteration**：方法论本身的改进机制

## 适用于

需要跨多次 session 持续推进的知识工作：文档仓库、研究课题、写作项目、技术方案等。

## License

MIT
