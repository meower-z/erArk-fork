## Why

远处 NPC 的多重绝顶二段行为没有被标记为必须结算，因此角色离开玩家所在位置后，行为会留在队列中；NPC 以后回到玩家附近时，旧的多重绝顶口上才被显示。普通部位绝顶已经使用现有 `997` 配置语义在远处静默结算，多重绝顶应采用同一规则。

## What Changes

- 为 `plural_orgasm_2` 至 `plural_orgasm_11` 增加现有的 `997` 必须结算标记。
- 让远处 NPC 的多重绝顶效果按时结算并清空队列，同时不向玩家显示远处口上。
- 保持同房间多重绝顶的口上和效果不变。
- 不处理 `extra_orgasm`、`b_orgasm_to_milk`、`u_orgasm_to_pee`；这些效果函数会直接绘制文本，需要单独的显示系统改造。它们的同类远程滞留问题是本 change 后仍然存在的已知缺陷，不得把本 PR 描述成修复了所有远程绝顶衍生显示。

## Capabilities

### New Capabilities

- `remote-plural-orgasm-settlement`: 规定多重绝顶二段行为在远处静默结算、在玩家附近正常显示的行为。

### Modified Capabilities

None.

## Impact

修改 `data/csv/Behavior_Effect.csv` 中十个多重绝顶行为。配置构建只用于本地一致性验证，不提交生成物；复用现有 `997` 加载和远程二段行为结算路径，不修改 Python 结算或绘制代码。
