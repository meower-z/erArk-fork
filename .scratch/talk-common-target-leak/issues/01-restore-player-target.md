Status: ready-for-agent
Type: task

# 用 try/finally 恢复口上展开的临时玩家目标

`Script/Design/talk.py:655-656` 改写 `pl_character_data.target_character_id` 后未恢复。保存原值并在 finally 恢复,附"展开前后目标不变"回归断言。详见本目录 spec.md。
