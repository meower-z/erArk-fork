/investigate-game-bug

你是 erArk“时停解除结算归属”任务的最终流程监督者。当前永久 INVALID、仅作 DIAGNOSTIC ONLY 的 run2 按你刚批准的 `CONTINUE FROM H MENU` 继续，在第四轮口交选择 `[射出]` 后出现了稳定但视口位置不同的同一结算页。执行者按旧 run2 prereg 的整页 SHA 门停止；请怀疑地决定这是内容缺失、输入污染，还是旧协议又把视口像素误当语义。不要为了到 endpoint 而忽略关键 setup 状态，也不要把本任务真正要测的“解除时停归属页”与用于造状态的口交页混为一谈。

## 精确事实

- 从稳定射精选择面板，仅点击一次 `[射出]`；没有 Return、滚轮、拖动、signal 或其他输入。
- 之后按 1 秒间隔的 r2-36..45 共十张全部 byte-identical，AE0，SHA256 都是 `101c5676b3170f79f8f60a32b33df497711479b155dee8738fbf858d296f2674`。不是逐字动画，也没有超时重绘。
- 十张从第一张起都可读：`射出`，以及黄色 `在林的口腔射精，射出了20ml精液（醒来第一发+）`。这个文本、20ml、角色林与 run1 相同。
- run1 对应 stable page SHA 是 `0e54354a9305ac390de293676af2d6501ed4d0492183ecd8f5827338d9323eeef`。它的文本 widget 自动滚得更靠下，因此同一屏还显示下一块标题 `博士射精`；run2 viewport 停得稍靠上，`博士射精` 位于可视区下方。
- 两张原图尺寸都是 1238x937。run2 没有出现错误文本、错误人物、错误数值、菜单或异常，只是 scroll offset 不同。
- 当前页是普通口交第四轮的 setup wait page，用来制造林的 deferred count/shoot position。被测的 T4 输出尚未发生；真正 PR-facing 测量页是在切换到惊蛰后点击 `[4115]` 的解除时停结算。
- 下一步若获准，只需从当前 wait 页按一次 Return，进入 numeric settlement；之后 hard sample1 会直接核验 Lin counts `{0:1,21:2}`、shoot_position_body `2`、经验、target/H/time-stop，以及全部其他 trigger NPC。该状态门比是否在上一屏看见下一个标题更直接。
- 执行者已经 STOP，未补滚动、未按 Return，unit/window 保持原样。

## 你上一裁定的相关规则

- 稳定页只有“不在预注册语义链上”才是错误页；沿链到后续 checkpoint 不是错误。
- 状态改变动作以最终稳定 semantic checkpoint 为门；稳定互动决策点必须逐页出现。
- 例外是“承载被测结算文本的 wait 页”必须捕获，否则整轮重启。
- current run 仍只诊断 endpoint，绝不能成为 PASS/PR 证据。

## 请作最后决定

1. 给 `CONTINUE WITHOUT SCROLL`、`CLOSE/RESTART` 或 `REVISE`。若继续，是否明确禁止为了追 run1 SHA 而滚动，只按一次正常 Return，让后续 numeric page 和 sample1 决定 setup 是否正确？
2. 本页是否属于你说的“承载被测结算文本的 wait 页”？T4 测的是解除时停归属，不是普通口交；请给任务边界上的明确答案。
3. 正式 prereg 对这种 setup 输出页应要求哪些 semantic anchors（人物、20ml、射出位置等），哪些应留给 sample1 state gate；是否应禁止硬编码整页 SHA/scroll offset？
4. 正式解除时停后的归属输出页仍是否必须逐页可读捕获，并按 baseline/candidate 预期文本/分组审查，而不能只凭 sample3 推断？
5. 若允许诊断继续，后续 endpoint 前仍执行原计划：numeric page→H menu→sample1→两次 trough→点惊蛰→bottom menu→sample2→一次 active `[4115]`；若任何 hard state 不符立即停止。
6. 是否需要玩家介入？这里不改玩法语义、不外发。
