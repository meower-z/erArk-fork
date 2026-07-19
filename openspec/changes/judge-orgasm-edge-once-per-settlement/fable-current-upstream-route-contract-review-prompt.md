/investigate-game-bug

请以怀疑视角重新裁决 T2 当前上游 Tk 诊断路线合同。新证据证明此前冻结的“38物理输入=六次等待”在真实输入流中不成立。不要为了保留旧合同否认输入代码，也不要自动授权重跑。

请读取：

- `openspec/changes/judge-orgasm-edge-once-per-settlement/current-upstream-route-contract-invalid.md`
- `openspec/changes/judge-orgasm-edge-once-per-settlement/current-upstream-attempt4-invalid.md`
- `openspec/changes/judge-orgasm-edge-once-per-settlement/current-upstream-attempt7-invalid.md`
- `openspec/changes/judge-orgasm-edge-once-per-settlement/fable-current-upstream-attempt7-review-ruling.md`
- `/tmp/erark-pr-evidence/orgasm-edge-current/formal-current-20260715-attempt4/action-log.md`
- attempt4 六张所谓post-wait帧、`character_behavior.py:265-270`、`flow_handle.askfor_wait`及输入处理代码。

已验证事实：

1. 6001 handler在update前写player behavior=`wait`,duration=5；wrapper入口depth0/update_depth1，入口边界谓词正确。
2. 玩家结算和黄字画出后，同一init调用进入WaitDraw/askfor_wait；它只在空字符串输入或鼠标确认时退出。非空`6001`被读取但不break，Return handler本身不置鼠标确认flag。
3. 因此 attempt4/7 第一次6001后 original()仍未返回，wrapper finally没有outer_wait记录；这不是谓词失败。
4. attempt4 后五个非空6001都被同一个暂停吞掉。六张所谓结果帧PNG hash和文件大小逐一相同，都是第一次等待结果。旧“六次等待”证据合同无效。
5. attempt4/7 first-result像素完全相同，未来画面硬门应使用解码RGB raster hash `a16009f...`，尺寸2100x1079，零像素容差。
6. 最小正常玩家修正：每次真实wait的结果帧后发送一个空Return退出WaitDraw，等outer_wait finally落盘，再输入下一次6001。若六次都在最后结果后也确认，总输入从38变44；若第六次结果停止采证而不退出，只需43，但没有第六条outer_wait/finally诊断记录。
7. 在WaitDraw之前提前flush会漏NPC阶段，不能回答你选的诊断A。

请只裁决一个新合同：

- 是否应采用44输入（六次wait均完成并退出，六条完整诊断），还是43输入（第六次结果可见但第六条诊断不完整，应拒绝），或BLOCKED停止；
- 每次空Return后必须看到什么状态/trace才能输入下一次6001；
- 六次结果帧的RGB raster门禁是否都应继续要求等于第一次参考a16009f，还是只要求输入流/角色结果合同，防止把“正常时间推进导致画面变化”错误拒绝。

只输出 `PASS`、`REVISE` 或 `BLOCKED` 开头。只给一个最终路线合同和停止条件，不写PR文案，不提出其他诊断方向。
