/investigate-game-bug

请以怀疑视角只读审查 T2 `judge-orgasm-edge-once-per-settlement` 的 current-upstream Tk Diagnostic A attempt8。不要修改文件，不要写 PR 文案，不要因为此前契约由 Fable 给出就默认它正确。先核对源码、文档、trace 和两张关键画面，再裁决下一步。

已验证事实：

- current upstream/base 是 `72e28051ebaaabb069d06059b4633fda90b0b621`；本轮使用真实 Tk、pristine save99、seed0、`PYTHONHASHSEED=0`，没有候选生产代码。
- 旧 attempt4 后来被证明只执行了一次真实 `[6001]`：后续非空 `6001` 都被同一结果等待吞掉。静态输入流与历史相同帧支持该结论，记录在 `current-upstream-route-contract-invalid.md`。
- Fable 随后规定 44 个物理输入：26 个读档输入，之后六轮 `6001`、Return、检查结果、空 Return；每轮空 Return 后必须有 completed `outer_wait` 且画面回到空输入框主面板，否则 INVALID，不能临场补救。原 verdict 是 `fable-current-upstream-route-contract-review-ruling.md`。
- attempt8 严格执行到第一轮。action28 的结果图 `/tmp/erark-pr-evidence/orgasm-edge-current/diagnostic-current-20260715-attempt8/frame-28-w1-result.png` 为 2100x1079，RGB raster SHA-256 精确等于契约值 `a16009f709c1885cd214e66f60bf99faeb0c997f3843dc0e23f29ef875987536`，该门槛通过。
- action29 只发送一次空 Return。40 秒内没有 completed `outer_wait`；`frame-29-w1-after-empty-return-timeout.png` 仍为结算文字页，不是空输入框主面板。进程存活。按契约立即 INVALID，未发 rescue input，未开始第二轮。
- `diagnostic-trace.jsonl` 只有五条 probe setup/installation 记录，无 settlement diagnostic。source/runtime 存档前后哈希相同。allocator 已释放，临时 runtime/controller/worktree 已清理。
- 原始本轮记录：`/tmp/erark-pr-evidence/orgasm-edge-current/diagnostic-current-20260715-attempt8/{RESULT.md,action-log.md,manifest.md,diagnostic-trace.jsonl,rgb-raster-hashes.txt,pre-route-save-hashes.txt,post-route-save-hashes.txt}`。
- 新正式记录为 `current-upstream-attempt8-invalid.md`；`tasks.md` 5.6 与 `pr-readiness.md` 已降级/补记。`openspec validate judge-orgasm-edge-once-per-settlement --strict` 通过。
- 当前代码候选没有改变：生产 diff score `a=19,b=19,S=11,U=0,penalty=49`，focused tests 11 passed；但 publication state 仍是 `evidence-blocked`。

请裁决：

1. 文档是否准确、克制、足以通过质量门槛；若不通过，只列必须修正的事实或措辞。
2. 基于真实 draw/wait 生命周期，为什么 action29 一次空 Return 后仍停在文字页？这是多段 `LineFeedWaitDraw`、焦点/提交条件、异步阻塞，还是其他可由源码和画面区分的机制？事实问题请引用具体源码/画面，不凭意见。
3. 下一步应是：先做一个无游戏运行的窄静态生命周期追踪；允许一个新的有限诊断；冻结 save99 路线并寻找其他正常玩家入口；或停止 T2 的 current-upstream 可视证据。不要受这些选项限制，但必须选择一个最小且可证伪的步骤。
4. 若允许新的 Tk 诊断，请给出精确输入类型、每次输入前后的可见门槛、最多输入/等待上限、成功/无效条件；不能用开放式试玩、盲按或临场救场。
5. 只有确实必须由玩家决定时才写 `PLAYER INPUT REQUIRED`；否则按项目 stopping rule 给出可继续执行的裁决。

请以 `PASS`、`REVISE` 或 `BLOCKED` 开头；随后分别写 `DOCS`、`MECHANISM`、`NEXT STEP`。不要修改任何文件。
