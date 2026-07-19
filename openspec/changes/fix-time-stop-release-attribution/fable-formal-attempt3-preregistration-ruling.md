/investigate-game-bug

你是 erArk“时停解除结算归属”fresh attempt3 正式 matched Tk A/B 的监督者。下面逐字附上尚未启动游戏的预注册草案。请以怀疑视角做协议审计，不要因为 attempt2 已失败两次、systemd 预检通过、候选代码已有 CODE PASS 或路线成本很高而降低门槛；也不要因为你刚批准了独立 transient service 就默认这份具体实现忠实执行了裁定。当前 candidate 没有启动，也没有任何 attempt3 游戏结果。

请特别检查：

1. attempt1/2 是否被彻底隔离为诊断材料，没有偷渡成正式结果；
2. fresh runtime、observer、common launcher、显式 environment 和两侧独立 service 是否足以形成可比 pair；
3. observer 新增的环境断言/打印是否仍是只读且不会改变玩法结果；
4. “实际等待页规则”、attempt2 页面只作异常探测器、attempt3 candidate 精确匹配 attempt3 baseline 这三层是否一致；
5. 四步切换、三次 sample 的时机、全 NPC gate、sample3 永久经验比较是否足够且没有过度断言；
6. 预注册的唯一可见差异与守恒条件是否能排除“显示看似修好但实际数值变了”；
7. systemd 生命周期、日志、异常和正常关闭的 stopping rule 是否仍有能让不完整结果混入的缺口；
8. 是否存在任何必须在游戏启动前修正的歧义、错误哈希、不可执行要求或文档质量问题。

请给明确的 `ATTEMPT3 PREREG PASS`、`REVISE` 或 `FAIL`。若不是 PASS，请给最小、可操作的修正；若 PASS，请明确哪些条款被冻结，以及 baseline 完整通过后 candidate 才可启动。最后说明是否需要玩家介入。

## Exact preregistration draft under review

# T4 fresh attempt 3 formal matched Tk A/B preregistration

Status: draft for Fable review. No attempt 3 game process has started.

This file defines a fresh pair. Attempts 1 and 2 are invalid diagnostics only.
Their screenshots, samples, logs, and action records SHALL NOT be used as
either formal side or paired with attempt 3.

## Governing decisions

- Fable formal route ruling SHA256:
  `5b3f4f40ca117efa37a6e0aab11c6455c70ff7616141df6f82e70a727c430ad8`
- Fable four-step/observer clarification SHA256:
  `792a3fd68036b4efbc546c5463a5cd9d0e0db3961bef262c08f86f8217236456`
- Fable actual-wait-page ruling SHA256:
  `80ff7f06f710efca1d8e3809fff45c705f064687ab85d245bb06967ca8f24109`
- Fable attempt-2 infrastructure ruling SHA256:
  `3fecce2e9fc3d0ee89b1d989b3503aec818528f5c21fc38aff999e93a8157713`
- Successful no-game systemd/allocator preflight manifest:
  `/tmp/erark-pr-evidence/time-stop-release-attribution/formal-current-attempt3/systemd-preflight-manifest.md`,
  SHA256 `60c52913b3c99ae0589fe6872b18fcbf99a13c74316ab81199196b1b557dd724`.

The attempt-2 ruling requires fresh runtime provenance, independent transient
user services for the two sides, and complete sequential runs: baseline must
finish and pass all local gates before candidate may start.

## Frozen runtime identity

- Upstream was freshly fetched before construction.
- Commit: `abebf33b52ebf51424f71365946eb8df1f75a23c`.
- Tree: `214bea9f3257f5336c36c4278b1d64a0cf378be0`.
- Baseline runtime:
  `/tmp/erark-t4-formal-current-20260714-attempt3/baseline`.
- Candidate runtime:
  `/tmp/erark-t4-formal-current-20260714-attempt3/candidate`.
- Fresh provenance manifest:
  `/tmp/erark-t4-formal-current-20260714-attempt3/attempt3-provenance-manifest.md`,
  mode `0444`, SHA256
  `6a31277f108631ee8bf1b9b72b29279cbd27cde6cc61dcead07e49997bf6cb2c`.
- Both runtimes have 4,174 regular files. Their path sets match, and their
  mode/size/content inventories differ only at `Script/Settle/default.py`.
