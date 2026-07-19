/investigate-game-bug

你是 erArk 修复方案的最终设计审查者。请以怀疑视角独立判断，不预设现有计划正确，也不要因为我已经写了测试就迁就方案。

事实（当前 upstream/master 72e28051e）：
1. Script/Design/talk.py 的 talk_common_judge(now_talk, character_id) 遇到 NPC 触发的通用占位符、NPC 与玩家同场景且玩家原目标不是该 NPC 时，会把 cache.character_data[0].target_character_id 临时改成该 NPC，但从不恢复。
2. code_text_to_draw_text 先调用 talk_common_judge；选择器生成的纸娃娃地文会传 common_talk_flag=True，随后把格式化角色切换成玩家，并从玩家当前 target_character_id 重取 target_data，最后才对展开得到的文本执行 .format(TargetName=target_data.name, clothing..., etc.)。
3. 生产 data/talk_common 中至少 66 个 CSV 文件的展开结果含 {TargetName}。因此若在 talk_common_judge 返回前恢复，当前这一句会把 {TargetName} 格式成玩家原来的旧目标，而不是正在产生纸娃娃地文的 NPC。
4. 红灯测试：玩家原目标=陈(2)，NPC=阿米娅(1)，输入 {test_common}，被选通用文本为 目标是{TargetName}。当前上游输出正确的 目标是阿米娅，且前提计算期间目标为1，但函数返回后玩家目标错误留在1；前提计算抛 RuntimeError 后目标也错误留在1。玩家自己触发时目标保持2。
5. 用户要求这是独立小 PR，行为语义不变，必须覆盖正常和异常恢复。

候选边界：
A. 在 talk_common_judge 内 try/finally 恢复。已知会在外层 .format 前恢复，因而让当前 {TargetName} 读到旧目标。
B. 把现有 code_text_to_draw_text 重命名为私有实现；保留同签名的公开包装函数，在调用私有实现前保存玩家目标，并在 finally 恢复。这样通用选择及之后的全部格式化都处在临时目标期间；没有通用占位符时只会将同值写回。
C. 改 talk_common_judge 返回展开文本和临时目标元数据，外层显式传 target_data，不改全局玩家目标或只在前提判断时临时设置；这会改更多接口与格式化上下文，但可能更纯。
D. 你认为更好的其他边界。

请检查：逻辑 owner、当前可见文本不回归、异常安全、普通/玩家口上行为、是否存在调用者依赖永久泄漏、以及最小充分测试。先给明确裁决。若 B 不可接受，请给具体替代。若 B 可接受，也请指出它是否过宽，以及需要哪些测试才能证明没有掩盖别的状态修改。最后按新版评分说明硬门槛通过后怎样比较：penalty=(新增非空行+删除非空行)+特殊语句数-2*不可避免行数；特殊语句包括 try/finally，每个特殊语句按语法次数计。不要替我写 PR 文案。
