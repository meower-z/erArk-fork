# 心理快感曲线化(curve-psychological-pleasure)

迁移自 openspec change `curve-derived-psychological-pleasure`(原文见 git 历史,2026-07-19 删除时 0/12 任务完成,未动工)。

## 目标

把 `extra_feel_settle()`(`Script/Settle/common_default.py:484`,现第 497 行仍是 `max(10, final_value / 20)` 线性换算)产生的额外心理快感,改为经实测校准、单调递增且**边际递减**的曲线,消除高输入下的无界线性增长。

## 已定的设计约束

- 只调整 `extra_feel_settle` 拥有的派生基础值;**不改**共享的状态 23 公式。
- 先实测状态 10、14、16、17 的低/中/高输入基线,再选曲线形态和参数——参数必须来自测量,不许拍脑袋。
- 能力门槛、心理经验、上限、变更记录、苦痛路由全部保持不变;非正输入维持现状。

## 剩余工作

全部:基线测量 → 曲线/参数决策 → 实现与边界测试 → 玩家可见回放验证。