- Baseline `Script/Settle/default.py` SHA256:
  `ecdec42b79d393e3dc5deb0d88f1ca897d052d08ffc99c0389ab2c1ce7278be5`.
- Candidate `Script/Settle/default.py` SHA256:
  `88197ef6bda5e8895e4f3a05fa0433563aaed0546bcf8bdcc108ed56acb93a1e`.
- Both `Script/Design/talk.py` SHA256:
  `481a9fc4a0f62142fcc8f77939063f8cd83367758ec59e1463b3d8b257cc4e06`.
- Both `game.py` SHA256:
  `c9d5c8ec9b75a510e0e5544c37a0a141bcd4ffa72a7bac94788c44e4fc30788c`.
- Both `config.ini` SHA256:
  `c766d3cd5a8bae9a0fa0b0eae385f9a416d0ca3966f650e7ccab9d62da74f458`.
- Both `save/5/0` SHA256:
  `a91afea82d91981bd14e40f9b3dc7ffa6392627951187d227b7b10443e1af981`.
- Both `save/5/1` SHA256:
  `45e77cfecf83ebecc980eece54b14eb981946b2f2a2af094f48e7e5844b8fdac`.
- Formal observer:
  `/tmp/erark-t4-formal-observer-attempt3.py`, SHA256
  `31932118bf625d122807cafcd3de4a7a28eaa968cae631829d83b8c942326ab9`.
- Common side launcher:
  `/tmp/erark-t4-formal-side-launch-attempt3.sh`, mode `0500`, SHA256
  `6723e3e228c8ec37839a8a5694025f7dcb9277c9b7e096abd36e3ec5f89af7e6`.
- Xvfb geometry/depth: `2100x1100x24`.

Before each side starts, the common launcher asserts its runtime hashes,
observer hash, save hashes, current working directory, empty side-log path,
and every required environment value. Any mismatch stops before the game.

## Frozen service envelope

Each side runs in its own transient user service. The two unit names and the
side-specific allocator owner/runtime/launcher argument differ; all service
properties and environment values are identical:

```text
--collect
--setenv=PYTHONHASHSEED=0
--setenv=ERARK_EVIDENCE_SEED=5270714
--setenv=LANG=C.UTF-8
--setenv=LC_ALL=C.UTF-8
--setenv=PYTHONUNBUFFERED=1
--property=Type=exec
--property=KillMode=control-group
--property=TimeoutStartSec=infinity
--property=TimeoutStopSec=30s
--property=RuntimeMaxSec=infinity
--property=StandardOutput=journal
--property=StandardError=journal
```

The absolute allocator command is the repository's
`.codex/skills/investigate-game-bug/scripts/tk_capture_slots.py run`. The
service command passes the side's fresh runtime, geometry, unique owner, then
the common launcher and side argument. The observer itself asserts and prints
the four critical environment values and prints random seed `5270714` into
each game log; the launcher separately prints the service environment,
observer hash, side, and systemd invocation ID.

Baseline unit:
`erark-t4-formal-baseline-attempt3.service`.

Candidate unit:
`erark-t4-formal-candidate-attempt3.service`.

Candidate SHALL NOT start until baseline has a complete three-sample run,
complete release frames, normal shutdown, unchanged saves, clean allocator,
and coordinator verification of every baseline gate. If baseline is invalid,
candidate does not start.

## Frozen identities and gameplay route

- NPC A: Lin, character ID 4080, the default target in the source save.
- NPC B: Jingzhe, character ID 306.
- Both sides use the same semantic inputs. Candidate also reuses baseline's
  exact window-relative click coordinates when the immediately current frame
  shows the same readable target. A layout or target mismatch invalidates the
  pair; the operator does not improvise another coordinate or route.

Route:

1. Click title command `[001]`.
2. Click visible populated slot `[005]`.
3. Click `[000]` load, then `[000]` confirm.
4. Click `[4113]` to start time stop.
5. Click `[5052]` to enter unconscious H, then press Return exactly once to
   reach the H menu.
6. Perform four oral rounds by clicking visible `[6602]` once per round.
7. For every actually presented complete wait page, first capture and inspect
   the full window, then press Return exactly once. Stop immediately when the
   H menu returns; never press a pre-counted extra Return.
8. The ejaculation panel must first appear in oral round 4. Capture it and
   click visible `[射出]`. Continue the same capture/inspect/one-Return rule
   through the oral-ejaculation, player-ejaculation, numeric, and returned-menu
   pages.
