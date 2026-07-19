# PASS

五项核验全部通过，另有一项必须修正的收尾遗漏（见末尾）。核验为只读，未改动任何文件、Git 引用或 PR。

## 逐项核验结果

**1. exact base/head 的真实 Tk 重跑 — 属实。**
- 现场 GitHub API 读取 PR #218：open、draft=false、base `94d586840…`、head `4e226f4f5…`，与 contract、closure 记录逐字一致。
- 两个 runtime worktree 仍在磁盘上，`git rev-parse HEAD` 实测分别为 `94d586840…` 和 `4e226f4f5…`。
- provenance 显示真实 Tk 流程（Xvfb `:38`、slot 1、`python game.py` PID/PGID、窗口 1200x900），baseline/candidate 各 38 条物理输入，`cmp` 实测与 `expected-physical-route.tsv` 逐字节相等。overlay 三文件哈希、种子 `20260712`、`PYTHONHASHSEED=0` 与 contract 一致。

**2. 像素一致与语义描述 — 属实（独立复算）。**
- 从 assets commit `e692de85…` 现场拉取 PR 两图，SHA-256 与记录的 `584baebf…`/`1ea9a360…` 完全一致；用 ImageMagick 独立复算：新 baseline vs PR before `AE=0`，新 candidate vs PR after `AE=0`，新 baseline vs 新 candidate `AE=184656`，三个数字与归档 metrics 一致。
- 实际逐像素查看两张 final PNG：baseline 在判定成功（`1440 >= 200`）后直接续接杜宾 H 文本，无可露希尔任何反应；candidate 显示可露希尔听完解释、离开健身区并前往博士房间，`气力 -15` 与 `5分钟过去了` 各恰好一次，随后才是杜宾 H 文本。与全部记录描述吻合。
- `final/` 两图与 `frames/38-persuade-wait.png` 哈希逐字节相同，"未做裁剪"的声明属实。

**3. partial redraw / 存档不变 / WAIT 未覆盖 / PR 未修改 / 归档校验 — 全部如实记录。**
- action-log 中 35b、36b（baseline）与 20b、23b（candidate）四次 settling 捕获均为 `shot`，其后无输入插入；与 MANIFEST/closure 的四次 partial redraw 记录一致。
- `prepared-save/{0,1}` 实测哈希 = contract 期望值 = pre = post，四组全同。
- WAIT 分支未覆盖在 closure、implementation-notes、MANIFEST 中均明示。
- 归档 `CHECKSUMS.sha256` 覆盖全部 111 个文件，`sha256sum -c` 零失败；其自身哈希 `db107e95…` 与 closure 声明一致。allocator before/after JSON 与 MANIFEST 描述（slot 0 无关任务未触碰、run 后 owner 消失、slot 2 为另一无关任务）吻合。

**4. session-closure 的持久知识与诚实边界 — 通过。**
- 实测该 OpenSpec 目录整体为未跟踪状态（`??`），`CHERRY_PICK_HEAD` 确为 `767562b83…`，`Second_effect.py`/`common_default.py` 确为 `UU` 冲突。"位于 main worktree 已核验、未声称进入 main history"的区分诚实且准确。
- 持久知识清单（被否决实验、per-case 设计、MOVE/WAIT 边界、29 项矩阵、Fable 记录、发布 provenance、最终重跑）与 change 目录内容一一对应，无缺项。

## 必须修正的 finding（1 项）

- **两个 disposable root 未按 contract 删除且无记录。** `tk-final-pr218-rerun-contract-20260715.md` 明确要求归档核验后删除 `/tmp/erark-pr218-final-tk-rerun-20260715/` 与 `/tmp/erark-pr-images/discovery-settlement/pr218-final-rerun-20260715/`，两者当前均仍存在，而 MANIFEST 和 session-closure 既未声称已删（无虚假断言），也未记录"待删/保留"状态。请执行删除并在 closure 记录补一行，或明示保留理由。

次要备注（非必须）：`proposal.md` "Current Status" 段仍称 PR 为 "draft"，系创建时点的历史描述；最终重跑记录已正确写明 `draft=false`，可顺手补一句时序说明避免误读。
