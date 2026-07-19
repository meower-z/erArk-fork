`REVISE` — 三份状态文档的核心事实准确（attempt4 无效判定、evidence-blocked 降级、任务 5.6 未完成均与 action log、INVALID.md、当前 worktree diff 一致；我复核了 a=19, b=19, S=11, U=0, penalty 49 的逐行计数，属实），但有两处残留的 readiness 夸大/缺口需要修正，且当前候选的落盘状态存在一个未记录的风险。

## 文档修正（精确指出）

1. **`pr-readiness.md` 底部的 "Publication Checklist" 与顶部状态自相矛盾。** 复选框 `[x] Deterministic Tk evidence ready and inspected` 和 `[x] Fresh artifact audit passed` 未加任何历史限定，而文件第 5 行已声明当前包 `evidence-blocked`。新人从下往上读会得出"证据已就绪"的错误结论。改法：将标题改为 "Historical Publication Checklist（2026-07-13 旧包）"，或在这两项后追加"（仅对旧基线 `0268fe571` 包成立，不适用于当前包）"。

2. **`pr-readiness.md` 完全没有标识当前候选。** 全部 worktree/commit/base 字段（第 11–14 行）指向旧包 `/home/ubuntu/games/erArk-pr-edge-shared-settlement` @ `579b7c4`。当前候选实际在 `/home/ubuntu/games/erArk-pr-edge-shared-settlement-current`，基线 `72e28051e`——而且我用 `git status`/`git diff HEAD` 确认：**penalty-49 的最终生产形态是未提交的工作区改动**，叠在提交 `66db398e4`（大概率是 design.md 所说的 penalty-55 中间形态）之上。这是一个未记录的可丢失状态。改法：在 "Current Status" 段补一组当前候选字段（worktree、base、当前 diff 的 SHA-256），并把最终形态提交为一个 commit 后记录其 hash——目前任何文档引用的 commit 都不对应 penalty-49 的代码。

3. `current-upstream-attempt4-invalid.md`、`design.md` §Current PR Readiness、`tasks.md` 5.3–5.7 无需修改：措辞与证据一致，历史/当前边界清晰，未夸大。

## 旧图片/PR 文案

**保留，维持现状。** 它们已被明确降级为历史材料且未发布；旧图是唯一记录"该 bug 曾以何种玩家可见形态出现"的一手材料，是构造新路线时的症状规格。删除会丢失路线合同（六次等待 + 发现面板 + 结果簇）的原始定义。不需要额外改动。

## 下一步：选 A（且仅 A）

在只读诊断运行中，沿完全相同的冻结路线（save99、seed 0、`PYTHONHASHSEED=0`、六次 `[6001]`），每次等待后记录 清流/特蕾西娅/凯尔希 的各部位高潮输入、`orgasm_edge_count`、`orgasm_level` 与发现面板前提的求值结果。诊断探针只做日志输出，不得消耗 RNG、不得进入生产 diff，产物归档为诊断材料而非 PR 证据。

选 A 而非 B 的理由：A 的结果决定 B 是否值得做，反之不成立。当前最大的未解释事实是同一 seed、同一物理输入下结果簇消失——最可能的解释是上游 #215/#216 改变了代码路径从而改变了 RNG 消耗序列，但这只是候选假设，未经观测。B 现在就放弃旧簇是在原因未知时盲搜。

- **A 成功**（计数器显示 清流/特蕾西娅 在某次等待中确有多部位高潮输入进入结算，但结果不可见）：证明 bug 的前置条件在当前上游仍然发生、阻塞点在发现前提或显示层——旧路线可修复，下一步是定位那个前提，不需要 B。
- **A 失败**（六次等待中目标角色始终无高潮输入）：证明冻结路线在当前上游根本不再产生多部位同批绝顶（RNG 流分歧或上游行为变更），旧路线确认死亡——此时带着"为什么死"的证据转入 B，且 B 的搜索可以直接以"哪些状态能让目标角色进入绝顶"为约束，不再盲搜。

两个结局都有区分力；本轮不做 A/B 证据，不猜第七次等待，不扩大为开放式试玩。