9. At the returned H menu, capture a no-input continuity frame and send
   exactly one `SIGUSR1` for sample 1 before changing target.
10. Execute Fable's four viewport steps, with a full readable frame after each:
    click the scrollbar track above its thumb to expose the character list;
    click visible `[惊蛰]`; click the track above its thumb again to obtain a
    readable selected-Jingzhe/status frame; click the track below its thumb to
    return to visible `[4115]`.
11. Send exactly one `SIGUSR1` for sample 2, then capture a no-input
    preservation frame.
12. Only after the release gate passes, click visible `[4115]` exactly once.
13. Capture and inspect every actual release wait page. At the first numeric
    settlement frame, before another Return, send exactly one `SIGUSR1` for
    sample 3 and take a no-input preservation frame.
14. Continue the capture/inspect/one-Return rule until the normal interface
    returns. Do not save the game. Close the window normally only after the
    coordinator has inspected the final frame and samples.

The discovery-only wheel inputs and ineffective Page Up are not replayed.
Attempt 2's observed oral-page pattern is an anomaly detector, not a cross-run
hard gate: round 1 had one combined page, round 2 had two pages, round 3 had
one, and round 4 had the prerequisite page, first ejaculation panel, oral
ejaculation, player ejaculation, and numeric page. If attempt-3 baseline
departs from this expectation, pause and investigate before continuing.
Candidate's hard matching target is the completed attempt-3 baseline: page
boundaries, Return count, readable semantics, physical game inputs, and route
must all match it.

## Mandatory frames

Each side records the full window at minimum for:

- title before input, save page, slot options, confirmation, loaded scene,
  active time stop, unconscious-H result, and first H menu;
- every actual oral wait page and every returned H menu for rounds 1--3;
- round-4 premise, first ejaculation panel, selected `[射出]`, Lin oral-
  ejaculation text, player-ejaculation page, numeric page, and returned menu;
- pre-switch readable Lin selection/list, every four-step viewport result,
  readable selected-Jingzhe/status, visible post-switch `[4115]`, and its
  no-input sample-2 preservation recapture;
- `[4115]` release talk and every following result/numeric page, including the
  first numeric settlement frame before and after sample 3;
- returned normal interface.

All frames are private investigation evidence until separate publication
authorization.

## Three samples and release gate

Each side emits exactly sample indexes 1, 2, and 3. Samples 1 and 2 must have
`npc_states` containing exactly Lin 4080 and no other NPC trigger.

Sample 1, before target switch:

- `target_id=4080`;
- `time_stop_mode=true`;
- `player_is_h=true`, Lin `is_h=true`;
- Lin `counts={"0":1,"21":2}`;
- Lin `shoot_position_body=2`.

Sample 2, after the four viewport steps and before `[4115]`:

- `target_id=306`;
- `time_stop_mode=true`;
- `player_is_h=true`, Lin `is_h=true`;
- Lin's complete trigger and five-experience object is byte-for-byte equal to
  sample 1;
- `npc_states` is byte-for-byte equal to sample 1.

Baseline and candidate corresponding samples 1 and 2 must be identical. Any
extra trigger, early/missing ejaculation panel, missing/extra sample, input
mistake, route change, unreadable gate, or cross-side mismatch invalidates the
pair without adding rounds or adapting the route.

Sample 3 is sent only on the first numeric release-settlement frame before the
next Return. Expected non-ownership state is target 306, time stop false, Lin
deferred counts empty, and corresponding state fields equal across sides. For
Lin experience IDs 10, 20, 78, 111, and 156, every `sample3 - sample2`
permanent-data delta must match exactly between sides. The observer proves
route state and permanent-value equality; it does not prove record ownership.

## Preregistered visible difference and invariants

The only expected ownership difference is the direct effect-527 record from
Lin's preserved `shoot_position_body=2`:

- Baseline: `无意识绝顶经验 +1` (experience 78) and `饮精绝顶经验 +1`
  (experience 111) appear under the player-root heading `博士博士:`.
- Candidate: those direct records do not appear under the player root;
  experience 111 appears as `+1` under `林:`, and Lin's displayed experience
  78 total is exactly one greater than baseline Lin's displayed experience 78
  total.
- The expected release heading is `林:`, not `林 (时停):`, because effect
  1242 executes before effect 527.
- Compare by owner and experience ID, not screen line number.
- For each relevant experience ID, the sum across root and all target groups
  is conserved between sides.
