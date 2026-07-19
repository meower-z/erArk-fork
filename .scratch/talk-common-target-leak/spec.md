# 通用口上临时目标泄漏(talk-common-target-leak)

迁移自 openspec change `fix-talk-common-state-leaks`(原文见 git 历史)。两个泄漏点中**候选列表隔离已落地**(`Script/Design/talk.py:663-666` 已复制 A 候选列表再拼接),**临时玩家目标恢复仍缺失**——这是本 ticket 的剩余核心。

## 问题

通用口上展开时临时改写玩家目标:`Script/Design/talk.py:655-656` 直接写 `pl_character_data.target_character_id`,到函数返回(约 :735)之间没有保存原值,也没有 `try/finally` 恢复。一次渲染会把临时目标泄漏给后续游戏状态。

## 已定的设计

- 用 `try/finally` 把临时目标限定在展开作用域内:进入时保存原 `target_character_id`,finally 中恢复,异常路径同样恢复。
- 相关历史事实:NPC `{move}` 地文主谓颠倒的根因是强制 `character_id=0`(见 [[paperdoll-name-token-design]] 记忆与 `npc-move-talk-context-fix` 规格,该部分已由上游 PR #214 承接)。

## 验证要求

无头 A/B 已有;缺真实 Tk 流程验证(原任务被存档路线阻塞)。修复后至少补一个"展开前后玩家目标不变"的回归断言。
