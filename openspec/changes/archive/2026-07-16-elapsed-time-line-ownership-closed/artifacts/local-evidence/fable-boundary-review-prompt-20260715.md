/investigate-game-bug

只做代码边界裁定，不编辑文件，不扫描无关目录。请直接读取：
- /home/ubuntu/games/erArk-pr-elapsed-time/local_evidence/design-reassessment-20260715.md
- /home/ubuntu/games/erArk-pr-elapsed-time/Script/Design/settle_behavior.py
- /home/ubuntu/games/erArk-pr-elapsed-time/Script/Design/update.py
- /home/ubuntu/games/erArk-pr-elapsed-time/local_tests/test_elapsed_time_line_ownership.py
并用 git -C /home/ubuntu/games/erArk-pr-elapsed-time diff upstream/master...HEAD 核对当前补丁。

需要裁定四点：
1. 上游在同一个结算面板尾部用同一个角色局部 add_time 二选一显示 X分钟过去了 或 该行动将持续X分钟；后者也是结算阶段文本，并非行动选择前预览。用户希望二者都从角色面板删除，只由最外层 game_update_flow 显示一次净实际经过时间。候选保留后者 penalty 30；两者都删 penalty 27。两者都删是否是正确且更小的同一修复边界，还是必须拆成另一个体验改动？
2. 用户明确说若认可就删除且无需因此重跑 Tk。能否执行？
3. Web 旧实现会把包含局部时间句的 now_text 写入 web_instruct_texts，并 emit_realtime_text 为 instruct。合并后唯一时间句在 game_update_flow 生成。当前 update.py 显式在 Web 写入同一缓存并发同一类型，Tk 用 io_init.era_print。用户要求 Web 只从多条变一条，其余行为不变。这个 Web 分支是否必要且正确？是否存在 P2 级必须修改的问题？
4. 本地未跟踪测试是否应把 preview remains 改成两个角色局部时长句都不存在，同时保留 Web 恰好记录一次的断言？

输出必须以 PASS 或 NEEDS_REVISION 开头，然后逐项给出短答案和任何必须修改项。
