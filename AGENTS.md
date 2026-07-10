# 仓库维护指南（knowledge-project）

## 这是什么

本仓库分发一个 skill：`skills/SKILL.md`。这个 skill 指导**别的**知识项目如何自描述、自维护。
仓库本身是分发和演化这套方法论的地方——我们让它 dogfood：用自己的方法论维护自己。

## 文件职责

| 文件 | 给谁 | 职责 |
|------|------|------|
| `README.md` | 使用者（人） | 定位、安装、适用场景 |
| `skills/SKILL.md` | 运行时的 Agent | **产品本体**：完整方法论，单一权威源 |
| `CLAUDE.md` / `AGENTS.md` | 维护本仓库的 Agent | 本文件：怎么维护这个仓库 |
| `log.md` | 维护者 | 维护进展与决策，跨 session 接续 |

本文件只讲"如何维护本仓库"；方法论细节一律看 `skills/SKILL.md`，不复述。

## 两类改动——动手前先分清

| | 改什么 | 影响范围 | 怎么做 |
|--|--------|----------|--------|
| **Self-Iteration** | 本仓库（README、结构、维护流程） | 只影响这个仓库 | 直接改，记 log |
| **Meta-Iteration** | 产品（`skills/SKILL.md` 的方法论） | 影响所有装了它的项目 | 显式触发 + proposal（诊断→提案→确认→执行）+ 记 log，git 可回退 |

一句话判断：动的是"这个仓库"，还是"卖出去的方法论"？

## Agent 行为规则

完整方法论就在同仓库 `skills/SKILL.md`，因此本文件**不嵌种子块**，直接遵循 SKILL.md 即可。关键几条：

- **有实质进展就追加 `log.md`**："下一步"要写到任意 Agent 只读它就能接手
- **`CLAUDE.md` 与 `AGENTS.md` 内容保持一致**，改一个同步另一个
- **改产品走 Meta-Iteration**（见上表）
- Resume 顺序：本文件 → `log.md` 尾部 → 进入工作

## 上游依赖：OKF

方法论的**格式底座**是 [OKF v0.1](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)（frontmatter 字段、`index.md`/`log.md` 保留名、链接语义）。
OKF 只管格式；方法论层（Seed、自迭代、Epistemics 等）是本 skill 自己的，不随 OKF 变。
定期巡检 OKF 有无影响我们的变更，基线与结论见 `log.md`。
