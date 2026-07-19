# 通用候选列表隔离实现记录

## Scope

- PR scope：只阻止短部位通用口上展开修改全局候选列表。
- 当前上游基线：`72e28051ebaaabb069d06059b4633fda90b0b621`。
- 候选工作树：`/home/ubuntu/games/erArk-pr-talk-common-candidate-isolation`。
- 候选分支：`codex/fix-talk-common-candidate-isolation`。
- 不包含临时玩家目标恢复包装层；两个候选可独立审查、回滚和合并。
- 本地生产提交：`2f1fb083a2d3d5a97a5ad79e4d91197c919320ab`；仅含 `talk.py` 的一行插入，聚焦测试保持未跟踪、本地证据状态。

## Baseline failure

本地回归 `tests/test_talk_common_candidate_isolation.py` 在未改生产代码的当前上游上得到 `3 failed`：

1. 初始专属 A 候选为 `[1000]`、通用 A 为 `[2000]`。两次展开实际随机池依次成为 `[1000, 2000]` 和 `[1000, 2000, 2000]`；全局专属列表最终同样永久变为三项。
2. 第一次组合候选后让 `random.choice` 抛出 `RuntimeError`，全局专属列表仍从 `[1000]` 变成 `[1000, 2000]`。
3. 在 B/A/C 三个部位键且 A 已有重复 CID 时，第一次 A 随机池为 `[1000, 1000, 2000]`，第二次增长为 `[1000, 1000, 2000, 2000]`；这同时证明污染发生在保持部位顺序的正常展开中。

这证明历史渲染次数会改变后续随机权重，且异常不能回滚污染。

## Production reachability

- 配置加载器把每个分段类型构造成 `config_talk_common_cid_list_by_part[real_type_id][part_id]` 的 CID 列表。
- 生产 `data/talk_common/body_part/` 中有 12 个满足现有组合条件、同时具有 A 配置的短部位类型：`anal`、`armpit`、`breast`、`face`、`feet`、`hands`、`legs`、`mouth`、`throat`、`urethra`、`vagina`、`womb`。
- 45 个生产通用口上 CSV 文件实际引用这些短部位占位符，因此污染会影响正常纸娃娃地文，而不只是测试夹具。
- `talk.py` 中对该 `part_dict` 或其 CID 列表的唯一写入是现有 `part_dict["A"] += common_s_A_list`。

## Candidate

保留匹配 key 的原部位字典读取，只在现有 `if "A" in part_dict` 分支内把局部字典的 A 重绑定为原 A 列表副本。后续现有 A 拼接只修改本次副本；其他部位列表保持只读引用，字典顺序、列表顺序、原有重复 CID 和随机选择流程均保持不变。

最终生产 diff 为单行插入：`a=1`、`b=0`、`S=0`、`U=0`，`penalty=1`。它取代语义正确但分数为 2 的“复制全部部位列表”候选。

## Verification

- 干净 current-upstream baseline 的三项聚焦测试：`3 failed`，分别显示重复调用增长、异常后污染、以及多部位顺序中 A 的重复池继续增长。
- `python -m pytest -q tests/test_talk_common_candidate_isolation.py /home/ubuntu/games/erArk/tests/test_movement_talk_actor_context.py`：`13 passed`。
- `python -m py_compile Script/Design/talk.py tests/test_talk_common_candidate_isolation.py`：通过。
- `git diff --check`：候选工作树通过。
- 生产 diff SHA-256：`b418869cf38d453e34f758f31ca394c373581110381cca9e2ce294379a112295`。
- `talk.py` SHA-256：`3e9d14b8002300effbc58d687a3003ad29d75fdf7418fdbc4b61ca69b715f995`；聚焦测试 SHA-256：`7ef454ccc9bcbae0d21d87d68e8db799fd8f049f03ab70c3d9f600c9d19ba4aa`。
- 两个 disposable baseline linked worktree 均已移除并确认不再注册。
- OpenSpec strict validate：通过。

回归测试是本地证据，不进入上游生产 PR。真实 Tk 重复展开证据、Fable 最终实现复核、PR 文案和新鲜 artifact audit 仍待完成。

## Current Tk evidence blocker

生产加载器和真实数据给出一个确定性静态分叉：seed 0、凯尔希、`{breast_s}` 第一次在 baseline/candidate 都选择“羞涩美胸”，第二次 baseline 选择“害羞玉乳”而 candidate 选择“尴尬玉乳”。生产口上 CID 1004 与 1047 在 `[6311]对面抱位` 路径中使用该占位符。

现有 save 99 处于群交模式，不显示 `[6311]`。正常选择 `[6008]` 结束群交后，所有 NPC 仍在现场；`[5047]邀请H` 又要求现场恰好两人，因此没有证明一条无需状态注入即可从现有存档到达 `[6311]` 的玩家路线。seed 分叉是只读真实加载器证据，不是 Tk 玩家证据。任务 3.3 继续保持 open；在通过正常玩法制作可重复的单人-H reproduction save 前，不得声称 PR-ready。

## Supervision status

设计审查与最终代码/文档审查 prompt 均已原样保存；Fable high 两次都在 300 秒内没有任何输出并超时。根据玩家授权由主执行者继续，不能把任一超时记成 Fable PASS。新鲜上下文兜底审查要求把 `penalty=2` 候选进一步缩小为只复制 A 的 `penalty=1` 候选，并补多部位键与重复 CID 测试。
