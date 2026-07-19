/investigate-game-bug

请以怀疑视角只读审查 T7-B `fix-talk-common-state-leaks` 的候选列表隔离修复，重点判断新发现的 local save3 正常玩家路线是否足以进入真实 Tk 取证，以及应如何在不“反复试到成功”的前提下冻结随机性。不要修改文件，不要写 PR 文案，不要默认一行候选代码或路线已经很好。

已验证事实：

- current upstream/base `72e28051ebaaabb069d06059b4633fda90b0b621`。
- 独立候选 worktree `/home/ubuntu/games/erArk-pr-talk-common-candidate-isolation`，commit `2f1fb083a2d3d5a97a5ad79e4d91197c919320ab`。生产 diff 仅在现有 A 组合点前插入 `part_dict = {**part_dict, "A": part_dict["A"].copy()}`；按最新版 skill 为 `a=1,b=0,S=0,U=0,penalty=1`。
- focused baseline 3 failed；candidate focused3 + movement10 = 13 passed；py_compile/diff-check 通过。代码与测试事实已在 `candidate-isolation-implementation-notes.md`。
- local `save/3` header/data SHA 分别为 `0ef14ec...e5926aa`、`9a930923...da246`。只读受限反序列化显示：2020-03-12 12:21，急诊室，仅玩家和惊蛰306，当前目标306，双方非H，房间可锁、家具2、玩家腰技7；完整实行值约1170，超过邀请H 350、性交500。
- 最短正常玩法选择：`[5047]邀请H` → `[6301]阴道性交` → 体位面板 `[09]对面抱位` 执行第一次 → `[6311]对面抱位` 执行第二次。继续 `[6311]` 可重复；最多十二次玩法选择可得到十次 face-hug 抽文。确认页 Return 仅是传输输入。
- `data/talk/sex/insert_v/face_hug_sex.csv` 是标准口上池。编译数据给惊蛰 51 条同权 `adv_id=0,sys_0`，没有 CID306 专属项；只有1004、1047含 `{breast_s}`。
- `face_hug_sex` 不在 `data/Talk_Common.json` type index，故 save3 虽开启纸娃娃率3，`choice_talk_from_talk_data` 的30%替换分支对该行为不成立。每次命中 `{breast_s}` 精确概率2/51；前两次都中约0.154%；十次中至少两次约5.61%。
- 一旦命中，current upstream 在 `talk.py:662-665` 对全局 breast-short A 列表原地追加 shared common_s A；下一次命中看到更长列表和变化后的重复权重。候选只复制本次 A 后追加。
- 这只是生产可达性，不是 Tk A/B。没有 seed 扫描、GUI、存档修改或生产编辑。完整记录 `candidate-isolation-save3-route.md`。
- 独立 target-restoration scope 的 save99 路线已证明无有限等待次数；其他 save 也未找到十二选择内路线。不得混成一个证据任务。

请裁决：

1. save3 路线、51池/2命中、纸娃娃替换不适用、概率与生产 mutation 的证据链是否准确；文档是否 PASS。若事实有错，给最小修正。
2. 在 behavior-changing PR 需要 real-Tk before/after 的前提下，这条低概率路线是否值得继续，还是应冻结为 evidence blocker。
3. 若继续，给一个不依赖开放式试玩或“换 seed 直到成功”的最小随机性方案。区分允许的只读 full-startup RNG 预测、一次 instrumented route、正式 baseline/candidate A/B；明确 seed 选择上限、物理输入、每步可见门槛、两边必须匹配的触发次数/顺序、无效条件和停止条件。
4. 判断玩家看到的证据应证明什么：配置长度/trace 不能替代截图；若两边短语碰巧相同，是否必须 INVALID。
5. 只有确实必须由玩家决定时才写 `PLAYER INPUT REQUIRED`；否则按 stopping rule 给出可执行裁决。

请以 `PASS`、`REVISE` 或 `BLOCKED` 开头，分 `DOCS`、`EVIDENCE VALUE`、`NEXT CONTRACT`。不要修改任何文件。
