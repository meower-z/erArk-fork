# 修正实际射精量与无精液高潮流程

Status: ready-for-agent

## Problem Statement

玩家的基础精液和临时精液共同参与实际射精，但当前通用射精流程在扣除临时精液后，会把一个已经被改写的中间值返回给下游。临时精液处于特定范围时，界面已经按完整射精量显示、资源也已经正确消耗，但污浊、射精位置、受孕相关刷新和料理材料判定等下游逻辑收到的量偏少，甚至会把一次真实射精判定为没有射精。

当玩家射精槽达到高潮阈值、但基础精液与临时精液合计不超过 2 ml 时，当前流程仍把事件登记为普通小量射精，并强制要求玩家选择射精对象和部位。玩家完成没有实际意义的选择后，系统才告知已经无法射出精液。普通射精二段行为还会增加射精经验、射精次数、目标润滑和目标精液经验，使一次没有实际排精的高潮被错误记录为射精。

衣柜中的“用衣服冲，射在上面”也没有前置精液量守卫。玩家在无精液状态下仍能进入衣物选择，选定衣物之后才得到无精液结果。

这些问题让“高潮”和“实际射精”成为同一个错误身份，也让通用射精函数对同一次射精给出彼此矛盾的数量。修复必须保持改动小、边界清楚，并拆成三个互不混杂、可独立审阅和验证的上游 PR。

## Solution

通用射精流程应始终返回本次真实排出的完整精液量，不受其中多少来自临时精液影响。资源扣除、显示量、全局统计和下游记账必须使用同一个实际射精量。

引入独立的“无精液高潮”二段行为。无精液高潮属于高潮，但不属于射精：玩家达到高潮并承担属于高潮本身的后果，同时跳过射精对象和部位选择，不增加任何射精统计，也不产生精液相关目标效果。该行为使用专用系统文本，并在结算后清空射精槽、结束忍耐状态。

衣柜在玩家基础精液与临时精液合计不超过 2 ml 时，不显示“用衣服冲，射在上面”。闻衣物、偷内裤、偷袜子和返回等既有操作保持不变。

三个修复分别实施、测试、截图和提交。每个 PR 只处理一个根因，不顺手处理调查中发现的其他射精面板、动态事件或衣柜问题。

## User Stories

