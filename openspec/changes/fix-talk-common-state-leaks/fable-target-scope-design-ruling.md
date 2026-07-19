**裁决：B 可接受，且是硬门槛内惩罚最低的边界；A 否决；C 否决。** 但 B 有一个你事实清单里没列出的可见行为变化（Web 对话框路由），必须写进设计记录并作为暂定语义决定处理，见下。以下均已对照 `72e28051e` 实际源码核实，不是转述你的陈述。

## 各候选判定

**A（talk_common_judge 内 try/finally）— 否决，硬门槛失败。** 已核实回归面比你说的更宽：`common_talk_flag` 分支把 character_id 切成 0 后，不只 `{TargetName}`，还有 `PlayerTargetName`（直接读 `player_data.target_character_id`，talk.py:794）和全部 `Target*ClothName` 系列（`character_id == 0` 门控，读 target_data 衣物）都会格式化成旧目标。A 让至少 66 个生产文件的当前可见输出回归多个占位符。

**C（返回元数据、显式传 target）— 否决，不可行而非只是过宽。** 关键事实：前提计算发生在 talk_common_judge **内部**，`get_weight_from_premise_dict` 走 handle_premise，而 premise 函数从 cache 全局读玩家目标，不接受参数注入。所以临时目标必须在 talk_common_judge 执行期间就生效于全局——C 要么退化成"callee 设置、caller 恢复"的分裂所有权（比 B 差），要么要给 handle_premise 全家穿参数（远超小 PR）。

**B — 接受。** 逻辑 owner 论证：临时目标的必要生存期从 talk_common_judge 的前提计算开始，到 code_text_to_draw_text 末尾的 `.format` 结束（talk.py:945 `TargetName=target_data.name`）。跨两个函数的作用域，其最外层收束点就是 code_text_to_draw_text，所以恢复责任归它。重命名+同签名包装是在不缩进 250 行函数体的前提下获得整函数 try/finally 的最小写法。上游 `talk_common_judge` 只有这一个调用点（已 grep 全库确认），所以 B 覆盖全部上游泄漏入口，包括 event_option_panel、draw_event_text_panel 等非 handle_talk_draw 调用者传 NPC id 的情形。

## B 是否过宽 / 是否掩盖其他状态修改

已做写者审计：`Script/Design/handle_premise/` 整个包内 `.target_character_id = ` 赋值为 **零处**；talk.py 内唯一写点就是 656 行泄漏本身。call tree 其余部分（value_handle、map_handle、game_config 查表）无嫌疑。结论：B 的无条件恢复在非泄漏路径上是同值写回，不存在被掩盖的合法持久写。这个"不掩盖"证明是静态的（写者清单），写进设计记录即可，测试无法一般性证明不存在掩盖——别为此造测试。

## 你没列出的两个发现（必须处理）

1. **Web 路由兄弟读点（talk.py:358-360）。** `handle_talk_draw` 在 code_text_to_draw_text 返回**之后**读 `player_data.target_character_id` 决定主对话框还是小对话框。当前上游因永久泄漏，非目标 NPC 的纸娃娃地文会进主对话框并要求玩家 wait_input；B 恢复后它进小对话框。任何正确的泄漏修复都改变这个读点，无法回避。我暂定裁决：小对话框才是该路由注释声明的设计意图（"其他角色显示在头像下方的小对话框"），主框表现是泄漏喂出来的兄弟症状，B 顺带修对了。但这是可见 Web 行为变化——按 skill，PR 改了 Web 可见行为就需要补充 Web 检查，且此语义选择需用户在提交前最终确认。Tk 侧已核实无泄漏后读点（富文本绘制路径不读玩家目标），Tk 可见文本在 B 下逐字不变。
2. **本地 mod 组合缺口。** `local_npc_move_talk_context_fix` 直接调 `talk.talk_common_judge` 后才走 `call_original("code_text_to_draw_text")`——包装器在入口保存的是**已被 mod 泄漏污染后**的值，恢复等于固化泄漏。B 作为上游 PR 无碍，但本地 assumed-upstream 验证时必须先停用该 mod 的 `{move}` 路径职责，否则遮蔽核心修复效果。

## 最小充分测试

1. NPC 正常路径：输出仍为"目标是阿米娅"（可见文本不回归），返回后玩家目标恢复 2。
2. 异常路径：前提计算抛 RuntimeError，异常照常传播且目标恢复 2。
3. 玩家自触发（inverse）：character_id=0，`{TargetName}`→陈，目标保持 2。
4. NPC 触发但无通用占位符：目标全程不变（证明包装器同值写回无副作用）。
5. Web 路由变化：一条针对 add_dialog_text 分支的断言，或至少设计记录+补充 Web 证据。测试 1+2 满足你的要求 5；3+4 是防 A 型回归和防作用域错误的最低代价保险。

## 计分

先纠正一处：你转述的公式（"特殊语句数""不可避免行数"）**不是**已提交 skill 的定义。`76b1251aa` 版本里 `S` 是新结构附加费（每 change group 取 `max(净新增-1, 0)` 求和），`U` 是去重信用（多点删除同文归并到共享实现才计），try/finally 本身不单独计费。按权威定义算 B：包装函数约 14–17 非空行（含项目强制的中文 docstring）+ def 重命名 1 增 1 删 → `a≈15–18, b=1`；包装块是一个净新增 group，`S≈13–16`；无去重 `U=0`；penalty ≈ 28–35。A 未过硬门槛不参与比较；C 行数严格多于 B。故 B 是过门槛候选中的最低惩罚项。docstring 占了 penalty 大头，但它是项目风格硬门槛，不许为分数削减。

**行动项**：设计记录须补入 Web 路由语义变化（暂定按 B 的行为放行，用户提交前确认）和本地 mod 停用边界；测试补第 4 条和 Web 路由覆盖。其余按 B 实施。
