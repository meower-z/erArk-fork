---
timestamp: 2026-07-19
---
# mod 组件系统与本地组件现状

本仓库把所有本地修复/增强做成独立 mod 组件,靠运行期函数替换打补丁,上游 `Script/` 保持干净(见 [ADR-0001](../adr/0001-local-fixes-as-mod-components.md))。本页记录该系统的能力边界与当前盘上组件的现状,不复述 `Script/Core/mod_manager.py` 的实现细节。

## 能力边界

补丁引擎有两种函数挂载方式,都由每个 mod 的 `mod_info.json` 声明:`type: "replace"` 把目标模块的函数替换为 mod 函数,`type: "new"` 往指定模块注册新函数。**replace 只在第一次替换时保存上游原函数**(`mod_manager.py:551-557`),mod 内可通过 `call_original` 回调它。

依赖与加载顺序:`get_sorted_enabled_mods()`(`mod_manager.py:197-231`)在 `load_order` 基础上跑一遍稳定 Kahn 拓扑排序,让被依赖的 mod 先加载,同时不打乱无依赖关系 mod 的原始配置顺序。

asset override:mod 可用 `assets.data` 声明 CSV 覆盖/合并进 `game_config.config_*`(`_merge_data_file`,`mod_manager.py:440-472`,支持 `append`/`replace`/`merge` 三种 `merge_mode`),`assets.image` 声明图片别名替换。

**本地版相对上游的增强**(均来自本地基础设施恢复提交 `41796d267`,上游 mod 系统本身来自 `4640e19cf`):
- **加载失败回滚**:每个 mod 加载前对其将改动的模块属性与全局注册表拍快照,加载抛异常时逐项还原(`_snapshot_mod_mutations`/`_restore_mod_mutations`,`mod_manager.py:344-405`),一个坏 mod 不会留下半挂状态。
- **依赖校验**:启动时检测缺失依赖与**循环依赖**并跳过报错 mod,而非静默(`_get_dependency_errors`/`_find_dependency_cycle_mod_ids`,`mod_manager.py:254-310`)。

整个 mod 系统是软失败:`init_mod_system()` 只打印失败清单、返回布尔,从不中止游戏(`mod_manager.py:659-670`)。

## 运行时唯一事实:`mod_config.json`

盘上存在哪些组件目录**不等于**启用了哪些。运行时事实只有 `mod/mod_config.json` 的 `enabled_mods`(启用集)与 `load_order`(顺序)。`scan_mods()` 扫到的全部 mod 里,只有出现在 `enabled_mods` 的才被 `load_all_enabled_mods()` 加载(`mod_manager.py:119-125`)。判断"某修复现在生效吗"一律以本文件为准。

当前 `enabled_mods` 逐字为四项(顺序同 `load_order`):`easy_mode`、`group_sex_extension`、`local_fontfix`、`local_orgasm_chain_gate_fix`。各自一句话职责:

- **easy_mode**:难度放宽——催眠随机乘数、每日理智富余转上限、爱情旅馆房价三档。
- **group_sex_extension**:群交模式的全员寸止/戴玩具/催眠增强三个批量指令。
- **local_fontfix**:Windows 下进程内私有注册捆绑的更纱黑体,免系统安装即可让 Tk 解析。
- **local_orgasm_chain_gate_fix**:点击级释放门——同一玩家动作窗口内已实际高潮的 NPC 不再生成新自主行为(上游拒收 PR #226 后落地为 mod,见 [ADR-0002](../adr/0002-orgasm-chain-gate-as-local-mod.md))。

以上四项契约与 [CONTEXT.md](../../CONTEXT.md) 一致,详细语义不在此重复。盘上还有约十个 `local_*` 目录未列入启用集(如 `local_h_orgasm_batch_fix`、`local_hypnosis_state_fix`、`local_group_edge_release_fix` 等),它们**存在但不加载**。

## 盘上禁用组件的再启用风险

**最大的坑:replace 型 mod 复制的是"打补丁那一刻"的上游函数体。** 这些禁用组件多数是在某个上游版本前写的;之后上游把同一函数改了(常常正是因为该修复已被上游 PR 吸收)。如果直接把这类 mod 重新写进 `enabled_mods`,它的 replace 会用**旧函数体**盖掉现在树内的上游实现,**悄悄回退上游改动**。例如 `local_hypnosis_state_fix` 重新启用会回退已合并的 PR #232/#233。

因此再启用任何禁用组件前,必须先对照该组件包装的上游函数是否已变化。mod↔PR 的完整对照见 [LOCAL_BUGFIX_MIGRATION.md](../../mod/LOCAL_BUGFIX_MIGRATION.md):哪些 PR 已被上游合并(对应组件应保持禁用)、哪些行为改由本地 mod 承接。

另一个陷阱:退役的 monolithic `local_bugfix` 在 `mod/deprecated/local_bugfix/` 下,`scan_mods()` 只在 `mod/` 顶层每个目录里找 `mod_info.json`、不递归(`mod_manager.py:83-89`),所以 `mod/deprecated/` 里的 mod **根本不会被发现**,即便手动写进 `enabled_mods` 也扫不到、只会记一条"已启用 mod 未找到"。

## 组件边界与测试

组件按**根因**而非历史症状标题划分,共享同一根因的症状进同一组件、无逻辑依赖的修复必须能各自单独启用;每个组件自带 manifest、测试与文档。该标准见 [ADR-0001](../adr/0001-local-fixes-as-mod-components.md)。
