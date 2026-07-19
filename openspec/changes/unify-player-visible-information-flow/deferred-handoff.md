# 暂缓与恢复记录

## 暂缓决定

用户于 2026-07-14 判断本重构短期不值得投入时间精力，因此暂停。该决定是优先级判断，不否定架构方向。除非用户以后明确恢复，不得开始 Phase 0、apply、代码、测试、PR 或 maintainer 外发。

记录本 change 时，worktree 已有大量与本设计无关的未提交改动；本 session 只新增 `openspec/changes/unify-player-visible-information-flow/`。这是 2026-07-14 的工作区快照，恢复时必须重新运行 `git status`，不能假设仍然相同。

## 已保存内容

- `proposal.md`：动机、范围、breaking/no-mod 决策和 HOLD。
- `summary.md`：约 500 字的简短说明。
- `design.md`：完整职责边界、interface、风险、迁移和恢复条件。
- `specs/player-visible-information-flow/spec.md`：可测试的未来行为合同与显式 resume gate。
- `feasibility.md`：静态依据、live-cutover blockers、证据计划和审阅判定。
- `fable-review.md`：Fable `ACCEPT`/`KEEP` 的范围和结论。
- `tasks.md`：所有未来任务；1.2 的显式 user resume 是硬门。

OpenSpec 内的 Markdown 已保存全部实质内容。先前 `/tmp` HTML 只是一份可视化投影，没有独有的架构决定，因此不作为长期 source of truth。

## 历史来源

- 损坏 session ID：`019f5e04-88f2-7231-82d5-0fe0a05504fd`
- 本地 transcript：`/home/ubuntu/.codex/sessions/2026/07/14/rollout-2026-07-14T00-26-23-019f5e04-88f2-7231-82d5-0fe0a05504fd.jsonl`
- transcript 内置读取失败原因：约 42,999,806 字节处存在无效 UTF-8；尾部架构 turn 与 task completion 仍可恢复。

## 恢复顺序

1. 用户明确重新授权。
2. 对照当前代码重新验证 2026-07-14 的所有路径和行为事实。
3. 让 maintainer 重新确认职责边界、命名和方向。
4. 只执行 Phase 0 证据；不直接 live cutover。
5. Phase 0 blocker 全关后另行请求 live-cutover approval。

## Suggested skills

- `codebase-design`：复核 deep-module interface 与 deletion test。
- `improve-codebase-architecture`：代码漂移后重新扫描 producer/sink 图。
- `openspec-apply-change`：只有 1.2–1.4 全部满足时才能使用。
- `ponytail`：继续拒绝通用 event bus、持久 journal、replay 和 mod registry 等扩张。
