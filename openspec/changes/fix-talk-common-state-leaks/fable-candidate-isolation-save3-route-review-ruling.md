# PASS

## DOCS

我独立复核了证据链的每一环，全部与所声称一致：

| 声称 | 复核结果 |
|---|---|
| 候选 diff 仅一行 `part_dict = {**part_dict, "A": part_dict["A"].copy()}` 插在 `if "A" in part_dict` 分支内 | ✅ `git diff 72e2805..2f1fb08`：1 file, 1 insertion，位置正确 |
| `a=1,b=0,S=0,U=0,penalty=1` | ✅ 单组 e=1 → S=0；按最新 skill 公式 penalty=1 |
| save/3 header/data SHA | ✅ `0ef14ec…e5926aa` / `9a93092…da246` 逐字节一致 |
| 编译池 51 条同权 `adv_id=0,sys_0`，无 306 专属 | ✅ Character_Talk.json 中 face_hug_sex 共 56 条：51 条 (0, sys_0)，5 条 adv_id 350/358；惊蛰 `AdvNpc=306`，均不适用 |
| 仅 1004、1047 含 `{breast_s}` | ✅ 编译数据 breast_s cid 恰为 `insert_v_face_hug_sex1004/1047` |
| face_hug_sex 不在 Talk_Common type index，30% 替换分支不适用 | ✅ 按 `load_talk_common()` 的 `split("part_")[-1][:-2]` 逻辑重建索引（51 个 key），无 face_hug_sex；`choice_talk_from_talk_data` 的分支条件（talk.py:247）因此恒假。JSON 中出现的 "face_hug" 仅是其他 type 条目的 `dr_position_face_hug` 前提，不是索引键 |
| 标准口上会进入 mutation 点 | ✅ `code_text_to_draw_text` 对所有绘制文本调用 `talk_common_judge`（upstream talk.py:754），upstream 662-665 为原地 `part_dict["A"] += common_s_A_list`，作用于全局配置字典 |
| 概率 | ✅ 2/51 每次；4/2601≈0.154%；P(≥2 hit in 10)=1−(49/51)¹⁰−10·(2/51)(49/51)⁹≈5.61% |

save3 内部状态（时间/急诊室/实行值≈1170）与指令编号 [5047]/[6301]/[09]/[6311] 我未重新反序列化验证，按已记录事实接受（哈希已锚定存档身份，Tk agent 反正按可见帧选择而非按编号盲输）。

**文档 PASS。** 无事实错误。一条建议补充（非错误，一行即可，日后在 main worktree 补）：51 条池中的 `_s` 占位符只有 `penis_s`（18 条，被 `"penis" not in key` 守卫排除）和 `breast_s`（2 条）。这意味着 **breast_s 是该池中唯一能触发 mutation 的通道**——这是下面 A/B 合同的流一致性保证的前提，值得写进路线文档。

## EVIDENCE VALUE

**继续，不冻结为 blocker。** 理由：

1. 5.61% 是"随机 seed 下"的概率。seed 一旦离线选定，命中与否是确定的——低概率不是活体取证的成本，只是离线筛选的成本。
2. 存在一个可证明的**流一致性保证**：同 seed、同 `PYTHONHASHSEED`、同输入下，baseline 与 candidate 的 RNG 流逐位相同，直到**第二次 `{breast_s}` 展开的 A 部位 `random.choice`** 才可能分叉。依据：候选那行只做字典/列表拷贝，不消耗 RNG；第一次命中时两边 A 列表内容长度相同（baseline 污染全局后使用 vs candidate 拷贝后使用），选择结果与 RNG 消耗完全一致；两次命中之间没有其他消费者读取被污染的 breast_s A 列表；池中唯一其他 `_s` 占位符 penis_s 不触发 mutation。所以两边的命中序数、口上 CID、以及 hit-2 之前的全部可见文本**保证一致**——A/B 可比性不靠运气。
3. 路线短（≤12 次玩法选择）、纯正常玩法、无存档修改。这正是 skill 要求的"representative, easy-to-understand real Tk player flow"。

