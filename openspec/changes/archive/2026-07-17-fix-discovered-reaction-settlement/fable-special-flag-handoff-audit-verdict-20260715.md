# Fable 5 OpenSpec handoff-audit verdict

```text
FAIL

必须修复：

1. Handoff 未记录线上 PR 正文与已批准 v2 草稿不一致。线上标题与 v2 一致，但线上 body 仍是 ad-hoc 候选时代的旧文案；必须明确 v2 从未发布，且按用户指示不再发布。
2. Head 推送、公开回复、draft 转 ready 三个已发生的 outward PR 变更在记录链上缺失；必须补记实际状态与可确认授权，不能把未确认动作伪造成用户授权。
3. fresh-context PR artifact review 的 PASS / publication-ready 缺少留存凭证；必须补存该 verdict，或将该句降级为可核实的具体事实。

已核实：candidate `c75b3b173` 与 parent `58587deac` 一致；PR head/base 与 handoff 一致；Tk archive checksums 与像素比较通过；删除本地 special-flag worktree/branch、保留远程 PR ref 与旧 ad-hoc checkout 的边界正确。
```
