# 关闭记录：PR #222 异地H结算文本泄漏（2026-07-17）

## 结局

PR #222（修复异地干员的绝顶等 H 结算文本错误地显示给玩家，head `cb92c64cf`）于
2026-07-17 被上游关闭且**未合并**。维护者在同日以自己的方式修复了同一问题域：
`upstream/master` 提交 `97c35826e`（"修正：修正了部分异地的二段行为结算被错误跳过的BUG"）。

## 上游方案与本 PR 方案的差异

- **本 PR**：异地角色照常结算二段行为，但在口上触发处与 `Second_effect.py` 四个绘制点
  （榨乳机 404、采尿器 405、绝顶喷乳 406、绝顶漏尿 407、额外绝顶 408）加
  `handle_in_player_scene` 门禁，抑制向玩家的绘制。
- **上游**：从 `second_behavior_effect` 的异地门禁中删去 `second_behavior_list == []`
  条件，使异地角色（含 orgasm_list/mark_list 定向结算调用）一律提前走
  `must_show_talk_check` + `must_settle_check` 通道后返回，普通二段行为的效果函数
  根本不会被调用。

## 覆盖验证（2026-07-17）

- 泄漏绘制效果 404–408 均不挂在任何含 997（must-settle）的行为上（对
  `data/csv/Behavior_Effect.csv` 全表核验），因此异地角色在上游新逻辑下不可能触发
  这些绘制——泄漏被"阻止结算"而非"抑制绘制"所覆盖。
- 口上侧由 must_show（998）通道覆盖。
- 残余语义差异：刚离开玩家场景的角色（`behavior.move_src` 仍为玩家位置）上游按在场
  处理、全量结算并绘制；本 PR 会抑制其绘制。这是维护者选择的语义，接受之。

## 处置

- 本地不再保留 PR #222 的代码（2026-07-17 的 rebase-fork-to-upstream 运行把基线换为
  `upstream/master (97c35826e)` + 仅 PR #221）。
- 对应的本地组件 `local_h_orgasm_batch_fix` 已于 2026-07-16 删除，无需恢复。
