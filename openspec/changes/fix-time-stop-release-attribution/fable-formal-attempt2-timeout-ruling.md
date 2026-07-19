/investigate-game-bug

你是 erArk“时停解除结算归属”正式 matched Tk A/B 的监督者。请以怀疑视角裁定 attempt2 的证据效力，以及下一次运行应采用什么监督方式。不要因为基准版已经花了约 25 分钟、路线看起来正确或重新运行很贵而保留不完整结果；也不要默认我提出的 systemd 方案就合理。若有更小、更可信的办法，请直接指定。候选版从未启动，当前没有任何方向性的候选结果可供迎合。

## attempt2 已确认事实

- 当前 upstream：`abebf33b52ebf51424f71365946eb8df1f75a23c`，tree `214bea9f3257f5336c36c4278b1d64a0cf378be0`。
- fresh attempt2 provenance manifest SHA256：`5c9db51515304fc5ad777c1dffcb96bf7e69510fece44a2283683a0771a9bb40`。
- formal observer SHA256：`e21ee71b9dbd679a6305ad40de6c5f3f25935ed6ae90b25cd4d58f07d7305053`。
- sequential launcher SHA256：`7a702345a6a4a16fa7cc98c865d3e9d65f69aee99ef3c8477abbf86de35fff40`。
- baseline/candidate 启动前除 `Script/Settle/default.py` 外完全相同；candidate 尚未启动，candidate log 不存在。
- baseline 完成了正常鼠标读档、`[4113]`、`[5052]`、四次 `[6602]`，第四次首次出现射精面板并鼠标点 `[射出]`。页面边界符合 Fable 已批准的实际等待页规则。
- `b2-21` 可读地写明“在林的口腔射精，射出了20ml精液（醒来第一发+）”。
- `b2-24` 回到 H 菜单；无输入复拍 `b2-25` 与它字节相同，SHA256 均为 `6b97d1f009bffba2294a0af8aa1d3e3dc819ed4108e63f49a2aadfff562b13f3`，AE 像素差为 0。
- 此时主协调者只发送一次 `SIGUSR1`，baseline sample1 原文为：
  `EVIDENCE_FORMAL_STATE={"lin_4080": {"counts": {"0": 1, "21": 2}, "experience": {"10": 7, "111": 0, "156": 9, "20": 97, "78": 9}, "is_h": true, "shoot_position_body": 2}, "npc_states": {"4080": {"counts": {"0": 1, "21": 2}, "is_h": true, "shoot_position_body": 2}}, "player_is_h": true, "sample_index": 1, "target_id": 4080, "time_stop_mode": true}`
- 四步视口路线尚未开始；没有滚动、没有切到惊蛰、没有点击 `[4115]`，没有 baseline release 结算画面，也没有 sample2/sample3。

## 外部终止

- allocator 通过当前工具 cell 前台监督启动，记录的起始时间为 14:04:07 UTC。
- cell 最终返回 `Exit code: 143`、`Wall time: 1544.8 seconds`；也就是约 25 分 45 秒后，监督进程收到外部 SIGTERM。
- 视觉执行者准备四步路线第一步时，`xdotool` 立即报告 display 不存在；因此该尝试没有形成游戏输入。
- 随后的只读检查确认 supervisor、launcher、Xvfb、baseline observer/game PID 全部消失，X9 socket 不存在，allocator 三槽全 free。
- baseline log 最后一条游戏侧记录就是上述 sample1；没有 traceback、Exception 或游戏自行退出迹象。现有上游 `title_flow.py` 的三条 `SyntaxWarning` 仍在，需最终成对记录。
- baseline log SHA256：`d11100621a198c6a117930787021ff2c014c80a472a81ac150489562bb07591b`。
- action log 已逐字记录“phase6 输入前外部终止/没有输入”，SHA256：`753577a8992500fec498455adc55bc5aac498ae6d4c7882cb74499de3f5d671e`。
- baseline/candidate 的 slot5 两个存档仍分别为预注册哈希 `a91afea82d91981bd14e40f9b3dc7ffa6392627951187d227b7b10443e1af981` 与 `45e77cfecf83ebecc980eece54b14eb981946b2f2a2af094f48e7e5844b8fdac`；没有保存游戏。

这不是玩法或候选代码结果，只是承载 allocator 的工具 cell 生命周期短于整对人工 GUI 路线。attempt1 也曾因错误的键盘菜单输入在读档前作废；attempt2 是第一次正确执行路线，但在 release 前被基础设施终止。

## 可用但尚未执行的下一步方案

当前用户级 systemd manager 状态为 `running`，版本 255。可以让每一侧由独立的 transient user service 启动同一个 allocator 脚本；服务进入 user manager 自己的 cgroup，不依赖发起命令的短生命周期工具 cell。每侧仍由 allocator 独占槽位和 Xvfb，仍记录 owner、PID/PGID、DISPLAY、geometry 和日志。候选侧只在基准侧完整结束、证据 gate 通过后才启动。

拟议的新设计是：

