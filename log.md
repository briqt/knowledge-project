# 维护日志

### 2026-07-10 上游 OKF 巡检基线 @ai

**进展**：OKF spec 仍为 v0.1 Draft，自 2026-06-12 导入后未变，无 spec 变更合并；上游活跃在提案/讨论（~30 issue + 16 discussion）。
**决策**：格式层改名提案（`type`→`kind` #154、`log.md`/`index.md` 改名 #146/#164）互相冲突且零合并 → 观望，暂不改方法论里的默认约定。
**下一步**：方法论层值得盯——社区在独立收敛我们已有的机制（健康度 #120、置信/溯源 #160/#151/#140、durability #172）；#120 的 stable-ID 张力是唯一够格触发 Meta-Iteration 的信号。

### 2026-07-10 仓库开始 dogfood 自身方法论 @ai

**进展**：补齐 `CLAUDE.md`/`AGENTS.md`/`log.md`，让本仓库用自己的方法论维护自己；README 加一句定位澄清（元技能、方法论本体在 `skills/`）。
**决策**：`CLAUDE.md` 不嵌种子块——完整方法论就在同仓库 `skills/SKILL.md`，直接引用避免双份漂移。
**下一步**：B（stable-ID 的 Meta-Iteration proposal）待用户单独决策后启动。
