# PR #213 Revised Draft

`publication_state: publication-ready`

The three approved evidence images are published at commit-pinned public URLs below.

## 标题

修复：解除催眠后"苦痛快感化"未被一并解除

## 正文

## 问题

对已被施加`苦痛快感化`的干员主动使用`[4004]解除催眠`后，`心控`等其他催眠子状态都已结束，但状态栏仍残留`(痛→快感)`，该效果实际继续生效。

作为对比，干员`熟睡`自然结束催眠时，`苦痛快感化`会随其他子状态一并解除。设计上两条退出路径应当一致：结束催眠时，同一组持续性心体催眠子状态应当全部结束。

## 原因

主动`解除催眠`的子状态清理代码写于 `pain_as_pleasure` 字段加入之前；该字段后来加入时没有补进这份旧的清理列表。而更晚建立的`熟睡`清理从一开始就包含它。于是两处各自维护了一份几乎相同的清理列表，其中主动`解除催眠`少了`苦痛快感化`这一项。

## 修复

新增一个共用函数，专门负责结束五项持续性心体催眠子状态：`敏感度提升`、`木头人`、体控`逆推`、`苦痛快感化`、`角色扮演`。主动`解除催眠`和`熟睡`都改为调用它，这份列表只表达一次，两条路径不会再各自漏项。

`熟睡`的行为不变；主动`解除催眠`补上了对`苦痛快感化`的清除，与`熟睡`对齐。

## 验证

用同一份存档，以凯尔希作为代表案例走同一操作流程：

- 操作前，凯尔希状态栏显示 `<催眠(200%):心控(敏感)(痛→快感)>`，同一画面可见`[4004]解除催眠`指令。

[![操作前：状态栏含 痛→快感，可见解除催眠指令](https://raw.githubusercontent.com/meower-z/erArk-fork/619d313c020af38c014e338a24b9bdbf59bb0efe/pr-213/direct-cancel-before.png)](https://raw.githubusercontent.com/meower-z/erArk-fork/619d313c020af38c014e338a24b9bdbf59bb0efe/pr-213/direct-cancel-before.png)

- 上游当前版本：执行`[4004]解除催眠`后，状态栏仍显示 `<催眠(200%)(痛→快感)>`，效果残留。

[![上游当前版本：解除催眠后 痛→快感 残留](https://raw.githubusercontent.com/meower-z/erArk-fork/619d313c020af38c014e338a24b9bdbf59bb0efe/pr-213/direct-cancel-baseline-after.png)](https://raw.githubusercontent.com/meower-z/erArk-fork/619d313c020af38c014e338a24b9bdbf59bb0efe/pr-213/direct-cancel-baseline-after.png)

- 本 PR：同样操作后，状态栏显示 `<催眠(200%)>`，`痛→快感`已随其他子状态一并解除。

[![本 PR：解除催眠后 痛→快感 一并解除](https://raw.githubusercontent.com/meower-z/erArk-fork/619d313c020af38c014e338a24b9bdbf59bb0efe/pr-213/direct-cancel-candidate-after.png)](https://raw.githubusercontent.com/meower-z/erArk-fork/619d313c020af38c014e338a24b9bdbf59bb0efe/pr-213/direct-cancel-candidate-after.png)

## Published Evidence Map

The following local files are review inputs, not text to paste into the PR:

- `direct-cancel-before.png`: `/home/ubuntu/games/archive/erArk-upstream-pr-evidence/PR-213/local/hypnosis-cancel-narrow-20260714/capture/baseline-before.png`
- `direct-cancel-baseline-after.png`: `/home/ubuntu/games/archive/erArk-upstream-pr-evidence/PR-213/local/hypnosis-cancel-narrow-20260714/capture/baseline-after.png`
- `direct-cancel-candidate-after.png`: `/home/ubuntu/games/archive/erArk-upstream-pr-evidence/PR-213/local/hypnosis-cancel-narrow-20260714/capture/candidate-after.png`

## Required Revision Summary

- The title changes from a sleep-path failure to a direct-cancellation failure.
- The problem section makes sleep the correct comparison rather than the defect.
- The cause changes from an extra sleep cleanup entry to a field omitted from older direct-cancellation cleanup.
- The helper now owns five fields, including `pain_as_pleasure`, instead of four.
- The evidence route changes from sleep to `[4004]解除催眠`; none of the old images support this corrected candidate.