1. 新建 fresh attempt3 baseline/candidate runtime，再次证明只差 `Script/Settle/default.py`，重新冻结 provenance；不复用 attempt2 的运行中状态或截图作为正式结果。
2. 先用一个无游戏的短暂 transient service 做跨工具调用存活/停止/日志/allocator-cleanup 预检；若不通过则不启动游戏。
3. baseline 作为一个独立 transient service 从头执行完整路线，正常关闭并完成所有事后核验。
4. 只有 baseline 有 sample1/2/3、release 画面和完整性 gate 后，才以另一个独立 service 从头启动 candidate；candidate 使用相同 seed、observer、geometry、动作、实际页面边界、Return 次数和四步视口路线。
5. 两侧仍要求对应 pre-release 状态完全相同、每个永久经验增量相同、页面语义相同；任何偏差整对无效。服务 unit 名、属性、PID、日志和停止原因进入 private manifest。

这个设计把原来“同一个 sequential launcher 内 baseline 正常退出后自动启动 candidate”改为“两个独立受监督的 side run，中间先核验 baseline”。请不要默认二者证据效力等价。

## 需要你裁定

1. attempt2 应明确记为 `INVALID / INFRASTRUCTURE TERMINATION BEFORE RESULT`，还是其中任何部分可以作为正式 baseline？
2. 下一次是否必须 fresh attempt3 从双方起点完整重跑？哪些 attempt2 材料只能作为路线/基础设施诊断，不能进入正式 A/B 结果？
3. 上述“每侧独立 transient user service + allocator”的方式是否足以维持 matched A/B 的可比性？若不够，请指定必须保留的同进程或同 DISPLAY 条件，并说明原因。
4. 是否批准先做短暂的无游戏 persistence/cleanup 预检？需要验证哪些最小事实，才允许正式游戏启动？
5. attempt3 能否把 attempt2 已真实观察到的第 1~4 轮页面边界写进预注册，然后要求 candidate 精确匹配；还是必须继续使用更宽的“每个实际页”规则？
6. 是否应先完整完成并核验 baseline，再启动 candidate；还是为了更强的同时性必须让两侧并行/同一服务？
7. 当前没有玩法语义变更或外发动作。是否需要玩家介入？

## Fable verdict（逐字保存）

## 裁定

**1. attempt2 效力：记为 `INVALID / INFRASTRUCTURE TERMINATION BEFORE RESULT`。** 无任何部分可作正式 baseline。基准侧没有 release 结算画面、没有 sample2/3，整对的核心比较对象不存在；一个只覆盖前半路线的 baseline 无法与完整 candidate 配对，收下它就等于允许两侧不等长。不因 25 分钟沉没成本保留。

**2. 必须 fresh attempt3 双侧从头重跑。** attempt2 材料的可用边界：
- **可复用**：两个 slot5 存档（哈希与预注册一致，未被写入）、已验证的四步视口路线文本、observer/launcher 脚本本身（重跑前重新哈希入新 manifest）。
- **仅作诊断，不入正式结果**：全部截图（含 b2-21、b2-24/25）、sample1、baseline log、action log。它们证明路线可行和幂等复拍成立，这有价值，但归档到 diagnostics，不进 A/B 证据链。
- provenance manifest 必须重冻结，不继承 attempt2 的。

**3. 独立 transient service 足以维持可比性——但要认清可比性从哪来。** 它从不来自同进程或同 DISPLAY：原 sequential launcher 里两侧本来就是不同进程、不同时间。可比性来自：相同 seed + `PYTHONHASHSEED`、相同 overlay、相同存档、相同 Xvfb geometry/depth/字体环境、相同输入序列、相同 observer。必须保留的条件是这些，而非共居。两个注意点：
- systemd user service **不继承发起 shell 的环境**。`PYTHONHASHSEED`、seed、locale 必须显式写进 unit（`--setenv`），并在两侧游戏日志里各自打印确认，不能只靠 unit 定义。
- 两侧 unit 除名字外属性逐项相同，写入 manifest。

比 systemd 更小的办法（`setsid`/`nohup`/`tmux`）的存活性恰恰是未经验证的假设——harness 终止时是否清理整个 cgroup 不明。`systemd-run --user` 是一条命令、无新脚本、生命周期归属可证，这里它就是最小可信方案。**批准。**

**4. 批准无游戏预检。** 放行正式游戏启动前需验证的最小事实：
1. service 在发起它的工具 cell 结束后仍 `running`（从另一个后续 cell 查证）；
2. 日志跨 cell 可读；
3. `systemctl --user stop` 能杀死整个 cgroup，包括测试用孙进程（在测试 service 里 spawn 一个子进程验证其一并消失）；
4. allocator 槽在 service 内正常 acquire，stop 后正常释放，`status` 干净；
5. unit 上设置的测试 `PYTHONHASHSEED` 确实出现在 service 进程环境里。

五条任一不过，不启动游戏。

**5. 继续使用“每个实际等待页”规则，不把 attempt2 边界写成硬性预注册。** 理由：真正的有效性 gate 是 attempt3 内部 baseline↔candidate 的逐页配对（pre-release 状态、经验增量、页面语义完全相同，任何偏差整对作废）——这已在你的第 5 条设计里。attempt2 的第 1~4 轮边界可作**预期值/异常探测器**：attempt3 baseline 若偏离它，暂停并查明原因再继续；但 candidate 的匹配对象是 attempt3 baseline，不是 attempt2。把跨 attempt 精确匹配设为 gate 只会把无关的环境噪声升级成整对作废。

**6. 顺序执行：baseline 完整结束并通过全部核验后，才启动 candidate。** 同时性对确定性 seed + 相同输入的设计没有增益，反而引入资源竞争和显示环境差异风险。批准你的顺序设计。

**7. 不需要玩家介入。** 无玩法语义选择、无外发动作。按上述裁定继续执行 attempt3。
