# 维护日志

### 2026-07-10 上游 OKF 巡检基线 @ai

**进展**：OKF spec 仍为 v0.1 Draft，自 2026-06-12 导入后未变，无 spec 变更合并；上游活跃在提案/讨论（~30 issue + 16 discussion）。
**决策**：格式层改名提案（`type`→`kind` #154、`log.md`/`index.md` 改名 #146/#164）互相冲突且零合并 → 观望，暂不改方法论里的默认约定。
**下一步**：方法论层值得盯——社区在独立收敛我们已有的机制（健康度 #120、置信/溯源 #160/#151/#140、durability #172）；#120 的 stable-ID 张力是唯一够格触发 Meta-Iteration 的信号。

### 2026-07-10 仓库开始 dogfood 自身方法论 @ai

**进展**：补齐 `CLAUDE.md`/`AGENTS.md`/`log.md`，让本仓库用自己的方法论维护自己；README 加一句定位澄清（元技能、方法论本体在 `skills/`）。
**决策**：`CLAUDE.md` 不嵌种子块——完整方法论就在同仓库 `skills/SKILL.md`，直接引用避免双份漂移。
**下一步**：B（stable-ID 的 Meta-Iteration proposal）待用户单独决策后启动。

### 2026-07-10 Meta-Iteration：任务清单状态列纳入派生视图纪律 @ai

**进展**：据外部项目反馈（内容文件已完结、台账状态列仍「进行中」的假活跃），合入 `skills/SKILL.md` 三处——Context System 声明完成状态为派生量；Health Check、Daily Operations 各加一行状态一致性检查。
**决策**：采「派生视图对齐源头」框架（复用 index.md 模式），未采反馈原案的「双写对账」；未改 Seed（非核心种子规则，不 bump seed-version）；1 数据点，依「无多项目验证则试行合入」直接合入。
**下一步**：留意后续项目是否覆盖此规则。

### 2026-07-13 Meta-Iteration：复发即固化 + 门禁分层 + 定位松半档 + 方法论changelog(可选) @ai

**进展**：合入 `skills/SKILL.md` 三处——① Self-Iteration 新增「从教训到规则：复发即固化(复发≥3→固化+全量扫存量) + 门禁分层(可机械校验→确定性检查·机器优先/语义类留人审·零工具止于清单)」；② 经验沉淀加「方法论 changelog(可选)」；③ Boundaries「任务管理工具」改写为「重编排/多agent调度器才外包，轻量结构化任务资产是标准项目一等组成」+ Customization 追加轻量任务资产段。
**决策**：源自三项目独立收敛的反哺（novel-forge + post-forge + my-workspace 均现「3次固化」「机器结论优先」）；经渐进验证先在 post-forge/my-workspace 局部试行无摩擦（见各仓 log 2026-07-13）。**方法论 changelog 定为可选**——my-workspace(任务执行型)试行判定不适配、log.md 已够，故非默认。**定位只松半档**：明确重编排/多 agent 不是 kp 的活，仅把轻量任务资产收为一等（不越界成任务管理器）。**未改 Seed**（新增均非核心种子规则，不 bump seed-version）。**押后**：归档即关闭（post-forge 侧 2026-07-13 刚试行，熟化几天后单独合）。
**下一步**：观察 npx 装机项目是否覆盖新规则（尤门禁分层「机器优先」在纯文件项目是否被判过重）；归档即关闭 熟化后走下一轮。

### 2026-07-13 Meta-Iteration：Customization 范例去除私有仓引用 @ai

**进展**：`skills/SKILL.md` Customization 表两行（写作项目/软件项目）的「说明」列曾指名两个作者私有仓——对使用者而言不存在，是悬空引用（含在公开仓里也等于泄露私有项目名）。改为自解释描述（「方法论/角色/知识/作品四层分离」「按需求→设计→信息职责边界分层」），与研究/知识库两行的自足风格对齐。
**决策**：范例应自解释、不外链具体项目；未改 Seed（非核心规则，不 bump seed-version），CLAUDE/AGENTS 无涉、保持一致。
**下一步**：无。开源 skill 范例应始终自足，后续新增范例沿用此原则。
