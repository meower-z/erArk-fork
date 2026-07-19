# Current status and stop rule

实现与验证已完成。上游 PR #222 处于 OPEN 未合并状态——这是外部状态，不是待办工作。本文件不留未勾选任务。

若未来仅被要求"继续本 change"，报告无可执行工作并停止。PR #222 仍 OPEN 时不要 archive 本 change。允许在用户明确要求时做一次只读的 PR 状态刷新。

## 1. 边界与基线

- [x] 1.1 记录上游基线（`upstream/master`）、渲染器（Tk, web_draw=0）、复现存档（save/5）、玩家可见症状（异地干员绝顶提示插入界面）
- [x] 1.2 建立可红测的复现：真实 `second_behavior_effect` / `handle_extra_orgasm`，断言异地不绘制、结算照常、`998` 刻印远程仍显示
- [x] 1.3 记录所选边界（design.md），并经 gpt-5.6-sol 独立审查

## 2. 实现

- [x] 2.1 基于 `upstream/master` 建 `codex/remote-orgasm-display-leak` worktree
- [x] 2.2 站点 A：`second_behavior_effect` 的 `handle_second_talk` 加复合在场门（含 must_show 豁免）
- [x] 2.3 站点 B–F：`Second_effect` 的 extra_orgasm / b_orgasm_to_milk / u_orgasm_to_pee / milking_machine / urine_collector 绘制处加 `handle_in_player_scene` 门
- [x] 2.4 按"影响深浅"裁定：刻印升级与多重绝顶成就异地照常显示（移除 mark 门、还原 `achievement_panel.py`）

## 3. 验证

- [x] 3.1 单元测试全通过；还原 base 后失败（红能力）
- [x] 3.2 固定种子真实 Tk 前后截图，存档路线前后 hash 未变
- [x] 3.3 上游 rebase（解 `handle_extra_orgasm` 与 upstream `8882a6a27` 的冲突：采用上游通用结算 + 本地绘制门）

## 4. 提交

- [x] 4.1 推送 `codex/remote-orgasm-display-leak` 到 `meower-z/erArk-fork`
- [x] 4.2 前后截图发布到 fork 的 append-only `assets` 分支，PR 用 commit-pinned raw URL
- [x] 4.3 开 PR #222 到 `Godofcong-1/erArk` base=master
