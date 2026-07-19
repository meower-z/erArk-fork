# 修正：自身状态与经验结算数值的缩写单位错误

## 问题

一次普通的看电影结算后，自身状态行显示「习得 +3M」（图1）。同屏的「学识经验 +1」正常。一次看电影的习得不应达到百万量级，缩写的单位档明显偏大。

[![修复前：看电影结算画面，习得 +3M](https://raw.githubusercontent.com/meower-z/erArk-fork/2334724784041c99e9adc498c08f6fa9b29e4c25/pr-fix-compact-value-formatting/before-watch-movie.png)](https://raw.githubusercontent.com/meower-z/erArk-fork/2334724784041c99e9adc498c08f6fa9b29e4c25/pr-fix-compact-value-formatting/before-watch-movie.png)

## 原因与修复

自身状态与经验的结算数值在缩写为 K/M 时选错了档位：千位数值被标成 M。修复后按数值实际大小选择缩写档位。

## 验证

- 同一看电影流程，修复后自身状态行显示「习得 +3K」（图2），「学识经验 +1」不变。

[![修复后：看电影结算画面，习得 +3K](https://raw.githubusercontent.com/meower-z/erArk-fork/2334724784041c99e9adc498c08f6fa9b29e4c25/pr-fix-compact-value-formatting/after-watch-movie.png)](https://raw.githubusercontent.com/meower-z/erArk-fork/2334724784041c99e9adc498c08f6fa9b29e4c25/pr-fix-compact-value-formatting/after-watch-movie.png)
