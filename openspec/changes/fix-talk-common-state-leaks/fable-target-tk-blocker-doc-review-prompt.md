/investigate-game-bug

请以怀疑视角审查 erArk OpenSpec `fix-talk-common-state-leaks` 新记录的目标泄漏 Tk 证据 blocker。不要假设现有结论正确，也不要替作者寻找体面措辞。你可以用工具读取下列文件和其中引用的生产代码/配置：

- `openspec/changes/fix-talk-common-state-leaks/target-scope-implementation-notes.md`
- `openspec/changes/fix-talk-common-state-leaks/tasks.md`
- `openspec/changes/fix-talk-common-state-leaks/design.md`
- `openspec/changes/fix-talk-common-state-leaks/specs/talk-common-state-isolation/spec.md`

已验证事实：

1. 当前上游基线是 `72e28051ebaaabb069d06059b4633fda90b0b621`；候选生产提交是 `145ad51084c780e7ffc927a0ab472606802755a4`。
2. save 99 当前目标 A 是凯尔希；H 模式正确等待指令是 `[6001]`，`[1001]` 被 `NOT_H` 排除。
3. 同场其余十名 NPC 当前行为都是 `masturebate`。其首段真实文本源 `sex_masturebate0` 与林的专属 `chara_4080_林112/113` 均不含 Talk_Common 占位符。
4. 凯尔希可能产生使用纸娃娃地文的二段绝顶文本，但她就是 A，不能证明不同 NPC B 暂时覆盖 A 后未恢复。
5. 固定 `random/numpy seed=20260715`、`PYTHONHASHSEED=0` 的无界面只读生产结算在 300 秒内未返回，不能证明其他 NPC 会跨越绝顶阈值并命中纸娃娃地文。
6. 系统设置 CID 213 可以把纸娃娃比例设为 100%，但这不保证出现正常可达的 B 触发。
7. 存档未改，未取得可比 Tk A/B；OpenSpec 任务 3.2 保持未完成，文档将当前状态标为 `TK EVIDENCE BLOCKER`，不声称 PR-ready。

请判断：

- 文档是否把已证事实、未证猜测和停止边界分开；
- 这个 blocker 是否足够具体，是否遗漏一个由现有事实直接推出、且仍应在该限定 save 99 路线内执行的低成本证据步骤；
- `tasks.md` 保持 3.2 未完成是否正确；
- 将未来证据建议为“两张有顺序的全分辨率画面：B 文本帧、结算后原目标标题帧”是否足以证明玩家可见问题，还是还需更明确条件；
- 是否存在夸大、不可核验、对新人不清楚或与 spec 冲突的表述。

只输出 `PASS`、`REVISE` 或 `BLOCKED` 开头的裁决。若不是 PASS，给出必须修改的精确事实或句子；若认为还能继续限定搜索，请给出一个具体、有限、可证伪的下一步。不要写 PR 文案。