1. As a player with temporary semen, I want the game to count the full amount I actually ejaculated, so that downstream results agree with the amount shown on screen.
2. As a player whose ejaculation uses both temporary and base semen, I want both sources to be consumed correctly without shrinking the reported ejaculation amount, so that resource accounting and gameplay effects remain consistent.
3. As a player whose temporary semen is less than the ejaculation amount, I want the returned ejaculation amount to remain the full amount, so that part of the ejaculation is not silently lost from downstream records.
4. As a player whose temporary semen exactly equals the ejaculation amount, I want the action to remain a real ejaculation, so that the game does not consume semen and then report that no ejaculation occurred.
5. As a player whose temporary semen exceeds the ejaculation amount, I want only the required temporary semen to be consumed, so that base semen remains untouched and the complete ejaculation is recorded.
6. As a player with no temporary semen, I want existing ordinary ejaculation behavior to remain unchanged, so that the fix does not alter established resource consumption.
7. As a player, I want the displayed milliliters, global semen total, consumed resources and returned ejaculation amount to describe the same event, so that the game never presents contradictory quantities.
8. As a player ejaculating during ordinary H, I want target contamination and position effects to use the actual ejaculation amount, so that temporary semen is not omitted.
9. As a player ejaculating during group sex, I want the selected target and position to receive the complete actual amount, so that group-sex settlement matches the displayed result.
10. As a player using a direct ejaculation route such as a morning or evening assistant interaction, I want downstream settlement to recognize a real ejaculation even when temporary semen supplies the full amount.
11. As a player using semen as a cooking ingredient, I want a real ejaculation supplied by temporary semen to satisfy the ingredient requirement, so that consumed semen is not followed by a false material-shortage failure.
12. As a player, I want pregnancy-related recalculation to run whenever a real positive ejaculation occurred, so that an exact temporary-semen match is not treated as zero.
13. As a player whose ejaculation gauge reaches its climax threshold with no usable semen, I want to climax without being asked where to ejaculate, so that I do not make a meaningless choice.
14. As a player having a no-semen climax, I want the game to communicate that a climax occurred but no semen was expelled, so that the result is understandable.
15. As a player having a no-semen climax, I want the event to use dedicated text rather than ordinary ejaculation dialogue, so that characters do not describe semen that was not present.
16. As a player having a no-semen climax, I want my ejaculation gauge reset, so that the same completed climax does not immediately trigger again.
17. As a player ending an endurance state through a no-semen climax, I want the endurance counter cleared, so that “stop enduring” or H cleanup does not release the same climax twice.
18. As a player having a no-semen climax during ordinary H, I want the current insertion positions cleared as they are after the corresponding climax settlement, so that the completed interaction does not leave stale insertion state.
19. As a player having a no-semen climax, I want to lose the small amount of stamina and energy associated with the climax, so that the physical cost of climax remains.
20. As a player having a no-semen climax during hidden sex, I want the climax to increase exposure risk, so that a visible or audible climax remains risky even without ejaculation.
21. As a player having a no-semen climax in the human-power room, I do not want it to generate electricity, halve desire or display ejaculation-generation text, so that the new behavior does not reuse ejaculation-specific power settlement.
22. As a player having a no-semen climax, I do not want to gain ejaculation experience, so that experience reflects actual ejaculation.
23. As a player having a no-semen climax, I do not want the ejaculation counter to increase, so that lifetime and current-session ejaculation totals remain accurate.
24. As a player having a no-semen climax, I do not want to unlock an ejaculation achievement, so that achievement progress requires actual semen expulsion.
25. As a player having a no-semen climax, I do not want the target to gain lubrication from an ejaculation effect, so that target state reflects what physically occurred.
26. As a player having a no-semen climax, I do not want the target to gain semen experience, so that target experience is not awarded without semen contact.
27. As a player having a no-semen climax, I do not want semen contamination to be added to a body part, clothing or container, so that dirty-state records remain truthful.
28. As a player having a no-semen climax, I do not want a semen shooting position recorded, so that later systems cannot infer an ejaculation that did not happen.
29. As a player having a no-semen climax, I do not want pregnancy effects or condom handling to run, so that reproductive settlement requires actual semen.
30. As a player having a no-semen climax, I want no new persistent counter introduced solely for this fix, so that the patch stays small and does not change save schemas.
31. As a player reaching a no-semen climax through ordinary H, group sex, hidden sex, sleep sex, exposed sex or time-stop sex, I want the shared climax entry to apply the same semantics, so that normal gameplay routes do not disagree.
32. As a player choosing “stop enduring,” I want a no-semen release to use the same no-semen climax behavior, so that the manual release path does not reopen the ejaculation panel.
33. As a player whose ordinary H session ends and automatically releases endurance, I want a no-semen release to finish once without a second prompt, so that H cleanup is stable.
34. As a player inspecting a locker with no usable semen, I want “use the clothes to masturbate and ejaculate on them” hidden, so that the menu offers only actions that can produce their stated result.
35. As a player inspecting a locker with more than 2 ml of combined base and temporary semen, I want the clothing-ejaculation option to remain available, so that valid existing gameplay is preserved.
36. As a player inspecting a locker in a dormitory, I want the no-semen guard to apply consistently, so that dormitory lockers do not retain the invalid option.
37. As a player inspecting a locker in a locker room, I want the same no-semen guard to apply, so that location does not change the rule.
38. As a player inspecting a locker with no semen, I want the smell option to remain available, so that unrelated locker interactions are not removed.
39. As a player inspecting a locker containing panties, I want the steal-panties option to remain available when the ejaculation option is hidden, so that collection gameplay is unaffected.
40. As a player inspecting a locker containing socks, I want the steal-socks option to remain available when the ejaculation option is hidden, so that collection gameplay is unaffected.
41. As a player inspecting a locker, I want the return controls to remain available, so that hiding one action never traps me in the panel.
42. As an upstream reviewer, I want the temporary-semen correction isolated from the no-semen-climax behavior, so that I can verify one numerical invariant without reviewing unrelated domain changes.
43. As an upstream reviewer, I want the no-semen-climax behavior isolated from the locker menu guard, so that the shared climax semantics and the local UI availability rule can be reviewed independently.
44. As an upstream reviewer, I want each PR to contain only its stated root-cause fix, so that unrelated sibling problems cannot hide inside a larger patch.
45. As an upstream reviewer, I want each PR to have matched before-and-after screenshots from the same save, settings and actions, so that the visible consequence of the change is immediately clear.
46. As a maintainer, I want automated tests at stable behavior boundaries rather than tests of individual internal assignments, so that refactoring does not invalidate the specification.
47. As a maintainer, I want all three automated test groups to reuse the existing near-real no-GUI boot pattern, so that they exercise real configuration and settlement wiring without launching Tk.
48. As a maintainer, I want the established 2 ml threshold and existing semen premise reused, so that different interfaces do not invent conflicting definitions of “no semen.”
49. As a maintainer, I want the new behavior defined through existing behavior, effect and system-talk data, so that it follows the existing second-stage settlement architecture.
50. As a maintainer, I want dynamic event climax behavior left unchanged in this effort, so that an event-pipeline redesign does not enlarge three small fixes.

