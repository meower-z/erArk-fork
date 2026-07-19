# ADR-0001: 本地修复以独立 mod 组件交付,上游文件保持干净

日期:2026-07(自 openspec `local-mod-componentization` / `local-bugfixes` 蒸馏)

## 决策

1. 所有本地 bug 修复和增强通过 mod loader 的函数替换实现,放在 `mod/<component>/`;活跃开发分支上不保留对上游 `Script/`、`static/` 的脏改动。无法用函数补丁表达的改动,要么准备成 upstream PR,要么明确记录为"未迁移",不许静默留在核心文件里。
2. 组件边界按**根因**划分,不按历史症状标题:共享同一根因/不变量的症状进同一组件;无逻辑依赖的修复必须是独立组件,单独启用不需要对方。曾经的 monolithic `local_bugfix` 已退役到 `mod/deprecated/`,不被 loader 顶层扫描发现。
3. 每个保留的修复必须有可验证的根因证据;不能在当前代码上复现的历史 bug,要么以仍然成立的不变量证明保留的守卫,要么删除。
4. 组件声明的 `dependencies` 必须被 loader 强制:依赖缺失/顺序错误要有清晰诊断,不许带着部分行为静默运行。

## 后果

- 上游 rebase 成本低:核心文件无本地 diff,冲突集中在 mod 与基础设施。
- 被上游吸收的修复直接把对应 mod 从 `enabled_mods` 移除即可,盘上留档。
- 代价:每个组件要维护 manifest、测试与文档;跨组件协调(如批结算与寸止释放的双重 flush 防护)要靠显式暴露的状态钩子而非隐藏 import。
