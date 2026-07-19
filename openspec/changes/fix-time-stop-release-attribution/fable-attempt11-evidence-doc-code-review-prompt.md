/investigate-game-bug

请以怀疑视角独立审查 erArk 的“时间停止解除时，延后高潮的结算记录归属”候选。不要假设现有方案、证据或文档正确；请使用工具亲自打开所列代码、文档与完整分辨率图片。事实问题以源代码和归档证据为准。

当前上游基线为 `72e28051ebaaabb069d06059b4633fda90b0b621`。隔离候选工作树是 `/home/ubuntu/games/erArk-pr-time-stop-release-attribution-current`，唯一生产改动是 `Script/Settle/default.py` 的 effect 527 处：

```diff
-        second_behavior.orgasm_settle(chara_id, change_data, un_count_orgasm_dict = character_data.h_state.time_stop_orgasm_count)
+        settlement_change = change_data.target_change.setdefault(chara_id, game_type.TargetChange()) if any(character_data.h_state.time_stop_orgasm_count.values()) else change_data
+        second_behavior.orgasm_settle(chara_id, settlement_change, un_count_orgasm_dict = character_data.h_state.time_stop_orgasm_count)
```

按当前 skill 的正式评分定义，生产 diff 去掉空白行后为 `a=2, b=1, S=0, U=0, penalty=3`。一行内联候选会超过项目 200 字符硬风格门槛。显式正值判断的候选为 `a=3, b=1, S=1, U=0, penalty=5`；生产写入路径只产生非负计数。

当前文档：

- `/home/ubuntu/games/erArk/openspec/changes/fix-time-stop-release-attribution/proposal.md`
- `/home/ubuntu/games/erArk/openspec/changes/fix-time-stop-release-attribution/design.md`
- `/home/ubuntu/games/erArk/openspec/changes/fix-time-stop-release-attribution/tasks.md`
- `/home/ubuntu/games/erArk/openspec/changes/fix-time-stop-release-attribution/implementation-notes.md`

自动化事实：本地测试通过真实 `Script.Settle` 注册表和真实 `second_behavior.orgasm_settle`。未修改上游时，NPC 的实际经验增加但同步经验记录落到玩家根对象；候选把该记录放入同一 NPC 的 `target_change`。零、单个、多个、远端 NPC、清理副作用、Web 收集和未发布本地批处理 mod 兼容性均已有检查。当前候选聚焦测试 1 passed，`py_compile` 与 `git diff --check` 通过。

真实 Tk A/B 归档：`/home/ubuntu/games/archive/erArk-upstream-pr-evidence/2026-07-15-time-stop-release-attribution-attempt11/`。请至少打开：

- 修复前：`baseline/frames/b31-final.png`
- 修复后：`candidate/frames/c31-final.png`
- `outcome.md`
- `manifest.md`

已核对的运行事实：两边从标题到结果前共有 31 对逐帧完全相同的画面；使用同一存档、种子、窗口、物理输入，存档哈希未变。修复前结果页中 Doctor 获得 `无意识绝顶经验+1`、`饮精绝顶经验+1`，林获得 `无意识绝顶经验+2`。候选中 Doctor 结算块消失，林获得 `无意识绝顶经验+3`、`饮精绝顶经验+1`；其余可见数值不变，总量无丢失或重复。运行日志无 Traceback、Exception 或 TclError。此前 attempt 1-10 均仅为无效诊断，不作为 PR 证据。

请回答：

1. 这组玩家可见证据是否足以让未参与调查的人类评审相信这是正常玩法中的真实 bug，而不是人为构造状态或视觉误读？若不足，请指出最小的下一项证据。
2. 候选是否在正确逻辑所有者处修复了“被释放 NPC 的同步结算记录不应写进玩家根记录”这一规则，并保留零计数及其他既有语义？是否存在通过硬门槛且 penalty 更低的正确候选？
3. 四份 OpenSpec 文档是否准确、互相一致、没有把 effect 527 的结论外推到未验证的通用二阶段结算，也没有保留会误导后续 agent 的陈旧描述？
4. 该候选是否改变需要玩家最终选择的游戏语义，还是只修正结算归属？

请分别给出 `EVIDENCE PASS/REVISE`、`CODE PASS/REVISE`、`DOCS PASS/REVISE`。任何 REVISE 都请列出具体、可执行、按严重性排序的修改；如果认为应停止这一 PR，也请直接说明理由。不要起草 PR 文案。