## Implementation Decisions

- The work is divided into three independent upstream PRs: actual ejaculation return amount, no-semen climax behavior, and locker no-semen guard. Each PR is based on the same clean upstream baseline and does not depend on the other two being merged.
- “No-semen climax” is the canonical domain term. It means that the player reaches the ejaculation-gauge climax threshold while combined base and temporary semen is at most 2 ml.
- A no-semen climax is a climax but not an ejaculation. This distinction controls UI, dialogue, statistics, achievements, contamination, position and pregnancy behavior.
- The existing combined-semen premise remains the single rule for the 2 ml boundary. The locker menu and shared climax entry reuse it rather than reimplementing the formula.
- The common ejaculation operation retains its existing resource-consumption rules. Its returned amount is changed to remain the full actual ejaculation amount calculated before temporary and base semen are deducted.
- The actual ejaculation amount is a stable event value. Temporary semen is a funding source for that amount, not a subtraction from the amount reported to downstream consumers.
- The temporary-semen fix covers all callers of the shared common ejaculation operation, including ordinary H, group sex, locker contamination, direct assistant routes and cooking.
- The no-semen branch in the shared player climax entry registers a dedicated second-stage behavior and does not open the ejaculation-selection panel.
- The dedicated behavior identifier is `p_no_semen_climax`. It deliberately avoids the substring `orgasm`, because the existing dialogue layer maps player second-stage identifiers containing that substring to ejaculation wording.
- The new behavior is declared through the existing behavior data, behavior-effect data and system second-stage dialogue data. No new Python settlement function is introduced.
- The no-semen behavior uses effects 231, 232, 411, 501 and 997: small stamina loss, small energy loss, hidden-sex exposure settlement, bilateral insertion-position reset and mandatory second-stage settlement.
- The no-semen behavior excludes effects 221, 225 and 415, plus target semen-experience adjustment: it grants no ejaculation experience/count, no target lubrication, no human-power generation/desire halving and no target semen experience.
- Human-power generation is intentionally excluded even though it is attached to ordinary small climax behavior. Its current player-facing output says the player ejaculated, and its settlement also halves desire; changing that subsystem is outside this small patch.
- Hidden-sex exposure settlement remains because the risk arises from the climax itself rather than semen expulsion.
- The new system text states that the player climaxed without expelling semen. It does not enter ordinary `p_orgasm_*` dialogue pools and does not describe an ejaculation destination.
- On the no-semen branch, the ejaculation gauge and `endure_not_shot_count` are reset before control leaves the shared climax entry.
- No persistent no-semen-climax counter, experience category or save field is added. Existing ejaculation counters are not reused.
- The shared-entry patch covers normal routes already reaching the player climax judge: ordinary H, group sex, hidden/sleep/exposed sex, time-stop sexual actions, manual stop-endurance release and normal H-end endurance release.
- The locker guard is applied while constructing the selected character’s locker action menu. At combined semen of at most 2 ml, the clothing-ejaculation action is omitted entirely rather than shown as a disabled action or followed by an error message.
- The locker guard does not change locker discovery, character selection, garment listing, contamination display, smell behavior, collection behavior or return navigation.
- The three PRs do not include opportunistic cleanup, refactoring, new abstractions or dependency changes.
- Each PR has a single commit suitable for upstream review unless repository hooks require a separate generated-data commit. Generated configuration artifacts are included only where the repository’s normal data-build workflow requires them for the relevant data change.
- Every PR receives its own matched before-and-after Tk evidence. Evidence for one PR cannot be reused as evidence for another.

