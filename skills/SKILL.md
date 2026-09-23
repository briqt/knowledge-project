---
name: knowledge-project
description: >-
  让知识工作项目对 Agent 自描述、跨 session 可接续，并治理项目里的规则与工作纪律。
  两类场景使用：（一）项目组织——新建或初始化项目、整理或健康检查项目结构、
  设计目录与导航、写 frontmatter/index/log/决策记录、把探索期的临时文件沉淀下来、
  恢复一个还没有规则文件的项目的上下文；（二）工作方法论——同类问题反复出现要固化成规则、
  规则太多或互相冲突要精简、新增或删除一条项目规则、给项目立检查脚本或门禁并判断它是否有效、
  沉淀经验教训、回顾或改进方法论本身。触发词：新建项目、初始化文档结构、帮我整理这个项目、
  项目怎么组织、健康检查、又踩坑了、固化成规则、规则太多、精简规则、门禁、检查脚本、
  沉淀、蒸馏、经验教训、决策记录、回顾方法论、setup project、project health check。
---

# Knowledge Project

将知识工作组织为自描述项目——任何 Agent 打开即可理解和继续，无需外部记忆系统；并让项目里的规则随工作演化，而不是膨胀到没人遵守。

**本文件是常驻层**：每次触发都成立的原则、纪律与路由。具体做法按 §路由 读 `references/` 下的对应文件，只读本次意图需要的那几个。

## Philosophy

**核心理念**：项目本身携带完整上下文。不依赖特定平台、记忆服务或对话历史。

**设计原则：**

1. **纯文件 + 约定**：markdown + YAML frontmatter，零工具依赖，git 友好
2. **自包含**：每个文档独立可理解，项目整体打开即可继续
3. **最小约束**：只规定互操作必需的结构，其余由项目自行演化
4. **写的人花 2 分钟，读的人省 20 分钟**：信息密度优先，格式服务检索
5. **单一权威源**：规则只在一处定义，其他文件引用不复述

**格式基础**：[Open Knowledge Format (OKF) v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md) —— 知识用 markdown + YAML frontmatter 目录表示，人和 Agent 用同一份文件。字段约定与有意偏离见 [format.md](references/format.md)。

**底线**：项目目录是唯一的持久化载体。换 Agent、换平台、清空记忆、**本 skill 未安装**，打开项目目录即可继续。

## 硬约束

- **项目文件即记忆**：项目的所有上下文落在项目文件中（CLAUDE.md/AGENTS.md、log.md、内容文件），不写入 Agent 自身的 memory。
- **产出物不得反向依赖、不得引用本 skill**：由本方法论创建或维护的项目，其自足性不得以"本 skill 在场"为前提；项目文件中不出现本 skill 的名字，也不留指向任何外部方法论的指针——**无例外**。判据与理由见 [seed.md §关键约束](references/seed.md)。
- **进展随工作落地**：进展、决策、文件元数据随工作产生同步写入。最终检验：结束工作时，log.md 最后一条的"下一步"足以让任意 Agent 从零接手。
- **改进走 proposal**：诊断 → 提案 → 用户确认 → 执行 → 记录到 log。

## Epistemics

知识工作的认知纪律。贯穿所有工作流，优先级高于具体流程步骤。第 1、3 条以精简版内联进种子、第 4 条对应种子的"感知偏差与对齐"——本 skill 未被触发时，项目照样遵守。

1. **基于证据**：判断、选择、结论须追溯到可观测的依据。没有证据时承认不确定，而非填充看似合理的假设。委派或其他 Agent 的产出同样是候选输入而非既定事实——引用它做不可逆动作（删除、归档、改权威源）前先复核源头。
2. **在行动点决策**：不提前锁定依赖未知信息的决定。确定方向，开始行动，让工作本身产生下一个决策点。
3. **完整执行**：不跳步骤，不用"以此类推"代替实际工作。产出是做出来的，不是规划出来的。
4. **对齐优先于执行**：目标有歧义、存在矛盾、或涉及方向性取舍时，先澄清再行动。推断可以替代追问，但推断必须显式呈现供纠正——不用默认值静默填充。

## 路由

按意图只读需要的文件，顺序即阅读顺序：

| 意图 | 读 | 要点 |
|------|----|------|
| 创建新项目 | [workflows.md §Initialize](references/workflows.md) → [structure.md](references/structure.md) → [seed.md](references/seed.md) → [format.md](references/format.md) | 选规模、写规则文件并内联种子、建 log 与首个内容文件 |
| 恢复/继续项目 | 本文件 §Resume | 已有种子的项目按它自己的 CLAUDE.md/AGENTS.md 执行即可 |
| 整理、优化、健康检查 | [workflows.md §Health Check](references/workflows.md) | 按诊断结果转 Milestone Review 或 Distill（同文件） |
| 日常维护：写 log、frontmatter、决策记录，关闭事项 | [workflows.md §Daily Operations](references/workflows.md) → [format.md](references/format.md) | |
| 沉淀探索期产物 | [workflows.md §Distill](references/workflows.md) | |
| 规划文件组织、判断一条信息该写在哪 | [structure.md](references/structure.md) | |
| 新增/删除/固化规则、规则膨胀、立门禁或评估门禁 | [governance.md](references/governance.md) | |
| 回顾或改进方法论本身 | [governance.md §Meta-Iteration](references/governance.md) | 须用户显式触发 |

除 Resume 外，触发时顺带对照 Health Check 清单扫描项目现状，发现可改进项时向用户提出。

## Resume

新 session 阅读协议：

1. CLAUDE.md/AGENTS.md → 理解项目结构和约定
2. 任务路由表（如有）→ 按本次任务加载对应的任务层规则
3. 任务清单（如有）→ 知道当前活跃任务
4. log.md 尾部 5-10 条 → 知道最近进展和阻塞
5. 进入具体工作

若 log 描述与当前文件实际状态冲突，以文件为准，更新过时描述。

## 日常感知

在项目中工作时，持续感知结构摩擦并推动改进：

- 发现规则与实际操作不一致 → 提出 CLAUDE.md/AGENTS.md 修改建议
- 发现导航不够高效 → 提出结构调整
- 发现重复模式 → 提出新规则或模板（新增前先过 [governance.md §规则的准入与退出](references/governance.md)）

何时启动正式的结构性迭代，见 [governance.md §Self-Iteration](references/governance.md)。

## Boundaries

**不是**：
- 记忆系统（不做向量检索、不跨项目同步状态）
- 重编排 / 多 agent 调度器——但轻量结构化任务资产（复杂事项拆 需求/设计/实施清单/决策记录）是标准项目的一等组成，见 [structure.md §Customization](references/structure.md)
- git 的替代品（版本管理就是 git）
- 强制模板（最小约束，项目自行演化）

**是**：
- 方法论指南（告诉 Agent "如何组织知识项目"）
- 结构规范（OKF 兼容的文件约定）
- 生命周期管理（从创建到归档的过程定义）
- 自我改进框架（项目和方法论都能迭代）
