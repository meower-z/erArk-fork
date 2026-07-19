## Why

`remote-plural-orgasm-settlement`（PR #215）只用 `997` 标记静默结算了多重绝顶的汇总口上，并明确把 `extra_orgasm`、`b_orgasm_to_milk`、`u_orgasm_to_pee` 等直接绘制文本的效果列为"本 change 后仍存在的已知缺陷"。实际游玩中这些遗漏点仍会泄漏：玩家不在场时，异地干员的逐部位绝顶口上、连续额外绝顶、B绝顶喷乳、U绝顶漏尿，以及搾乳机/采尿器的每回合产出文本仍会插进玩家界面——玩家做完一次与之无关的移动后，会看到别处干员的这些结算文本（每条还是需要点击翻过的等待）。

根因：`second_behavior_effect` 顶部的远程门只在传入的二段行为列表为空时生效；高潮/刻印以非空列表单独调用它（`check_second_effect` 行101/106），绕过了这道门，于是绝顶类口上照常绘制。若干效果处理器各自直接绘制，同样没有"玩家是否在场"判断。游戏在其他同类结算处已用 `handle_premise.handle_in_player_scene` 门控绘制（人力发电、猥亵道具、`Second_effect` 中另外四个处理器）；这些泄漏点只是遗漏了这道既有的门。

## What Changes

- 在 `second_behavior_effect` 的 `handle_second_talk` 调用处补上"玩家在场"判断（与顶部远程门同一 position/move_src 判定，且豁免 `998` 必须显示行为），使异地干员的绝顶类口上不再绘制。
- 给 `handle_extra_orgasm`、`handle_b_orgasm_to_milk`、`handle_u_orgasm_to_pee`、`handle_milking_machine`、`handle_urine_collector` 的绘制处补上同一在场门。
- 所有抑制只挡绘制，不影响数值/资源/记录结算（苦痛恐怖数值、乳汁/圣水入库均照常）。
- 明确保留远程显示：刻印升级（永久改变干员能力）与多重绝顶成就（解锁蚀刻章）有持久影响，异地照常显示，不在收敛范围内。

## Capabilities

### New Capabilities

- `remote-orgasm-display-leaks`: 规定异地干员瞬时绝顶类衍生显示按玩家在场门控、而持久影响事件（刻印升级、成就）与必须显示行为照常远程显示的行为。

### Modified Capabilities

None.

## Impact

修改 `Script/Design/second_behavior.py` 与 `Script/Settle/Second_effect.py`（各补既有的 `handle_in_player_scene` 门；只挡绘制）。不改 CSV，不改 `achievement_panel.py`（成就异地照常显示）。对应上游 PR #222（`Godofcong-1/erArk`）。