## Testing Decisions

- Tests verify externally observable behavior and cross-module contracts, not local variable names, exact branch structure or the number of helper calls.
- All three automated test groups reuse the existing near-real no-GUI boot pattern used by the repository’s mod BDD tests. The test process loads real configuration, character, map and settlement wiring without starting Tk or rebinding module-level cache objects.
- The ideal test architecture is one shared boot fixture with three behavior-focused groups. No production seam is added solely for testing unless the existing boundaries prove impossible to control deterministically.
- The common ejaculation operation is the test seam for the temporary-semen PR. Tests control random ejaculation amount and unrelated bonuses, then observe returned amount, displayed amount, resource reductions and global semen-total increase.
- Temporary-semen tests cover at least four partitions: no temporary semen; temporary semen below actual ejaculation amount; temporary semen exactly equal to actual ejaculation amount; and temporary semen above actual ejaculation amount.
- For every temporary-semen partition, the returned amount equals the actual amount expelled. Total base-plus-temporary semen decreases by that amount, subject to existing availability rules.
- The exact-match regression test proves that a positive ejaculation is not returned as zero and that a downstream positive-amount branch remains reachable.
- A cooking-level behavior check is included if the near-real test can reach it without creating a new seam. Its assertion is that an exact temporary-semen-funded ejaculation is accepted as material rather than consumed and rejected. If the panel is impractical to drive headlessly, the shared-operation regression remains the required automated test and the cooking consequence is verified manually.
- The shared player climax judge is the test seam for the no-semen-climax PR. Tests arrange a player at the climax threshold with combined semen at or below 2 ml and observe second-stage behavior registration, panel invocation, ejaculation gauge and endurance state.
- The core no-semen test asserts that `p_no_semen_climax` is registered, the ejaculation-selection panel is not drawn, the ejaculation gauge becomes zero and `endure_not_shot_count` becomes zero.
- A second-stage settlement test asserts the retained effects: small stamina and energy loss, insertion-position reset and mandatory settlement output. Hidden-sex exposure is tested through its externally visible hidden-sex state or discovery-flow call only if this can be done deterministically with the existing near-real fixture.
- Negative no-semen assertions cover ejaculation experience/count, target lubrication, target semen experience, contamination, shooting position, pregnancy/condom flow, achievement flow and human-power storage/desire halving. The test may use spies at established subsystem boundaries where the real downstream setup would otherwise make the result nondeterministic.
- A positive-semen control test asserts that combined semen above 2 ml continues into the existing ejaculation-selection path and retains ordinary `p_orgasm_small`, `p_orgasm_normal` or `p_orgasm_strong` behavior selection as appropriate.
- The selected locker action menu is the test seam for the locker PR. The test uses a real locker containing clothing, captures rendered menu elements, exits through the normal return action and inspects player-visible button text.
- The locker regression test asserts that the clothing-ejaculation action is absent at combined semen of at most 2 ml, while smell, any inventory-appropriate steal actions and return remain present.
- A positive locker control test asserts that the clothing-ejaculation action remains present above 2 ml.
- The same menu construction is shared by dormitory and locker-room lockers. Automated coverage must exercise one location and confirm the shared branch; manual Tk verification covers the player-visible route. A second automated location case is added only if implementation inspection reveals divergent logic.
- Each PR’s Tk evidence uses the repository’s capture skill and the same save, configuration and user actions for the before and after image.
- Temporary-semen evidence shows a player-visible downstream difference for the exact-match or partial-temporary case. The frame must make the expended amount and resulting success/record visible; cooking is preferred if it provides the clearest deterministic contrast.
- No-semen-climax evidence shows the same climax trigger before and after: before, the ejaculation target/position selection appears; after, it is skipped and dedicated no-semen-climax output appears.
- Locker evidence shows the same character locker with the same no-semen state before and after: before, the clothing-ejaculation action is visible; after, it is absent while other menu actions remain.
- Automated tests, data rebuilds and Tk evidence are run separately for each PR. A passing later PR does not substitute for verification of an earlier one.
- Before each PR is considered complete, its diff is reviewed against this specification on both axes: adherence to project standards and adherence to the assigned behavior only.

