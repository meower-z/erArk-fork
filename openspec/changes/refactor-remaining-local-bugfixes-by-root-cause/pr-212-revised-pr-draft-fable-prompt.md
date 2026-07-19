/investigate-game-bug
/review-erark-pr-artifacts

请为 Godofcong-1/erArk PR #212 重写中文 PR 标题和正文。你是唯一的 PR-facing 文案作者。输出必须能直接供上游 maintainer 阅读，并严格匹配下面的最终拟议 diff 和全新 Tk 证据。

## Maintainer 意见

> 直接在这里判断苦痛是否为正就可以了，不需要再单独构建函数，以及单独构建的那个函数的里会导致重复计算两遍心理快感的能力加成

## 最终拟议 diff

base: upstream/master abebf33b52ebf51424f71365946eb8df1f75a23c
head: 6864d4cf9d26590a7b17642c4800309688e820fc

```diff
-    # 心控-苦痛快感化，将苦痛状态转化为快感状态
-    if state_id == 17 and handle_premise.handle_hypnosis_pain_as_pleasure(character_id):
+    # 心控-苦痛快感化，将正向苦痛状态转化为快感状态
+    if state_id == 17 and final_value > 0 and handle_premise.handle_hypnosis_pain_as_pleasure(character_id):
         base_chara_state_common_settle(character_id, final_value, 23, 0, ability_level = character_data.ability[36], tenths_add = False, change_data = change_data, change_data_to_target_change = change_data_to_target_change)
         return
```

PR 相对 master 只有 `Script/Settle/common_default.py` 这一个文件、上述 2 行替换；旧 PR 中的新 helper、`Second_effect.py` 直接写入迁移和提示文本修改已全部撤回。

## 已确认的规则和边界

- `苦痛快感化` 只应把最终为正的苦痛增量改道为心理快感。
- 最终为零或负的苦痛变化必须留在原有 state 17 路径。
- 原有 state 17 路径包含状态写入、change record，以及 `extra_feel_settle`；能力 36 足够高时，它仍可正常产生受虐派生的心理快感和经验。正文不得声称“心理完全不变”或“没有心理变化”。
- 正苦痛仍复用原有递归 state 23 结算，因此不会在新 helper 中重复计算心理快感能力加成。
- 不得声称本 PR 修复 direct second-effect pain writers、睡眠/无意识语义、hypnosis flag 生命周期、额外绝顶文本或其他入口；这些均不在最终 diff 中。
- 不得写本地-only 测试命令、测试数量、OpenSpec、private investigation 路径或未提交的 `tests/`。

## 全新 Tk A/B 证据

本次证据完全重新运行，不复用旧截图。两侧都从冻结的同一个 No.99 存档、相同种子开始，经真实 Tk 标题页和存档页加载后执行一次 `[4103]体控-强制高潮`，逐页确认到完整结算。

- baseline `abebf33b52ebf51424f71365946eb8df1f75a23c`：`心理快感 -272586 (lv10→0)`，`苦痛 +3811`。
- candidate `6864d4cf9d26590a7b17642c4800309688e820fc`：`心理 +168`，`苦痛 -30397 (lv7→4)`，并显示普通 state 17 路径保留的 `心理经验 +3`。
- PR 正文图片 URL 暂用 `{{BEFORE_URL}}` 与 `{{AFTER_URL}}`；它们稍后会替换为 commit-pinned raw GitHub URL。图片链接和图片 src 必须相同。

## 写作要求

1. 输出一个准确、简短的中文标题，以及完整中文正文。
2. 正文按“玩家可见问题 / 原因 / 修复 / 验证”组织，先讲可见行为，再讲最小修复。
3. 明确旧设计已按 maintainer 意见收窄为现有通用结算分支上的 `final_value > 0` 判断；不要把已撤回设计继续写进正文。
4. 验证段只使用上述新证据，并解释 candidate 的 `心理 +168` / `心理经验 +3` 是普通苦痛路径保留的原有副作用，而非转换错误仍存在。
5. 为两张图写精确 alt/caption，使用下面形式：
   `[![alt](URL)](URL)`
6. 不要写测试清单，不要写维护者看不到的文件或过程，不要写 unsupported claims。
7. 只输出如下 markers 内的内容，不要额外解释：

```text
TITLE_BEGIN
<title>
TITLE_END
BODY_BEGIN
<body markdown>
BODY_END
```
