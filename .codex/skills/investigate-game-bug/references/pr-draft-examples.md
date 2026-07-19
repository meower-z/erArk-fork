# Upstream PR Draft Examples

Read the current title and body before drafting. Imitate their altitude and economy, not their wording.

- [#210 修复群交 NPC 自动补位时意外切换玩家交互目标](https://github.com/Godofcong-1/erArk/pull/210): names the exact scene, states the visible failure immediately, then gives a short lifecycle fix and GIF evidence.
- [#211 修复无意识奸指令对睡眠和时停对象不可用的问题](https://github.com/Godofcong-1/erArk/pull/211): explains a configuration fix using existing game terms and defines only the premise tokens the diff exposes.
- [#206 修复玩家未移动时同一角色重复发现 H 行为](https://github.com/Godofcong-1/erArk/pull/206): gives only the context needed to understand the repeated discovery, then states the state-lifecycle rule and image proof.
- [#207 修复跨系统读档后房间地址不匹配导致的场景角色丢失](https://github.com/Godofcong-1/erArk/pull/207): reference for a larger fix whose affected data boundary genuinely needs enumeration.

Use `gh pr view <number> --repo Godofcong-1/erArk --json title,body,url` to read the source body rather than relying on a copied snapshot.