## Out of Scope

- Dynamic event `Climax` effects, including player P climax events that directly open the ejaculation panel and non-P climax effects whose second-stage settlement is delayed.
- Redesigning or unifying the event climax pipeline with the shared player climax judge.
- Condom flows that ask for a target or position and later ignore the choice.
- Group-sex ejaculation target lists that include same-scene nonparticipants.
- Deep-throat state that rewrites a manually selected body destination to the stomach.
- Character-specific ejaculation dialogue whose premises depend on insertion state that has already been cleared.
- General audit or repair of missing, overly broad or misplaced character ejaculation dialogue.
- Changing ordinary positive-semen ejaculation behavior, effect sets or amount tiers beyond correcting the returned actual amount.
- Adding a no-semen-climax statistic, experience, achievement, save field or user-facing counter.
- Adapting human-power generation text to distinguish climax from ejaculation; effect 415 is simply excluded from the new behavior.
- Changing the semantics or threshold of the existing combined-semen premise.
- The locker smell option being displayed when the locker has clothes but no underwear.
- Locker collection behavior that may retain only the last garment while clearing multiple panties or socks.
- Reworking locker navigation, garment categories or dirty-state representation.
- Broad refactoring of ejaculation, climax, dialogue, settlement or panel architecture.
- Changes to local mods unrelated to proving that the upstream core behavior works with the current enabled-mod configuration.

## Further Notes

- This specification follows the fork’s “upstream first” rule. The fixes target upstream core behavior rather than a local mod because they correct general gameplay defects and are intentionally kept small enough for upstream review.
- The three PRs may be implemented in the order listed for ease of work, but they are logically independent and should not be stacked on one another for upstream submission.
- The actual-return fix is a numerical contract correction; the no-semen behavior is a domain-identity correction; the locker guard is a local availability correction. Keeping these explanations separate is part of the review strategy.
- The canonical threshold is inclusive: combined base and temporary semen at or below 2 ml is no semen for these flows; above 2 ml remains eligible for ordinary ejaculation.
- If implementation discovers that any normal route named in this specification bypasses the shared player climax judge, stop and report the boundary mismatch rather than expanding the PR silently.
- If a required generated artifact creates a large unrelated diff, isolate the source-data change and follow the repository’s established generated-data handling rather than hand-editing generated files.
- Dynamic event climax behavior and the other sibling defects found during investigation should become separate future efforts only if the user chooses to pursue them.
