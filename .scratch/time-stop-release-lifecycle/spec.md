# 时停释放的生命周期语义(time-stop-release-lifecycle)

迁移自 openspec change `fix-time-stop-release-settlement-output`(原文见 git 历史)。该 change 的三个部分中,**NPC 归属**(`Script/Settle/default.py:6718-6719`,随上游 PR #227 合并)和 **K/M 数值格式**(`Script/Design/attr_text.py:134-144`)已落地;剩余的是释放生命周期语义。

## 剩余缺口(2026-07-19 审计确认)

1. **零计数也被置标记**:`Script/Settle/default.py:6716` 对所有 NPC 无条件设置 `time_stop_release = True`;设计要求仅非零延迟高潮计数的 NPC 置释放标记(但所有 NPC 仍执行昏迷恢复清理)。
2. **遍历共享集合无快照**:`:6711` 直接遍历 `cache.npc_id_got`,结算中集合被修改会出问题;设计要求防御性快照。
3. **验证缺口**:实际运行的 Tk/Web 集成验证、实际差值与上限验证、mod 开关矩阵均未做;Web 侧验证还耦合着 `local_settlement_input_fix`(现禁用)。

## 注意

动手前先复核第 1、2 条在当前 upstream 代码上是否仍然成立——审计基于 2026-07-19 工作树,上游后续可能已改。
