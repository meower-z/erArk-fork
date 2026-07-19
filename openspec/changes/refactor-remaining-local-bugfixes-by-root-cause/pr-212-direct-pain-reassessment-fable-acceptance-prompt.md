/investigate-game-bug

请验收下面完整的 PR #212 internal design record。上一轮你已裁决边界 C 和双 Tk 证据计划 PASS，但因无文件工具而暂缓文档验收。本文已按你的要求明确：两个失败方向和生产可达性、心理能力系数与连续衰减的区别及探针数值、C 的唯一 owner/True-False caller 契约/输入是 source-adjusted delta，以及两阶段 continuous tuning 是非目标。

只依据下面全文判断记录是否满足上一轮标准。输出 `PASS` 或 `REVISE`；如 REVISE，只列必须修改项。除非确有无法从用户已确认语义及代码证据决定的问题，否则不要要求玩家输入。

--- RECORD BEGIN ---

# PR #212 direct-pain reassessment

## User direction

PR #212 must still repair the original bypass: while `苦痛快感化` is active, every positive pain gain that is part of the supported pain-settlement lifecycle must become psychological pleasure rather than increasing pain. The maintainer comment is evidence to test, not an implementation specification. The candidate should retain the original broad responsibility, remove any genuine duplicate calculation, receive Fable 5 design review, and publish two independent Tk A/B comparisons: the signed negative-delta case and a direct positive-pain bypass case.

## Reproduced failures and production reachability

At `upstream/master` `abebf33b52ebf51424f71365946eb8df1f75a23c`, the existing common state settlement converts every active state-17 result, including negative values. The focused production-function probe already reproduces the first failure: negative pain is recursively posted as negative state 23 instead of reducing state 17.

Four positive-pain writers bypass that common branch and write `status_data[17]` directly:

- `handle_add_small_pain`
- `handle_add_middle_pain`
- `handle_add_large_pain`
- the pain half of `handle_extra_orgasm`

With `pain_as_pleasure=True`, production-function probes produce the following current results:

| Writer | Pain delta | Psychological delta |
| --- | ---: | ---: |
| `handle_add_small_pain` | `+20` | `0` |
| `handle_add_middle_pain` | `+100` | `0` |
| `handle_add_large_pain` | `+1000` | `0` |
| `handle_extra_orgasm` at count 1 | `+120` | `0` |

This is production-reachable. `Behavior_Effect.csv` maps the ongoing nipple-clamp and clit-clamp second behaviors (`1100`, `1101`) to effect `270` (`ADD_SMALL_PAIN`), and maps extra orgasm behavior `1080` to effect `408` (`EXTRA_ORGASM`). The clamp instructions are normal H-item actions (`[6406]戴上乳头夹` and `[6409]戴上阴蒂夹`). The pain-mark behaviors additionally use small/middle/large pain, though pain-mark acquisition is gated off while pain-as-pleasure is active.

## Reviewer claim audit

The rejected commit `21261e9513984a50fa715009655e0731d769fe15` introduced `route_pain_delta`. Its body calls `chara_feel_state_adjust` exactly once and never calls `base_chara_state_common_settle`; a dynamic probe with pain `70`, psychological adjustment `2.0`, and continuous adjustment `0.7` returns state 23 value `98` with exactly one psychological-adjustment call. Therefore the specific claim that this helper necessarily applies the psychological-pleasure ability adjustment twice is not supported by the submitted code.

There is a separate repeated-instruction fact. The existing upstream recursive common path applies the continuous repetition multiplier once while computing state 17 and again while recursively settling state 23. With raw value `100`, psychological adjustment `2.0`, and three repeated instructions (`continuous_adjust=0.7`), production functions produce psychological delta `98` and call `chara_feel_state_adjust` once. The rejected helper reproduced that existing two-stage repetition behavior; it did not introduce it. Whether that inherited double repetition multiplier is desirable tuning is a distinct semantic question from duplicate psychological ability calculation.

## Violated rule and owner

The rule is: after a pain source has computed its signed pain delta, a positive delta is admitted to the existing psychological-pleasure settlement exactly once when `苦痛快感化` is active; zero and negative deltas retain their original pain behavior. Pain-source calculation (pain mark adjustment and source-specific accumulation) remains owned by each source. Psychological sensitivity, ability adjustment, sleep/unconscious admission, caps, and change recording remain owned by the existing state-23 common settlement.

The current interface permits bypasses because precomputed direct pain writers can mutate state 17 without invoking the conversion admission rule.

## Candidate boundaries

1. **Sign guard only in the common function:** smallest diff, but leaves all four reproduced direct writers broken. Rejected because it does not satisfy the user-confirmed rule.
2. **Restore the old value-routing helper:** fixes current direct writers and calculates psychological adjustment once. However, it manually reproduces part of state-23 settlement and can drift from canonical sleep/unconscious admission or future state-23 rules.
3. **Preferred: one conversion-attempt helper that delegates to canonical state 23:** accept an already source-adjusted signed pain delta plus change records; return `False` for inactive/non-positive values; for active positive values call `base_chara_state_common_settle(..., state_id=23, ability_level=ability[36], tenths_add=False, ...)` exactly once and return `True`. The common state-17 branch and each of the four direct positive writers call it. Callers retain their original state-17 write only when it returns `False`; a `True` result must skip that write so the same delta cannot become both pain and pleasure. This helper does not calculate psychological ability coefficients, so that coefficient remains exactly once in the canonical state-23 owner. Its Chinese function documentation must state that callers pass the delta after their source-specific pain calculation.
4. **Send direct writers back through state-17 common settlement:** superficially removes direct writes, but would reapply pain adjustments already computed by those writers and would add ordinary state-17 side effects they did not previously own. Rejected as a semantic widening.
5. **Repeat the sign/flag/state-23 call at every writer:** avoids a helper but duplicates the conversion contract across five sites and makes the next direct writer easy to miss. Rejected because the bypass is caused by that scattered ownership.

## Continuous-repetition decision

The preferred helper preserves the current common path unchanged: common state 17 still computes its current final pain amount and canonical state 23 performs its existing psychological settlement. A converted direct writer enters canonical state 23 once, so repetition adjustment is applied once at that psychological stage. Removing one of the two inherited repetition multipliers from the existing common recursive path would change established tuning and is not necessary to repair either reproduced bug. Changing that tuning is an explicit non-goal of this PR.

## Falsifying checks

- Active positive common pain calls psychological adjustment exactly once and records only state 23.
- Active zero/negative common pain records state 17 and does not call the conversion helper recursively.
- Inactive positive/negative common pain preserves upstream state-17 behavior.
- Active direct small/middle/large pain and extra-orgasm pain do not increase state 17; each enters canonical state 23 once.
- Inactive direct writers preserve their exact existing state-17 amounts and source-specific formulas.
- The canonical state-23 sleep/unconscious guard remains effective for converted direct pain.
- Repeated-instruction probes distinguish psychological ability call count from the inherited continuous multiplier.

## Evidence plan

Publish two separate real-Tk A/B comparisons from frozen saves and identical inputs:

1. `[4103]体控-强制高潮`: before shows negative pain misrouted as a huge negative psychological change; after shows pain decreasing and ordinary state-17 side effects preserved.
2. Active `苦痛快感化` plus a normal clamp second-effect route: before shows pain increasing despite conversion being active; after shows the same positive source no longer increasing pain and instead adding psychological pleasure.

The two comparisons demonstrate the inverse halves of one signed routing rule. Old PR screenshots are not reused.

--- RECORD END ---
