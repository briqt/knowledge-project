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
| `tests/test_repo_contract.py` | 维护本仓库的 Agent | 确定性仓库门禁（含证伪用例），不属于产品本体 |

本文件只讲"如何维护本仓库"；方法论细节一律看 `skills/SKILL.md`，不复述。

## 两类改动——动手前先分清

| | 改什么 | 影响范围 | 怎么做 |
|--|--------|----------|--------|
| **Self-Iteration** | 本仓库（README、结构、维护流程） | 只影响这个仓库 | 直接改，记 log |
| **Meta-Iteration** | 产品（`skills/SKILL.md` 的方法论） | 影响所有装了它的项目 | 显式触发 + proposal（诊断→提案→确认→执行）+ 记 log，git 可回退 |

一句话判断：动的是"这个仓库"，还是"卖出去的方法论"？

## Agent 行为规则

**自足性：完全自足**（三档制已于 2026-08-17 废除，见 SKILL §关键约束）——完整方法论就在同仓库 `skills/SKILL.md`，指向它是**仓内链接**而非外部依赖（零外部引用规则禁的是引用别人的方法论，不禁产品仓引用自己的产品本体），因此本文件**不嵌种子块**，直接遵循 SKILL.md 即可。关键几条：

- **不指名任何外部项目**：本仓公开。所有文件与提交信息一律不写外部项目/仓库名，只写类型描述（如"写作型项目"）
- **有实质进展就追加 `log.md`**："下一步"要写到任意 Agent 只读它就能接手
- **`CLAUDE.md` 与 `AGENTS.md` 内容保持一致**，改一个同步另一个
- **改产品走 Meta-Iteration**（见上表）
- **提交前跑 `python3 tests/test_repo_contract.py`**：双文件一致、SKILL frontmatter 与 YAML 示例可解析、种子模板零回引、无机器路径，机械可判项交给门禁
- Resume 顺序：本文件 → `log.md` 尾部 → 进入工作

## 上游依赖：OKF

方法论的**格式底座**是 [OKF v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)（frontmatter 字段、`index.md`/`log.md` 保留名、链接语义）。
OKF 只管格式；方法论层（Seed、自迭代、Epistemics 等）是本 skill 自己的，不随 OKF 变。
**有意偏离 OKF 的地方一律写进 `skills/SKILL.md` §与 OKF 的显式分歧**，不静默违反。
**每月巡检一次**上游有无影响我们的变更（上次基线与结论见 `log.md`）。
本仓是 skill 的分发容器，仓库根不宣称为 OKF bundle（见 SKILL §项目与 OKF bundle 的边界）；dogfood 的是方法论层（log、规则治理、Meta-Iteration），不强行给包装文件加 frontmatter。
