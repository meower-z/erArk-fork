**PASS。** 我独立复读了 D 的实际 diff、生产函数全文、两组测试的红绿状态与评分，D 推翻先前"包装器最低分"的结论，应保留 D、弃用包装器。逐项：

**1. 硬门槛语义等价 — 成立。** 我核对了 judge 返回后到函数末尾（812–988 行）的全部代码：除三处已改读点外，再无任何 `target_character_id` 读取，尾段仅调 `map_handle.get_map_system_path_str_for_list`（纯路径转字符串）。逐路径比对包装器语义：flag=True 的 `target_data`/`PlayerTargetName`/`PlayerNickName` 读捕获 ID = 包装器读的泄漏值；flag=False 时 NPC 自身 target 不被 judge 触碰，两设计同读；character_id=0 时 judge 的 655 行守卫不写入，捕获值=原值，无发散窗口；judge 内异常时 `common_target_character_id` 未赋值但异常传播后无人读它，finally 已恢复；judge 后异常（最终 `.format` KeyError）两设计对外均已恢复。嵌套/连续调用 save-restore 天然正确配对。测试亲手复跑：基线 8 failed/2 passed 红（stash 同环境验证后完整恢复候选），候选 focused 10 + movement 10 = 20 passed。测试第 9 项确实能拦截 flag=False 误读捕获 ID 的错误实现（会产出"不应采用"）。未找到可触发反例。

**2. penalty=17 精确无误，且是硬门槛内最低。** 主组 b=1,a=6,e=5→S=4；三处 1-for-1（a=3,b=3,e=0）；四条删除行规范化文本互不相同→U=0；(9+4)+4−0=17。更低的形态只有去掉 try/finally 的裸 save/restore（≈13），但异常泄漏正是已确认规则的一部分（focused 测试 2、6 号），不过硬门槛；在 judge 内部恢复需缩进 86 行循环体或改签名，均更大。三处 1-for-1 无一可省——省掉 elif 条件改写即产生行为回归（测试 9 拦截）。

**3. D 是更准确的 owner，不是过碎切分。** 全局临时 target 的唯一用途是 judge 内的前提计算；judge 返回后下游只需要"这次选中的 B 是谁"，这本来就是局部值。D 把全局突变的生存期收缩到恰好等于其用途，用显式局部 ID 替代跨 45 行的泄漏全局读——比包装器"让泄漏活到函数尾再兜底擦掉"更诚实。782 行的条件表达式略丑，但那是两种上下文来源的如实表达，不是碎片化。

**4. Web 与 mod 结论准确。** `handle_talk_draw` 358 行的路由读取在 306 行格式化返回之后，两设计届时均已恢复——minor dialog + `wait_input=False` 是相对 baseline 的同一待确认语义（Web 测试 5 号实测）。mod 事实核实：D worktree 无该 mod 且 `enabled_mods: []`；主树保留 `local_npc_move_talk_context_fix` 但未启用；其替换函数签名为两参 `(talk_text, character_id)` 而生产调用传三参（306 行）→ 启用即 TypeError；其 `{move}` 路径在 `call_original` 前直调 `talk.talk_common_judge`，污染发生在 D 的快照之前。真实 A/B 必须用 pristine upstream runtime 的要求正确。

**5. 裁决更替。** 先前 penalty=33 的改名+包装候选被推翻：D 以 17 通过全部硬门槛且外部语义等价，按 SKILL.md 规则 D 是应保留的候选。开放 PR #212/#217/#218 已核实（gh 实查）不重叠；talk_common 数据 68/0/0 的占位符统计实测吻合；py_compile 与 `git diff --check` 干净。先前裁决中不阻塞代码但 PR 前未完成的事项（玩家语义最终确认、真实 Tk 前后图证据、review-erark-pr-artifacts 门 + fable 文案）原样继承到 D。
