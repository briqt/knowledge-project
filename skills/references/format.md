# 文件格式

> 何时读：写 frontmatter、log 条目、决策记录，或对照 OKF 检查格式。

## Frontmatter Schema

遵循 OKF v0.2 字段约定。

```yaml
---
type: 架构设计                     # 必填（OKF 唯一必填），概念类型，自由文本
description: 一句话摘要             # 推荐，Agent 判断相关性
tags: [tag1, tag2]                # 推荐，跨目录检索
generated:                        # 推荐，取代 v0.1 的 timestamp
  by: human:alice                 #   actor：human:<id> 或 <产出者>/<版本>
  at: 2026-08-13T10:00:00+08:00   #   最后实质修改（ISO 8601，带时区偏移）
status: stable                    # 可选，draft | stable | deprecated（缺省 stable）
verified:                         # 可选，谁复核过
  - { by: human:alice, at: 2026-08-13T18:00:00+08:00 }
---
```

**规则：**
- `type` 是唯一必填字段，值为自由文本
- 只写有值的字段，宁缺勿空
- 无 frontmatter 时 Agent 从标题和正文推断，不报错
- **actor 约定**：`human:<id>` 表示人，`<产出者>/<版本>` 表示 Agent 或工具。与 log.md 的 `@操作人` 是同一套身份语义
- **`generated` 取代 `timestamp`**：旧文档的 `timestamp` 仍可读（OKF 允许回退），新写文件与顺手更新时改用 `generated`。迁移旧文档时 actor 无从确认就保留 `timestamp`，不编造 `generated.by`——读旧文档做宽容消费者，自己写入做严格生产者
- **`status: deprecated`** 是"归档即关闭"的元数据表达（见 [structure.md §归档即关闭](structure.md)）
- **`verified` 决定可信档**：无该字段 = 未复核；仅非 human actor = 机器确认；含 `human:<id>` = 人已复核。这与"门禁分层"（见 [governance.md §从教训到规则](governance.md)）是同一个区分——可机械校验的由机器确认，只能语义判断的须人复核
- **时间字段一律带时区偏移**：`generated.at`、`verified[].at`、`stale_after`、`sources[].last_modified`、`usage_window` 都写成 `2026-08-13T10:00:00+08:00` 这种形式。只写日期的值，严格的消费者会直接忽略——`stale_after: 2026-12-31` 等于没写。迁移只有日期的旧值时，补 `T00:00:00` 加项目所在时区的偏移；时区无从确认就问，不默认 `Z`。log 的日期标题不是字段值，不在此列
- **`index.md` 不带 frontmatter**，唯一例外：项目根 index.md 可写 `okf_version: "0.2"`
- **其余可选族按需采用**：`sources`（来源清单，正文逐条归因用与 `sources[].id` 同名的脚注；v0.1 的正文 `# Citations` 迁入此字段，无法核实的条目标注待核验）、`stale_after`（绝对过期时刻）。研究型项目值得用；不写不违规，写就只写已核实的值——来源、actor、时间、核验一律不伪造
- 概念之间的关联用正文里的标准 markdown 链接表达，不另设 frontmatter 字段——OKF 工具按正文链接建关系图

## 与 OKF 的显式分歧

以下三处有意偏离 OKF，理由记在此处，不静默违反：

| 处 | OKF | 我们 | 理由 |
|----|-----|------|------|
| `log.md` 顺序与格式 | 日期分组、**最新在前**、条目为散文 | **最新在底部**（append-only）、条目为四字段结构 | append-only 的 diff 只在末尾增长、冲突少；"下一步"恒定落在文件末尾，是 session 接力的取用点 |
| `AGENTS.md`/`README.md` 的 frontmatter | 非保留名 ⇒ 要求有 frontmatter | 不带 | 它们是 harness 契约文件（面向运行时的 Agent 与人），不是知识 concept |
| Attested Computation（OKF §10） | 可选族 | 不采用 | 面向可执行的数据口径，超出知识项目范围 |

`log.md` 的日期标题统一用 `###`，不与 `##` 混用——混用会让任何按标题定位条目的检查失效。

## log.md（工作日志）

```markdown
### YYYY-MM-DD 事项名称 @操作人

**进展**：本次完成了什么
**决策**：做了什么选择、为什么（无则省略）
**阻塞**：卡在什么上（无则省略）
**下一步**：接下来该做什么
```

**规则：**
- 一条 = 一次实质进展，没有实质内容不写
- 每条不超过 5 行
- 最新在底部（append-only，git diff 友好）
- `@操作人` 用 git 用户名，AI Agent 用 `@ai`
- `下一步` 是 session 接力的核心机制——写法标准：一个新 Agent 只读这一条就知道该做什么
- **归档阈值 = 装得下 Resume 所需的最近窗口**（约 2-3 天或 10-15 条），默认 200 行。条目密度高的项目按此上调并在 AGENTS.md 写明覆盖值——阈值卡在绝对行数上会把接力需要的上下文一起归档掉
- **归档做法**：旧条目原样移到 `log-archive/<年份>.md`（同样最新在底部），log.md 只留最近窗口；最后一条的"下一步"永远留在 log.md

## 决策记录

内联到相关文档末尾的 `## 决策记录` 章节。

```markdown
### YYYY-MM-DD 结论短语

**背景**：面临什么选择
**结论**：选了什么
**理由**：为什么
**排除**：为什么不选其他方案
```

只记有多个可行方案的决策。排除理由必写。
