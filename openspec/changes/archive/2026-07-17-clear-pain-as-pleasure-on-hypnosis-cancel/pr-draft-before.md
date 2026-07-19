# PR #213 Remote Draft Before Maintainer-Requested Revision

Captured from the live PR on 2026-07-14 UTC.

## Title

修复：干员熟睡后"苦痛快感化"被错误解除

## Body

## 问题

当一名已被施加`苦痛快感化`的干员自行入睡进入`熟睡`时，她的`痛→快感`效果会被错误清除。

作为对比，对干员主动使用`解除催眠`时，`苦痛快感化`是保留的。设计上两种情况应当一致：无论干员`熟睡`还是被主动`解除催眠`，`苦痛快感化`都应保留。

## 原因

`熟睡`和主动`解除催眠`都会结束同一组心体催眠子状态：`敏感度提升`、`木头人`、体控`逆推`、`角色扮演`。这四项在两种情况下的处理本来就一致。问题在于，`熟睡`时执行的清理列表里意外多包含了一项`苦痛快感化`，所以只有睡觉这一种情况会把它一并清掉。

## 修复

把两处相同的四项子状态清理提取为一个共用函数，`熟睡`和`解除催眠`都改为调用它。这样两种情况都只结束上述四项，`苦痛快感化`不再被混入`熟睡`的清理。`解除催眠`的行为不变，`熟睡`与之对齐。

## 验证

用同一份存档，以凯尔希作为代表案例走完整流程：

- 操作前，凯尔希状态栏显示 `<催眠(200%):心控(敏感)(痛→快感)>`。
  [![操作前：凯尔希状态栏显示 <催眠(200%):心控(敏感)(痛→快感)>](https://raw.githubusercontent.com/meower-z/erArk-fork/3d7dfc2748a0d5cdb962244088378fdada7471c7/pr-fix-hypnosis-sleep-pain-preservation/before.png)](https://raw.githubusercontent.com/meower-z/erArk-fork/3d7dfc2748a0d5cdb962244088378fdada7471c7/pr-fix-hypnosis-sleep-pain-preservation/before.png)
- 上游当前版本：凯尔希入睡后，状态栏含`熟睡`与 `<催眠(200%)>`，`痛→快感`已丢失。
  [![上游版本入睡后：凯尔希状态栏显示熟睡与 <催眠(200%)>，痛→快感已丢失](https://raw.githubusercontent.com/meower-z/erArk-fork/3d7dfc2748a0d5cdb962244088378fdada7471c7/pr-fix-hypnosis-sleep-pain-preservation/upstream-after.png)](https://raw.githubusercontent.com/meower-z/erArk-fork/3d7dfc2748a0d5cdb962244088378fdada7471c7/pr-fix-hypnosis-sleep-pain-preservation/upstream-after.png)
- 本 PR：同样入睡后，状态栏含`熟睡`与 `<催眠(200%)(痛→快感)>`，效果保留。
  [![本 PR 入睡后：凯尔希状态栏显示熟睡与 <催眠(200%)(痛→快感)>，效果保留](https://raw.githubusercontent.com/meower-z/erArk-fork/3d7dfc2748a0d5cdb962244088378fdada7471c7/pr-fix-hypnosis-sleep-pain-preservation/fixed-after.png)](https://raw.githubusercontent.com/meower-z/erArk-fork/3d7dfc2748a0d5cdb962244088378fdada7471c7/pr-fix-hypnosis-sleep-pain-preservation/fixed-after.png)
