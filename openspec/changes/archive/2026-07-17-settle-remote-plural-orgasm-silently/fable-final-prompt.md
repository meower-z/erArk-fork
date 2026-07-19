/investigate-game-bug

请继续作为 erArk 这个候选 PR 的独立把关者。不要修改代码，不要做重型复现；只判断下面新增的只读来源证据是否补上你指出的“小满身份矛盾”，并给出最终提交边界、PR 文案和证据 caption。不要假定主代理的判断。

固定事实：

- 上游基线为 `upstream/master` `06fc59c1e71d092224375fc4a096b956aea2ad63`。
- 生产候选只有 `data/csv/Behavior_Effect.csv` 十行变化：`plural_orgasm_2` 至 `plural_orgasm_11` 各自在原有效果末尾追加 `997`。没有 Python 生产改动。
- 现有 997 语义是“远程必须结算但不必须显示”；普通部位绝顶已有 997。没有 997 的多重绝顶在远程 pass 中不会进入 must-settle，会留在 `second_behavior`，以后与玩家同处并完成当前行为时才显示、结算。
- `extra_orgasm`、`b_orgasm_to_milk`、`u_orgasm_to_pee` 不在这个 marker-only change 内，因为其效果函数直接绘制。
- 精确生产 diff：

```diff
-1050,plural_orgasm_2,409 - 301
-1051,plural_orgasm_3,409 - 301 - 302
-1052,plural_orgasm_4,409 - 303 - 302
-1053,plural_orgasm_5,409 - 303 - 302
-1054,plural_orgasm_6,409 - 303 - 304
-1055,plural_orgasm_7,409 - 303 - 304
-1056,plural_orgasm_8,409 - 303 - 304
-1057,plural_orgasm_9,409 - 305 - 306
-1058,plural_orgasm_10,409 - 305 - 306
-1059,plural_orgasm_11,409 - 305 - 306
+1050,plural_orgasm_2,409 - 301 - 997
+1051,plural_orgasm_3,409 - 301 - 302 - 997
+1052,plural_orgasm_4,409 - 303 - 302 - 997
+1053,plural_orgasm_5,409 - 303 - 302 - 997
+1054,plural_orgasm_6,409 - 303 - 304 - 997
+1055,plural_orgasm_7,409 - 303 - 304 - 997
+1056,plural_orgasm_8,409 - 303 - 304 - 997
+1057,plural_orgasm_9,409 - 305 - 306 - 997
+1058,plural_orgasm_10,409 - 305 - 306 - 997
+1059,plural_orgasm_11,409 - 305 - 306 - 997
```

- 本地回归在有效基线为 `11 failed, 2 passed`，候选为 `13 passed`。它经过真实的 admission、remote settlement、must-settle 和 plural effect 函数体，断言数值实际增加、队列归零、无远程 talk、靠近后不重放、附近仍显示，且群交发现入口仍工作。上游无 tests 目录/pytest CI；你先前要求测试保持 local-only。
- 真实 Tk A/B 使用同一 pristine slot99、无 mod、固定 Python seed `99720260714`、NumPy/PYTHONHASHSEED `936012906`、同一 2100x1100 geometry 和同一玩家路线。基线 12:57 屏幕底部显示黄色“小满双重绝顶”；候选同路线 12:57 没有延迟多重绝顶文本。两边 11:57 均正常显示附近“凯尔希阴道小绝顶”。
- 主图：baseline 原始外窗 sha256 `eca0c5f72011bd9c71062b3829bc01d6d58d4359884f49036fe17a471adafab7`；只裁掉 21px 窗口管理器标题栏后的原生 Tk client `before.png` 为 2100x1079、sha256 `12d663a7734b51418a8571bbd93c0447a6f3d9ba543b1bf64a8cba980faccd0d`。candidate `after.png` 为 2100x1079、sha256 `3b9aca0c7dc455ccdfc23f7bf2f09ad909235aa73bb5622c513e672495deb07a`。主代理已 original 像素复检；你没有看图工具，不能声称看过像素。

你上次唯一保留意见是：先前逻辑模拟预测的是林/惊蛰，但真实屏幕写小满；且小满在 12:42 到达咖啡馆时与玩家同处，所以必须只读确认她的 pending queue 是何时何地生成，不能把一个本地新绝顶误当成远程旧队列。

新增只读探针事实：

- 探针仅在 pristine baseline 运行时包装真实 `character_get_second_behavior`、`second_behavior_effect`、`talk.handle_second_talk`，写 JSONL；不修改 save、queue、数值或随机源。最终 v6 探针 sha256 `ab13287caea58445b5b98d06099428a100eea5a0924995f97ab6f0d6dcf35441`，py_compile 通过。slot99 运行后仍为原始两个 sha256：`6bcd68f4e9a14460206c7e29f61980c27d9b1fce41f25d03aa44dd40d44e59cf` / `534ba3960ebe29bb020cad68499b1622b9f8f4a54669dd4b79c49ed525b26b63`。
- 探针有效性控制：11:57 屏幕显示“凯尔希阴道小绝顶”时，真实 talk 包装记录：
```json
{"behavior_id":"v_orgasm_small","character_id":3,"character_name":"凯尔希","character_position":["动力","人力发电室"],"is_plural":false,"kind":"talk","player_position":["动力","人力发电室"],"time":"2019-12-29T11:57:00"}
```
- 关键 admission 原始记录：
```json
{"behavior_id":"plural_orgasm_2","character_behavior":"eat","character_behavior_duration":30,"character_behavior_start":"2019-12-29T12:26:00","character_id":4122,"character_name":"小满","character_position":["贸易","哥伦比亚咖啡馆"],"kind":"generated","player_position":["动力","内走廊"],"reset":false,"time":"2019-12-29T12:29:00"}
```
- 同一时刻还记录清流、食铁兽、惊蛰在别处生成 `plural_orgasm_2`，说明探针确实观察真实 admission 流。
- 12:29 当场冻结的 trace 副本有 31 行，sha256 `05f18e870ef26d1259614f5f7a9e536c5590699332b0f69dadf8de7ae435bd55`；其中持久保存了上面的小满原始行。探针随后按同一路线正常到达哥伦比亚咖啡馆 12:42，但 allocator 的一小时 supervisor 到期后留下未监督子进程，主代理立即停止该自有 PGID；因此没有得到小满 12:57 talk 的探针行。最终主 trace 33 行，sha256 `02b85cf9328e0daa2e0a270d575c84fc9e5e976203df7614049c4f4030f85df6`。独立的未插桩真实 Tk 基线已按完整路线得到 12:57 “小满双重绝顶”原图；不要把两次运行说成同一会话，也不要隐去这个限制。

请返回：

1. `VERDICT: ACCEPT / REVISE / BLOCK`。专门判断“12:29 小满在咖啡馆、玩家在内走廊时生成 plural_orgasm_2”的只读 admission 记录，加上独立同 seed/同路线的 12:57 小满可见帧，是否足以闭合先前身份矛盾；如果还不够，只指出下一条最小必要证据。
2. 最终提交边界：仅十行 CSV，还是包含本地测试；给唯一选择。
3. 若 ACCEPT，给上游中文 PR 标题、正文，以及 `BEFORE_URL` / `AFTER_URL` 两张主图的中文 alt/caption。文案只写提交和证据支持的内容，按“问题、修复、验证”简洁组织；不要写调查过程、测试文件路径、known non-goals 或本地路径。
4. 给主代理一份提交前本地清单；用户要求在上传图片、push、创建 PR 前停下，不得建议执行这些 outward actions。

