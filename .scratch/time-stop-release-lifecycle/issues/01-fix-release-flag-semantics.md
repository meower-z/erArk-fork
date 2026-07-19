Status: needs-triage
Type: task

# 修正时停释放标记的零计数语义与遍历快照

`Script/Settle/default.py:6716` 零计数 NPC 也被置 `time_stop_release = True`;`:6711` 遍历 `cache.npc_id_got` 无快照。先在当前上游代码上复核仍成立,再决定是否做成 upstream PR。详见本目录 spec.md。