- Lin's permanent experience deltas are identical between sides.
- Later generic second-stage fields, formulas, counts, and gameplay state are
  otherwise equal. Jingzhe may have an empty internal target block, but an
  empty group is not visible evidence.

Any formula, count, persistent-state, unrelated generic-line, or total-value
difference fails the evidence. The production change may move only temporary
settlement-record ownership.

## Logs, stopping, and shutdown

- Record for each side: unit name/properties/invocation ID, allocator owner,
  slot, DISPLAY, supervisor/child/observer PID and PGID, Xvfb PID, geometry,
  interpreter, runtime, stable window ID, every input, signal, frame path/hash,
  continuity comparison, anomaly, and shutdown.
- Each game log must print the asserted environment, seed, observer hash, and
  exactly one expected zoomed fallback.
- The known current-upstream `title_flow.py` invalid-escape `SyntaxWarning`
  lines must be recorded and compared. Any warning asymmetry, traceback,
  Exception, unexpected Tcl error, or other launch anomaly invalidates the
  affected side pending review.
- If a service or display disappears before normal close, that side is invalid
  and no partial result is paired with the other side.
- After each side, verify normal service completion, all side PIDs gone,
  allocator released, source/runtime save hashes unchanged, observer/launcher
  and runtime hashes unchanged, and proof frames opened at original resolution
  by the coordinator.
- After both sides, produce a complete frame inventory and hash table, compare
  samples/page boundaries/visible ownership/totals, and obtain a fresh
  skeptical Fable evidence ruling before accepting the result.

## Fable verdict（逐字保存）

**裁定：`REVISE`** — 协议骨架合格，但有 4 处必须在任何游戏进程启动前修正/澄清的缺口。均为最小文档级修正，无需推倒重来，无需玩家介入。

## 八项检查结论

1. **attempt1/2 隔离** — 通过。诊断材料定位明确；attempt2 页面模式仅作异常探测器、candidate 硬匹配对象是 attempt3 baseline，三层无偷渡。路线知识（指令号、四步视口）来自旧 attempt 属允许的路线学习，不算证据配对。
2. **可比 pair 成立性** — 基本通过，但有缺口 A（见下）。fresh runtime 仅差 `Script/Settle/default.py`、同 save、同 observer/launcher、逐项哈希断言、相同 service envelope、顺序执行，均符合 attempt2 裁定。
3. **observer 只读性** — 通过。环境断言在游戏前失败即停，打印进日志不进 Tk 事件流，SIGUSR1 采样为读取。前提是缺口 A 确认。
4. **三层等待页规则一致性** — 一致，但"pause and investigate"缺行为约束（缺口 C）。
5. **采样时机与断言强度** — 通过。sample1 的 `counts={"0":1,"21":2}` 虽源自诊断轮观察，但它是 effect-527 比较成立的语义前提，作硬门合理，不算把 attempt2 偷渡成硬门。sample3 时机（首个数值结算帧、下一次 Return 之前）定义清晰。
6. **可见差异 + 守恒条件** — 设计上足以排除"显示修好但数值变了"：逐经验 ID 的跨组求和守恒 + sample3−sample2 永久增量跨侧相等 + 其余字段全等，三者合围。但"displayed experience 78 total"一词有歧义（缺口 B），歧义不消除则该门可能误判正确的 candidate。
7. **生命周期 stopping rule** — 基本封闭："service/display 提前消失即该侧无效"、逐侧收尾校验、双侧后全量清点均在。两个小缝：`--collect` 会回收失败 unit，须规定在回收前按 invocation ID 固化 journal；`RuntimeMaxSec=infinity` 下无挂死终止规则（缺口 D）。
8. **文档质量** — 见缺口 B 的 `博士博士:` 字面串确认。哈希清单内部自洽（无法在本会话执行校验，以 Codex 提供的清单为准；启动前 launcher 断言即是执行时校验）。

## 必须先修的最小项