诚实的弱点：证据本身是"同 seed 同操作下第 k₂ 次文本中一个短语不同"，对人类 reviewer 需要图注解释 seed 匹配。这是该 bug 可见性的下限，可接受，但 PR 文案阶段要正面处理。

## NEXT CONTRACT

三阶段，禁止任何"live 换 seed 重试"：

**阶段 0 — 只读 headless seed 预测（允许，非试玩）**
- 用真实游戏模块写一个只读 replayer：skill 标准 overlay（`random.seed`/`numpy.random.seed` 在 `auto_build_config` 之前），加载 save/3 副本，无 GUI，按固定路线驱动同一批生产函数。
- 按 **seed = 0,1,2,… 升序扫描，上限 200**，取**第一个**满足全部条件的 seed：(a) 10 次抽文内 ≥2 次 `{breast_s}` 命中，序数 k₁<k₂≤10；(b) 在 hit-2 的 RNG 状态上分别模拟 baseline 列表（原 A + 2×common）与 candidate 列表（原 A + 1×common）的 `random.choice`，**两个短语必须不同**；(c) 记录 (seed, k₁, k₂, 两次命中的口上 CID, 双方预测短语)。
- 期望约 18 个 seed 内命中；200 个全失败的概率约 10⁻⁵ → 若耗尽，记 evidence blocker，**不进 GUI**。

**阶段 1 — 一次 instrumented 探针（恰好一次）**
- baseline runtime + 只记录不改行为的日志 overlay（永不入生产 diff），选定 seed，`PYTHONHASHSEED` 在进程启动前固定。tk-visual-runner 走路线至第 k₂ 次抽文。
- 通过标准：日志的 (k₁, k₂, CID) 与预测完全一致。
- 不一致 → **不换 seed**。允许修一次 predictor 的 RNG 消耗建模并重探**一次**；第二次不一致 → BLOCKED，记录"真实启动/GUI 存在未建模 RNG 消耗"这一具体 gap。

**阶段 2 — 正式 baseline/candidate A/B**
- 两侧 pristine runtime（无日志 overlay，只有 seed overlay），同 seed、同 `PYTHONHASHSEED`、同 save/3 副本、同显示几何。物理输入为书面固定路线：`[5047]` → `[6301]` → `[09]` → `[6311]` 重复至**恰好 k₂ 次抽文**，每步由 tk-visual-runner 从当前已检视帧选择，逐帧捕获每次抽文后的口上画面，保留 k₁、k₂ 两对全分辨率帧。
- **有效条件（全部满足才算证据）**：两侧命中序数与口上 CID 在 k₁、k₂ 完全相同；k₂ 之前所有可见口上文本两侧逐字相同；k₂ 帧上 baseline 与 candidate 的 breast 短语**不同**且与阶段 0 预测一致，且短语在截图中清晰可读。
- **INVALID 条件**：两侧 k₂ 短语相同（即使其他都匹配）——同图不能证明分叉，作废；命中次数/顺序/CID 任一不匹配；任何偏离书面路线的输入；任何存档或运行中修改。INVALID 不触发换 seed 重跑，而是回阶段 0/1 诊断（predictor 已预验短语分叉，live 出现相同短语本身就是失配信号）。
- 配置列表长度、trace、日志只进本地 manifest 佐证 provenance，**不得替代截图**。

**第 4 问的直接回答**：玩家可见证据要证明的是——同一存档、同一 seed、同一操作序列下，第 k₂ 次对面抱位的口上措辞因候选修复而不同（baseline 显示被污染权重的结果，candidate 显示原始配置的结果）。两侧短语碰巧相同 → **必须 INVALID**。

**第 5 问**：无需 PLAYER INPUT REQUIRED。按 stopping rule，下一步可执行动作是阶段 0 的 headless predictor（只读，不改生产文件，不进 GUI）。
