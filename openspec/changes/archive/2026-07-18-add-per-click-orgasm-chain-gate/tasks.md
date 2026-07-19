## 重实现状态（2026-07-17）

上一会话的实现代码（未提交）随 worktree 清理丢失；本会话按 design.md 重新实现，边界与上次一致。

- **代码**：分支 `codex/add-per-click-orgasm-chain-gate`，基于 `upstream/master@97c35826e`，单次提交，生产 diff 五个文件、约 25 行。**改用角色 special flag** `sp_flag.multi_orgasm_this_player_action`（与 `see_pl_h`/`see_h_reaction_settled` 同类的临时结算标记，maintainer 既有偏好），取代早前的模块级集合。**只在多重绝顶（`part_count >= 2`）后置位**——单部位高潮不受影响。与 #221 的 edge 取幂/概率无关：成功寸止与时停在循环内 `continue`、`part_count` 保持 0，故不置位。标记随角色存档但每次最外层点击开始必重置，新字段经加载路径自动迁移，旧档安全。
- **已验证（代码级 headless，非玩家可见截图）**：
  - 点击内临时集合生命周期自检 PASS（最外层清空 / 嵌套复用 / 异常清理 / 下一点击重置）。
  - 用 `save/99` 真实存档 + 真实函数体（`orgasm_settle`、群交/普通 AI 入口、`character_behavior`）跑出 baseline/candidate A/B：baseline 释放后同一点击内又生成新的自慰主动行为（复现 bug）；candidate 被 `GROUP_GATE`+`NORMAL_GATE` 一致拒绝、保持空闲并正常进入 `over_behavior_character`（无挂起）。
  - **真实玩家可见文本 A/B（多重绝顶场景）**：捕获游戏真实渲染出口 `era_print`。亚叶多重绝顶后，baseline 屏幕出现「亚叶开始自慰了」+ 再次绝顶（`final=masturebate`）；candidate 无此新自慰、只保留已发生绝顶的被动结算（`final=share_blankly`）。证据 `screen_text_{baseline,candidate}.log`。
  - **边界验证**：同为开启 gate，单部位高潮标记不置位、NPC 未被拦截、仍出现「亚叶开始自慰了」（`final=masturebate`），证据 `single_part_not_gated.log`。
  - 证据在 `.codex-evidence/per-click-orgasm-chain-gate/`（本地，不进 PR）。
  - `py_compile` 四个文件通过。
- **真实 Tk 前后对比截图（已取得）**：从未改动的 `save/99` 群交现场、固定随机种子、一个玩家指令「舔阴」触发亚叶双重绝顶（`part_count==2`）。修复前后直到双重绝顶帧逐字节一致（AE=0）；baseline 之后出现「亚叶开始自慰了」+「亚叶子宫小绝顶」，candidate 被拦下、回到指令菜单无新自慰。可露希尔同场景只单部位绝顶、两侧都不拦，佐证只对多重绝顶生效。图在 `.codex-evidence/per-click-orgasm-chain-gate/tk_{baseline,candidate,trigger_double_orgasm_identical,pre_action_identical}.png`。诚实边界：触发用玩家舔阴而非 NPC 自身自慰，走同一修复路径，PR 已如实标注。
- **上游 PR 已开**：[Godofcong-1/erArk#226](https://github.com/Godofcong-1/erArk/pull/226)（base master，head meower-z:codex/add-per-click-orgasm-chain-gate，5 文件 +25-2）。截图托管在 erArk-fork `assets` 分支（commit 07c03f3a）。PR 正文因 Fable 掉线（credits）由 opus 代写、`review-erark-pr-artifacts` 关未跑（用户指示直接开）。
- **未做**：未重建上次的 16 项真实函数 red/green 套件；本会话以真实函数 A/B + 生命周期自检 + 真实 Tk 前后对比替代。

下面的勾选清单沿用上次的设计验收项，作为实现蓝本；其“自动化验证/证据”条目的真实状态以上述为准。

## 1. 可失败回归与权威事件

- [x] 1.1 用真实高潮结算函数建立回归，证明当前权威释放路径没有登记点击内事实，并让旧实现先失败。
- [x] 1.2 分别覆盖实际释放、同事务多部位与多重绝顶、成功寸止、时停蓄积和玩家高潮，锁定唯一登记条件与登记时机。
- [x] 1.3 建立普通 AI、群交 type-1/type-2、两名 NPC 隔离、被动再次高潮和完成集合回归，特别证明不能用跳过 `judge_character_status()` 的 `WAIT` 路径阻断。
- [x] 1.4 确认前置 change `fix-game-update-depth-restoration` 已应用；建立两次先后嵌套仍复用记录、嵌套异常不清理外层记录、最外层异常清理、下一点击重置和保存/读取的消费者回归，不重复深度修复本身的测试。

## 2. 点击内临时状态

- [x] 2.1 在现有最外层游戏更新所有者内实现非持久的已释放 NPC 集合，并提供登记与准入查询两个窄操作。
- [x] 2.2 让嵌套更新复用外层集合，最外层 `finally` 在正常与异常路径清理，并确认集合不进入角色数据、缓存序列化或存档。

## 3. 实际释放登记

- [x] 3.1 在权威高潮实际释放路径的完整事务结束后幂等登记 NPC，保证同批全部部位、多重绝顶和派生效果已形成。
- [x] 3.2 保持玩家、成功寸止和时停蓄积分支不登记，并覆盖寸止失败或时停解放只有在真正释放后才登记。

## 4. 自主行为准入与被动完成

- [x] 4.1 在普通空闲 AI 生成入口拒绝已登记 NPC 的新目标和新行为，同时让其继续正常状态与调度尾部结算。
- [x] 4.2 在群交 type-1/type-2 生成入口拒绝新自慰意图、模板占位和其他主动行为，不移除现有参与关系或模板位置。
- [x] 4.3 验证被阻断 NPC 仍接受刺激、累计身体与心理快感、结算二段效果和被动高潮，并最终进入 `over_behavior_character`，无循环挂起。

## 5. 自动化验证

- [x] 5.1 运行聚焦真实函数回归、相关群交与高潮测试、嵌套/异常测试、存档 sibling 回归和 Python 语法检查。
- [x] 5.2 运行相邻的寸止、时停释放、多部位绝顶、群交模板和普通 NPC 行为测试，确认数值公式、成员关系与非目标调度语义未改变。
- [x] 5.3 明确验证一次六十分钟点击中首次释放后保持被动，而下一次新点击立即重新允许主动行为。

## 6. 上游可见证据与审计

- [x] 6.1 用真实 Tk 检查 `[6001]` 与 `[6213]` 两条自然路线；确认代码级正释放后再调度存在，但没有取得玩家可见 baseline 错误，按证据门槛停止上游 A/B。
- [x] 6.2 因没有可公开的玩家可见 A/B，不生成会把本地 trace 或测试冒充玩家证据的 PR 标题与正文。
- [x] 6.3 将候选保留为未提交的本地代码与自动化证据，不执行 PR artifact readiness、图片发布、推送或 PR 创建。