- **A（唯一可能实质性的缺口）**：预注册只说 observer "prints random seed 5270714"。必须写明并核对 observer 源码确实在首次 game import（`auto_build_config` 之前）执行 `random.seed(5270714)` 和 `numpy.random.seed(5270714)`。若 observer 只打印不播种，这是真缺陷，必须改 observer 并更新其冻结哈希后重新提交预注册。
- **B**：定义"Lin's displayed experience 78 total"指数值结算页 Lin 分组内的记录增量之和（而非 Lin 的累计属性值），并确认 `博士博士:` 是 attempt2 帧中逐字观察到的标题串而非笔误。
- **C**：补一句：任何"pause and investigate"期间禁止一切游戏输入，只允许查看已捕获帧/日志；若解决问题需要路线外输入，该侧作废。
- **D**：补一句：无法按路线抵达下一个预注册页面的挂死侧，由协调者中止并判无效；`--collect` 回收前须先按 invocation ID 导出 journal。

## PASS 后的冻结条款（预告）

修正版通过后冻结：runtime/observer/launcher/save 全部哈希、service envelope、种子 5270714 与 `PYTHONHASHSEED=0`、NPC 身份与 14 步路线、四步视口、三次采样定义与门、可见差异 + 守恒条款、强制帧清单、stopping rule。执行顺序不变：baseline 完整通过全部本地门并经协调者逐项核验后，candidate 方可启动；candidate 完成后仍需一次全新怀疑视角的 Fable 证据裁定才能接受结果。

**玩家介入：不需要。** 四项修正均可由 Codex 完成后重新提交本审计。

## Follow-up prompt（逐字保存）

/investigate-game-bug

你刚把 erArk“时停解除结算归属”attempt3 预注册裁定为 `REVISE`，要求在任何游戏启动前补 A/B/C/D 四点。现在没有任何 attempt3 游戏进程启动，runtime、observer、launcher、save 与 service envelope 都未改变。请只审查四项修正是否完整执行并给最终 `ATTEMPT3 PREREG PASS`、`REVISE` 或 `FAIL`；不要因为修改很小就默认通过，也不要扩张到已在上一轮通过且没有改动的章节。

修正版完整 draft SHA256：
`6351253194decb1496b4999c58fcebda4e752ff573ab455148e6b794b892e84f`

Observer 仍为 SHA256：
`31932118bf625d122807cafcd3de4a7a28eaa968cae631829d83b8c942326ab9`

与上一版相比只有下面四处实质修改。

### A：实际播种发生在 game import 前

预注册新增：

```text
Its frozen source executes `random.seed(5270714)` and
`numpy.random.seed(5270714)` before the sole `runpy.run_path("game.py", ...)`
call, so both seeds are set before the first game import and before
`auto_build_config`.
```

Observer 冻结源码的相关执行顺序逐字为：

```python
EVIDENCE_SEED = 5270714
...
random.seed(EVIDENCE_SEED)
numpy.random.seed(EVIDENCE_SEED)
print(f"EVIDENCE_RANDOM_SEED={EVIDENCE_SEED}", flush=True)
...
sys.path.insert(0, os.getcwd())
runpy.run_path("game.py", run_name="__main__")
```

文件中没有其他 `runpy.run_path` 或 game import。环境断言在播种之前执行；Tk/NumPy 是观察器依赖，不是 erArk game import。

### B：显示总数与标题字面串

预注册新增：

```text
`博士博士:` is the exact title string read in the current-upstream attempt-2
diagnostic numeric frame, not a spelling normalization or inferred label.
```

并把 candidate 的 experience-78 门定义为：

```text
Here "displayed experience 78 total" means the sum of experience-78
record increments printed inside the Lin group on that numeric settlement
page; it does not mean Lin's accumulated experience attribute.
```

因此比较的是同一数值结算页、同一 owner 分组内 experience 78 的临时记录增量之和，不是角色永久属性。

### C：pause 期间零输入

预注册新增：

```text
During such a pause, all game input is forbidden; only already captured frames
and logs may be inspected. If resolving the discrepancy would require any
route-external input, the side is invalid rather than repaired in place.
```

### D：journal 固化与挂死处理

预注册新增：

```text
Before any normal window close or coordinator-requested service stop, export
the active unit journal by its exact systemd invocation ID into the private
evidence directory. This freezes the log before `--collect` can unload the
unit. After service completion, export the remaining lifecycle lines by the
same invocation ID and compare them with the pre-close capture.

If the title page does not become available within five minutes of service
start, or a valid route input does not produce a stable next page within 60
seconds, treat the side as hung. Send no further game input; capture the
current frame and invocation journal, then have the coordinator stop the
service and mark the side invalid.
```

请裁定：

