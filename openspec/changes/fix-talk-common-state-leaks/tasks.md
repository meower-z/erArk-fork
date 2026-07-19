## 1. 临时交互目标隔离

- [x] 1.1 盘点 `talk_common_judge()` 设置和读取玩家交互目标的所有路径，固定正常、无需覆盖和异常三种基线行为（见 `target-scope-implementation-notes.md` Production trace）
- [x] 1.2 用作用域恢复边界实现 NPC 临时目标，保证正常返回和异常退出均恢复原目标（候选 `94eef7f5`，try/finally）
- [x] 1.3 用无头 A/B 证明展开使用临时目标而后续状态不受影响，含注入异常路径（`demo_target_leak.py`：基线 367→3 泄漏、候选 367→367 恢复，下游 KeyError 仍恢复即验证 finally 异常路径）。注：原始 pytest 回归套件为本地证据，rebase 中随旧 worktree 清除，PR 本不含测试。

## 2. 通用候选配置隔离

- [x] 2.1 盘点通用口上部位字典及候选列表的所有写操作，并记录重复展开前后的配置快照（唯一写点为 `part_dict["A"] +=`；快照见 `candidate-iso__*.log`）
- [x] 2.2 将短词 A 候选组合改为调用内复制与拼接，不修改全局部位字典或候选列表（候选 `dcee1801`，单行）
- [x] 2.3 用重复展开 A/B 证明候选内容/重复数不随历史绘制次数变化（`demo_candidate_leak.py`：基线 breast_s.A 五次 123→788、候选恒 123）

## 3. 独立验证与交付

- [~] 3.1 已跑无头确定性 A/B（`.codex-evidence/talk-common-state-leaks/`）替代原 pytest 套件（后者随 rebase 清除）；py_compile 两分支通过。原“现有纸娃娃/格式化回归套件”已不存在于当前树。
- [~] 3.2 真实 Tk 玩家可见流程两个方向均被现有存档挡住（见 `candidate-isolation-implementation-notes.md`、`target-scope-save99-wait-only-route-closed.md`），保持 TK EVIDENCE BLOCKER；改以无头 A/B 确认渲染后玩家交互目标未被永久改变。
- [x] 3.3 两个修复各为独立单提交、仅改 `Script/Design/talk.py`，可独立审查/回滚；已核实最终 diff 未包含纸娃娃来源显式传递（`codex/fix-movement-talk-actor-context`）分支的改动

## 待玩家/上游协调（非代码缺陷）

- [x] P1 玩家已确认：目标恢复后非当前目标 NPC 地文进头像小对话框（不阻塞），符合代码注释既定意图；故 PR 文案未列此"待确认"项
- [x] P2 候选列表隔离一行修复的独立最终代码复核：fable PASS（含 `key=="common_s"` 自引用边界安全性确认；`common_s_A_list` 在 rebind 前捕获）
- [ ] P3 上游合入后本地 mod `local_npc_move_talk_context_fix` 的 `{move}` 直调路径需退役/改走公开入口（污染发生在修复快照之前）
- [x] P4 fable 撰写/复核两份中文 PR 文案完成；`review-erark-pr-artifacts` 审计已跑（像素级视觉证据 BLOCKED，已记入 manifest）；上游 PR 已开：#223 候选隔离、#224 目标恢复
