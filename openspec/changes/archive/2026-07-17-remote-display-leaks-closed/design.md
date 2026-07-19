# 设计记录：异地干员绝顶类结算绘制泄漏

## 违反的规则

玩家不在场（不与某干员同场景）时，该干员在H结算中产生的瞬时绝顶类文本不应绘制给玩家。这是 `remote-plural-orgasm-settlement`（#215）已确立、但只对多重绝顶汇总口上落实的规则；本 change 把它扩展到 #215 显式遗留的其余显示点。

## 根因

`check_second_effect` 对每个NPC（含异地）都会跑。`second_behavior_effect` 顶部（约行128）的远程门只在 `second_behavior_list == []` 时 return；而高潮与刻印以非空列表单独调用它（行101 `orgasm_list`、行106 `mark_list`），绕过该门 → 进入显示循环，行147 `handle_second_talk` 对远程干员照常绘制。效果处理器（`handle_extra_orgasm` 等）的文本在效果结算内部直接绘制，不经行147，需各自加门。

## 修复边界与谓词

既有约定即"逐点 `handle_premise.handle_in_player_scene` 门"（`store_power_by_human_power`、`mark_effect` 猥亵道具、`Second_effect` 中另外四个处理器都如此）。本 change 只是给漏掉的点补上同一道门，不新增 helper、不做 refactor。

- 站点 A（`second_behavior_effect` 行147 `handle_second_talk`）与顶部远程门同处一函数，用**同一复合谓词**：`position == 玩家 or move_src == 玩家 or 行为∈config_behavior_must_show_cid_list` 时才绘制。move_src 项保持"本回合刚从玩家处离开仍显示"的既有语义；must_show 项确保 `998` 行为（如能力面板手动升级刻印，直接以非空 list 调用、绕过 `must_show_talk_check`）不被误挡。
- 站点 B–F（`Second_effect` 的 extra_orgasm / b_orgasm_to_milk / u_orgasm_to_pee / milking_machine / urine_collector）与其本地兄弟一致，用 `handle_in_player_scene`。这些处理器都是"先结算后绘制"，门只加在绘制处，数值与资源结算在门之前、不受影响。

## 远程显示决定表（按影响深浅）

| 事件 | 远程显示 | 理由 |
|---|---|---|
| 逐部位/多重/额外绝顶口上、喷乳、漏尿、搾乳机、采尿器 | 否 | 瞬时、无持久影响、高频刷屏 |
| 刻印升级 | 是 | 永久改变干员能力；刻印行为本就 must_show |
| 多重绝顶成就 | 是 | 一次性持久解锁，非刷屏 |

（成就与刻印的远程显示为最终裁定：先曾用 `draw_notice` 参数让成就"记录但不弹"，后按"减少改动量+按影响深浅区分"撤销，`achievement_panel.py` 完全还原、`mark_effect` 门移除。）

## 已核实的安全性

- `must_show_talk_check` 显示后归零并清空列表，故常规结算路径中 `998` 行为永不经行147；站点 A 的 must_show 豁免是为覆盖能力面板等直接调用 `second_behavior_effect(target, [mark_id])` 的旁路。
- 射精面板绘制被 `if character_id == 0` 守卫（玩家专属），非泄漏。

## 独立审查

gpt-5.6-sol（codex）独立审查最初的候选（含成就 `draw_notice` + 刻印门），指出两点并已处理：成就整调用加门会连记录一起挡（记录属结算）；站点 A 会误伤经能力面板升级的 `998` 刻印口上。后按用户裁定进一步收敛为"成就/刻印异地照常显示"，两处审查问题随之消解。

## 验证

- 单元测试 `test_remote_settlement_draw_leak.py`：驱动真实 `second_behavior_effect` / `handle_extra_orgasm`（结算函数打桩以隔离绘制门）。站点 A 门、额外绝顶只挡绘制不挡结算、`998` 刻印远程仍显示三项均通过；还原到 base 后失败（红能力确认）。
- 固定随机种子（20260716）的真实 Tk 前后截图：读档后从健身区移动到走廊，修复前接连弹出「琳琅诗怀雅双重绝顶」等异地干员绝顶提示，修复后同一移动直接完成显示走廊场景。证据归档于 `~/games/archive/erArk-upstream-pr-evidence/2026-07-16-remote-orgasm-display-leak/`。

## 关联

- 前置：`remote-plural-orgasm-settlement`（PR #215），本 change 解决其显式遗留的衍生显示缺陷。
- 上游 PR：#222（`Godofcong-1/erArk`），base=master，改动 2 文件（21 增 12 删）。