1. A 是否证明两个 RNG 都在首次 game import/`auto_build_config` 前实际播种，而非只打印？
2. B 是否消除了经验 78“显示总数”与 `博士博士:` 的歧义？
3. C/D 是否封住 pause 临场补输入、unit 被回收前日志丢失、以及无限挂死三个缺口？
4. 若 PASS，请明确冻结上一轮预告的全部条款，并重申 baseline 全部通过后 candidate 才能启动。
5. 是否需要玩家介入？

## Follow-up Fable verdict（逐字保存）

**裁定：`ATTEMPT3 PREREG PASS`**（以修正版 draft SHA256 `6351253194decb1496b4999c58fcebda4e752ff573ab455148e6b794b892e84f` 为准）。审查范围限于 A/B/C/D 四处修正；上一轮已通过且未改动的章节不重开。

## 逐项裁定

**1. A — 通过。** 提交的逐字源码顺序证明两个 RNG 在唯一一次 `runpy.run_path("game.py", ...)` 之前实际播种，而非只打印；播种先于首次 game import，自然也先于 `auto_build_config`。observer 哈希未变是自洽的：缺口 A 的两个分支里落在"源码本已播种、只需文档写明并核对"这一支，所以只改预注册、不改 observer 是正确结果，而非疏漏。numpy 的 import 发生在播种前不影响 erArk 的随机流。两点使本裁定成立的绑定条件：(a) "文件中没有其他 `runpy.run_path` 或 game import"以 Codex 对冻结源码的逐字核对为准；(b) launcher 启动时对 observer SHA256 `31932118…` 的断言即是执行时对"被审查的就是被运行的"的强制校验——若断言失败，本 PASS 对该次运行无效。

**2. B — 通过。** "displayed experience 78 total"现在明确为同一数值结算页、林分组内 experience-78 记录增量之和，排除了"累计属性值"读法；配合守恒条款与 sample3−sample2 永久增量跨侧相等，正确的 candidate 不再会被该门误判。`博士博士:` 已确认为 attempt2 诊断帧中逐字读到的标题串，作为 baseline 侧预期字面串成立；若 attempt3 baseline 实际帧显示不同标题，按既有异常规则 pause（且受 C 约束），不得当场改写预期。

**3. C/D — 通过，三个缺口均封住。**
- C：pause 期间零游戏输入、只读已捕获材料、需路线外输入即该侧作废——临场修补路线的口子关闭。
- D 前半：按 invocation ID 在任何正常关闭或协调者停止之前先导出 journal，`--collect` 回收 unit 不再能吞掉失败日志；完成后再按同 ID 导出并与预关闭副本比对，可发现截断。
- D 后半：5 分钟标题门 + 60 秒稳定翻页门给出了 `RuntimeMaxSec=infinity` 下的挂死终止规则，且失败方向是"判该侧无效"，是保守失败而非放行——不会让不完整结果混入配对。60 秒对 Tk 翻页是宽裕的，不构成过度断言。

## 冻结条款

自本 PASS 起冻结，任何改动都使 PASS 失效、须重新提交审计：

- runtime（commit `abebf33b…`、tree `214bea9f…`、两侧目录、4174 文件清单、唯一差异 `Script/Settle/default.py` 及两侧全部逐文件哈希）、observer `31932118…`、launcher `6723e3e2…`、save `a91afea8…`/`45e77cfe…`；
- service envelope 全部属性与环境值、种子 `5270714`、`PYTHONHASHSEED=0`、Xvfb `2100x1100x24`；
- NPC 身份（林 4080 / 惊蛰 306）、14 步路线、四步视口、实际等待页三层规则（含 C 的零输入 pause 约束）；
- 三次采样定义与全部门（sample1/2 逐字段断言、全 NPC gate、sample3 时机与五项永久增量比较）；
- 可见差异 + 守恒条款（含 B 的两处定义）、强制帧清单；
- stopping rule 全部条款（含 D 的 journal 固化与挂死终止）。

## 执行顺序（重申）

baseline 先行；baseline 须完整走完三采样、全部释放帧、正常关闭、save 不变、allocator 干净，并经协调者逐门核验通过后，candidate 方可启动。baseline 任何一门失败则 candidate 不启动。candidate 完成后，结果不自动接受——仍须一次全新怀疑视角的 Fable 证据裁定（对帧清单、哈希表、采样、页边界、可见归属与总值比较）才能采纳。

**玩家介入：不需要。** 双侧运行、核验与最终证据裁定均可由 Codex 按冻结协议执行。
