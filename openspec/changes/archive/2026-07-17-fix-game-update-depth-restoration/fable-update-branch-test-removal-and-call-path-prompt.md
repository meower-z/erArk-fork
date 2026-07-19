/investigate-game-bug
/review-erark-pr-artifacts

请作为 erArk bugfix program 的 Fable 发布监督者，复核用户澄清后的 fork branch 处理以及间接递归调用链。请自行读取下面列出的仓库文件和提交，不要编辑文件，不要授予 push 权限。

用户澄清：

- fork 上 `23188ce1a` 的 merge commit 是用户点击 GitHub “Update branch” 按钮产生的，用于把 side branch 更新到当前 upstream main；应保留这次同步，不再改写历史。
- 用户要求进一步把 branch 中的自动化测试文件移除。
- 用户观察 `game_update_flow()` 本身没有直接调用自己，要求解释所谓递归错误路径。

当前候选：

- 发布 worktree：`/home/ubuntu/games/erArk-pr-game-update-depth-publish`
- 远端当前 tip：`23188ce1afba4cd670542a7428d18d778d546968`
- 本地 tip：`fb10be12a`，是在远端 tip 之上的普通提交，只删除 `tests/test_game_update_depth_restoration.py`。
- 本地 tip 相对 `upstream/master` 的最终拟提交 diff 只有 `Script/Design/update.py`，5 行新增、4 行删除；tip 树中没有 `tests/`。
- `Script/Design/update.py` 与已经审计通过的 production-only `bc1bfb44e` 文件哈希完全一致。
- 本地未跟踪回归仍通过 4 项，production file 通过语法检查；这些结果不进入 PR 文案。
- 没有 PR。

生产调用链的源码位置：

1. `Script/Design/update.py:23-24`：`game_update_flow()` 推进时间后调用 `character_behavior.init_character_behavior()`。
2. `Script/Design/character_behavior.py:52-74`：该循环调用 `character_behavior(...)`。
3. `Script/Design/character_behavior.py:148-160`：玩家行为结算调用 `realtime_settle.character_aotu_change_value(...)`。
4. `Script/Settle/realtime_settle.py:124-127`：玩家的交互对象处于无意识状态时调用 `settle_sleep_h(...)`。
5. `Script/Settle/realtime_settle.py:443-471`：熟睡等级低且醒来随机判定成立时调用 `handle_npc_ai_in_h.judge_weak_up_in_sleep_h(...)`。
6. `Script/Design/handle_npc_ai_in_h.py:327-349`：醒来判定调用 `recover_from_unconscious_h(...)`。
7. `Script/Design/handle_npc_ai_in_h.py:155-256`：恢复函数末尾再次调用 `update.game_update_flow(5)`。

另一个静态入口是 `character_behavior.judge_character_status()` → `settle_behavior.handle_settle_behavior()` → 注册的 `default.handle_recover_from_unconscious_add_adjust()` → `recover_from_unconscious_h()` → `game_update_flow(5)`，但本次只需一条完整链即可说明生产代码存在循环。

证据边界：

- 真实 Tk 99/97 号档探索只看到最外层 update，没有进入上述嵌套路径。
- 因此当前只能确认生产代码中存在条件式的间接递归/重入循环；不能把它说成已在用户截图的连续高潮路线中发生，更不能说它是该截图的已确认根因。

请明确裁定：

1. 在保留用户主动产生的 Update branch merge 的前提下，追加一个只删除测试文件的普通提交，是否是最小且正确的处理；最终 PR diff 是否因此只剩生产文件。
2. `game_update_flow → ... → recover_from_unconscious_h → game_update_flow` 应称为间接递归、重入，还是别的术语；请给出最准确的中文解释。
3. 深度保存/恢复修复是否仍是对该生产循环的正确防护，但必须与用户截图中的重复高潮根因明确分离。
4. 是否允许在用户已明确要求“进一步移除测试文件”的授权下，将 `fb10be12a` 普通 fast-forward push 到同名 fork branch；只判断授权范围是否匹配，Fable 本身不要授予权限。
5. PR draft 若继续保留，应怎样避免把条件式生产循环夸大为已复现玩家故障；若现有 production-only draft 已符合，请明确说无需修改。

输出简洁但逐项回答。
