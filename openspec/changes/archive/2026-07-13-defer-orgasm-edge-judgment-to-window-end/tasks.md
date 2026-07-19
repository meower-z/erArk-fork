# Tasks: 寸止判定延迟至玩家行动窗口末尾

## 1. 前置与基线

- [x] 1.1 确认 `merge-orgasm-edge-per-action` 已归档/同步进主 spec（`openspec/specs/h-orgasm-settlement/spec.md` 含两条 edge requirement），否则先执行其归档
- [x] 1.2 跑通现有 `mod/tests/` 全量作为绿色基线，记录存档 99 BDD 回归当前断言（首个跨级掷骰、窗口复用）

## 2. 回归测试先行（先红）

- [x] 2.1 改写存档 99 BDD 回归（`mod/tests/bdd/`）：插桩 `judge_orgasm_edge_success` 记录调用时机与次数，断言"窗口内零掷骰、窗口末尾每待判角色恰一次、掷骰时 `orgasm_edge_count` 已含本窗口累积"（对现实现跑红）
- [x] 2.2 新增失败路径场景（掷骰打桩为失败）：断言窗口末尾当场释放旧积攒+本窗口累积、释放后 `orgasm_edge_count` 清空且 `h_state.orgasm_edge` 重置、解放二段效果被 flush（对现实现跑红）
- [x] 2.3 新增中途退出场景：角色在窗口内经 release fix 退出路径清算后，断言窗口末尾静默跳过、不二次释放（对现实现跑红或不适用即标注）
- [x] 2.4 单元测试改写 `mod/local_h_orgasm_batch_fix/tests/`：窗口缓存语义从 `{"success": bool}` 改为待判事件记录的合并行为（同部位跨结算合并、多角色按 ID 升序输出）

## 3. 寸止分支改纯累积

- [x] 3.1 修改 `h_orgasm_batch.py` 寸止分支（现 676-701 行）：跨级立即累进 `orgasm_edge_count`、登记 `_EDGE_WINDOW_RESULTS[character_id]["parts"]` 待判记录、不掷骰不绘制不入队口上
- [x] 3.2 删除首结算掷骰/复用逻辑与 `is_first_edge_settle_in_window` 分支，保留时停分支（`unconscious_flag_3`）原样 continue

## 4. 窗口末尾判定 hook

- [x] 4.1 新增 `init_character_behavior` 整函数接管副本并注册进 mod patch registry，manifest 更新接管声明；副本内以注释标记插入块边界
- [x] 4.2 实现窗口末尾判定函数：按角色 ID 升序遍历待判记录 → `handle_self_orgasm_edge` 前提守卫（不满足则静默丢弃）→ 调用一次 `judge_orgasm_edge_success` → 成功走提示+内联部位标题+代表部位口上，失败走当场释放
- [x] 4.3 实现失败释放：置 `orgasm_edge = 2` → 以 `orgasm_edge_count` 全量作 `un_count_orgasm_dict` 调用已接管 `orgasm_settle`（新建局部 `CharacterStatusChange`）→ 清空计数并重置 edge 状态 → flush 二段效果与数值变化绘制
- [x] 4.4 确认判定输出位于 web 文本录制关闭（`web_text_recording_flag = False`）与成就结算之前；TK 模式下输出位置在全部结算文本之后、控制权交还之前

## 5. 验证与收尾

- [x] 5.1 2.x 全部测试跑绿；全量 `mod/tests/`（含存档 99 E2E）确认效果 529、群交结束、退出清算、时停、睡眠结算链路无回归（生产修复后的远程全量 BDD 40 passed，组件/非端口及时停与睡眠分支测试均通过）
- [x] 5.2 以确定性存档 99 近真实回归替代手动 playtest：真实等待 1 小时，确认窗口内无寸止文本、末尾恰一条提示；失败释放的解放文本、派生与数值均处于同一 Web 响应边界
- [x] 5.3 更新 `mod/local_h_orgasm_batch_fix/README.md`：记录窗口末尾判定语义、失败释放量变更、`init_character_behavior` 接管的维护须知
- [x] 5.4 `openspec validate --strict` 通过；清理临时插桩/调试输出

## 6. 手动验证新发现：窗口末尾派生结算闭包

- [x] 6.1 用不落盘最小复现确认：窗口末尾失败释放已应用绝顶效果，但刻印在本窗口不输出，并在下一次 `patched_check_second_effect` 才出现；普通结算对照同回合完成
- [x] 6.2 测试先红：新增窗口末尾失败释放跨快乐/无觉刻印阈值的回归，断言刻印状态、效果与文本同窗口完成，下一窗口无遗留刻印行为
- [x] 6.3 补充自动素质边界回归：以经验 111 跨过“饮精绝顶”阈值为代表，确认新增窗口末尾入口不会额外延迟资格检查，同时保留原版素质二段行为时序
- [x] 6.4 设计并实现窄化 post-orgasm closure；禁止直接全量重跑 `patched_check_second_effect`，避免道具、插入、普通二段与绝顶判定重入
- [x] 6.5 重跑存档 99：确认多重绝顶 → 刻印/素质获取的输出归属当前窗口，下一次真实行动开头不再出现上一窗口遗留文本

## 7. 手动验证新发现：主动解放后的 p2 重复绝顶

- [x] 7.1 测试先红：以 8 部位 `un_count_orgasm_dict` 复现效果 526 主动解放，断言首批仅显示 3 个完整代表部位与其余合并摘要，并确认同一 `target_change` 的后续闭环错误调用一次 `orgasm_judge`
- [x] 7.2 实现变化对象级一次性完成标记：主动解放 batch 成功后标记角色；同一对象的目标闭环消费标记并跳过重复 `orgasm_judge` 及其第二遍宽泛消费，不影响刻印阶段
- [x] 7.3 回归确认抑制不跨对象泄漏：下一 `ChangeData` 仍正常调用 `orgasm_judge`；组件完整单元测试通过，并更新 delta spec 与组件说明

## 8. 后续 playtest 需求：标题、疲劳顺序与失败释放第二波

- [x] 8.1 新增寸止成功显示测试：多部位名称以顿号直接嵌入黄色“绝顶寸止”标题，断言不再绘制独立“寸止部位”行，代表部位口上仍只有一个
- [x] 8.2 设计疲劳两阶段门禁回归：区分行为前已疲劳与本批绝顶后新疲劳，先红断言后者的“太累了/提前离场”提示位于完整绝顶批次之后且不多执行行为
- [x] 8.3 以确定性存档 99 失败释放插桩记录每次 `patched_orgasm_settle` 的顺序、`change_data` 身份、三类字典、edge 状态、调用栈与二段强制队列；确认唯一调用及空队列后，定位真实所有者为 `b_orgasm_to_milk` 被核心宽泛 `"orgasm"` 标题分支误渲染
- [x] 8.4 在根因确认后新增红测：同一失败释放中胸部强/小绝顶并存时只显示强绝顶，低等级效果静默结算，喷乳/排尿最多一次，所有本批队列终态为零
- [x] 8.5 实现经插桩确认的最窄派生标题修复并重跑组件单测、存档 99 群交等待/失败释放回归及确定性输出顺序验证
