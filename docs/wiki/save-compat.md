---
timestamp: 2026-07-19
---
# 存档兼容契约

存档是整个 `cache` 的 pickle：运行数据写入 `save/<id>/1`，版本/时间/角色名等头部元数据写入 `save/<id>/0`（`save_handle.py:79`-`118`）。Linux 下靠 fork 并行落盘，子进程直接复制内存、不受玩家后续操作影响（`establish_save_linux` `save_handle.py:63`）。落盘流程的整体综述见 `.github/prompts/数据处理工作流/存档系统.md`，此处只记 grep 不出来的兼容规则与坑。

## 旧档字段迁移:新对象重建 + 旧值覆盖

`input_load_save` 先 `new_cache = game_type.Cache()` 造一个含全部默认键的干净实例，再把旧档 dict 递归补默认键（`update_dict_with_default` `save_handle.py:421`），逐角色则新建 `game_type.Character()` 并 `recursive_update(new, old)` 把旧值盖上去（`save_handle.py:294`-`296`、`recursive_update` `save_handle.py:457`）。由此推出给角色数据加字段的人**必须**知道的两条:

- **新增字段天然缺省。** 只要新字段在其类的 `__init__` 里有默认值，旧档读入时 `update_dict_with_default` / 重建对象就自动补上——不用写任何迁移代码。这是加字段安全的唯一前提。
- **删字段的残留是幽灵,不是清除。** 两条路径都只做"源→目标覆盖"，从不删除对方多出来的键。`recursive_update` 无条件把旧档实例的每个属性写进新对象（`save_handle.py:464`-`471`），所以从类定义里删掉的字段会以孤儿属性挂回新实例的 `__dict__`——不报错、也不清理，任何遍历实例属性的逻辑都会看到这个幽灵。要真正废弃一个字段，得显式在迁移里删，不能只改类定义。
- **顶层类型变更不重置。** `update_dict_with_default` 对 int/float/None 的顶层键即使新旧类型不符也保留旧值（`save_handle.py:448`），改字段类型时不要指望它帮你转。

## 版本迁移钩子:位置与触发

全部迁移集中在 `input_load_save`（`save_handle.py:212`），仅这条手动读档路径执行；`load_save`（`save_handle.py:197`）只反序列化 + 路径归一化，不迁移。触发点按序：旧版角色 ID 系统（`npc_tem_data` 为 list 时迁移，`save_handle.py:236`）、旧→新角色 ID 替换映射（`character_replacement_map` `save_handle.py:259`）、随后是补默认键、角色配置/服装/口上颜色、罗德岛资源/设施、系统设置、地图、医疗结构等一串 `update_*`（`save_handle.py:251`-`409`）。

## 跨 OS 路径归一化

只对枚举清单里的结构化房间地址字段生效，普通文本不碰。作用域决策见 `docs/adr/0004-save-path-normalization-scope.md`（实现入口 `_normalize_loaded_save_paths` `save_handle.py:150`）。

## 序列化了但必须在边界重置的运行时状态(自愈式)

有些字段随 `cache` 进了档，却**不能**信任存档里的值——读档或点击边界必须重置，否则旧值会毒化新会话:

- **`game_update_flow_running`**(刷新流程嵌套深度)随档序列化，但读档时强制置 0（`save_handle.py:289`）。否则崩溃时存下的非 0 深度会让刷新流程永久命中 `>= 2` 的拒绝分支（`update.py:13`），存档一读进来就再也刷不动。
- **`web_mode`** 读档时按当前进程覆盖，不用旧档的值（`save_handle.py:287`）。
- **逐点击重置的标记。** 本地 mod 的 `sp_flag.multi_orgasm_this_player_action` 随 `sp_flag` 序列化进档，但每次最外层玩家点击（`game_update_flow_running == 0`）开始时对全体 NPC 清零（`mod/local_orgasm_chain_gate_fix/scripts/local_orgasm_chain_gate_fix.py:68`）。这是自愈式设计的样板:标记即便被存档带出来，下一次点击自动归零，绝不跨点击泄漏——因此这类"本次点击内"的临时标记不需要专门的迁移或读档重置。给 `sp_flag` 加同类逐点击标记时，重置点应挂在最外层点击边界，而非依赖序列化后的干净值。
