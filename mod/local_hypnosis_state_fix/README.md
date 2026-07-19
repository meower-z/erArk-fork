# 本地催眠状态修复

## 症状

催眠模式在指令中切换后，当前目标的催眠无意识状态可能没有立即套用。单人催眠结算也可能因为默认模式为“无”或理智刚好耗尽而丢失目标状态。处于催眠类无意识的目标还可能被普通睡眠/醉酒/时停口上门禁吞掉。

## 根因

催眠“模式选择”和“状态套用”分散在面板与结算流程中，缺少幂等校正；口上前提判断也没有区分普通无意识和催眠类无意识。

## 修复范围

- 运行时包裹 `Chose_Hypnosis_Type_Panel.change_hypnosis_type`，指令模式切换后立即套用当前目标；空气催眠因地点不可锁门无法套用时，给出与上游一致的失败警告而非静默返回（2026-07-06 加深）。
- 运行时包裹行为效果 `1211` / `handle_hypnosis_one`，单人催眠结算后重新校正当前目标状态。
- 运行时包裹 `hypnosis_panel.evaluate_hypnosis_completion`：默认催眠类型为"无"(0)且目标催眠度达标时，上游会把目标既有催眠无意识态(4/5/6/7)清零；包装在源头保留该状态，同时覆盖单人(1211)与群体(1212)催眠两条调用路径（2026-07-06 加深——此前仅1211有事后补偿，群体催眠仍会误清）。
- 运行时包裹 `handle_premise.get_weight_from_premise_dict`，仅对催眠类无意识标记 `4/5/6/7` 开启口上门禁绕过。
- 本组件改写 `sp_flag.unconscious_h` 的所有路径同步调用 `settle_chara_unnormal_flag(5/6)` 重算异常标记缓存，与上游写入点的配对约定一致（2026-07-06 加深）。

## 依赖

本组件不依赖其他拆分组件。

## 验证

```bash
python mod/local_hypnosis_state_fix/tests/test_local_hypnosis_state_fix_mod.py
```

近真实BDD（真实 ModManager 加载后驱动真实 `evaluate_hypnosis_completion`）：

```bash
.venv/bin/pytest mod/tests/bdd/test_bdd_hypnosis_state.py -v
```

## BDD待补充

后续BDD场景需要覆盖普通场景指令切换催眠、H模式中切换心控催眠、单人催眠理智耗尽后仍保持心控状态，以及催眠态口上正常出现（完整UI路径）。
