`REVISE` — 旧“38输入=六次等待”合同作废，采用 **44输入合同**。我已对主证据独立复核，全部支持你的事实链，且推翻我此前 attempt7 裁决中的“谓词缺陷”归因：

- `flow_handle.py:543-547`：`askfor_wait` 仅在 `w_frame_up` 或空字符串输入时退出；`key_listion_event.py` 中 `<Return>` 绑定到 `main_frame.send_input`，从不设置 `w_frame_up`（只有鼠标左/右键经 `set_wframe_up` 设置）。非空 `6001` 被 `askfor_str(donot_return_null_str=False)` 原样返回、不 break——被暂停吞掉，代码证实。
- `character_behavior.py:265-270`：玩家结算绘制后同一 init 调用进入 `WaitDraw`，`original()` 未返回，`finally` 自然未落盘。**attempt7 的缺失 outer_wait 是阻塞未返回，不是边界谓词缺陷；我此前裁决第4点的归因应更正存档。**
- attempt4 六张 w1–w6 结果帧加 `b38c-w6-settled2.png` 共七个文件 SHA-256 逐一为 `00f5d13c...`，我亲自重算确认；参考帧解码为 2100×1079 RGB 栅格 `a16009f709c1885cd214e66f60bf99faeb0c997f3843dc0e23f29ef875987536`，与合同锚点一致。attempt4 实际只执行了一次等待。

## 最终路线合同（唯一）

**输入总数：44。** 26 载入 + 6×(`6001` + Return + 结果帧 + 空 Return) = 26+18。拒绝 43：本诊断路线的目的就是六条完整的 per-wait `outer_wait`/finally 记录；第六次不退出则第六条诊断永不存在，等于用不完整仪器数据冒充完整覆盖。BLOCKED 不成立——输入机制已由代码与帧证据完全解释，路线可修。

**每次空 Return 后、输入下一次 `6001` 前，必须同时满足两个门：**

1. **trace 门**：诊断 trace 文件中出现第 N 条完成的 `outer_wait` finally 记录（launcher 行缓冲即时落盘），其边界值与本次等待一致（depth 0 / update_depth 1 / behavior `wait` / duration 5）。
2. **帧门**：捕获并用 `view_image` 检读一张已结算帧，主指令面板可输入、输入框为空。

任一门在有界等待内不满足：截帧+存 trace，**停止本次运行并判 INVALID**，不得追加即兴输入“救”路线（若帧上出现新面板/暂停，即为路线偏离，照此停止记录）。

**RGB 栅格门禁：只对 wait 1 保留硬门。** wait 1 结果帧解码栅格必须精确等于 `a16009f...`（2100×1079，零容差；attempt4 与 attempt7 两次独立运行已证实其确定性），用作路线与 seed 身份锚。**wait 2–6 不得要求等于该参考**：修正路线下每次等待真实推进 5 分钟游戏时间，面板内容合法变化，等式门会错误拒绝正确运行。改为输入流+trace+角色结果合同判定，并加一条**反向门**：任何后续结果帧的解码栅格若与前一结果帧相等，判定为疑似输入再次被暂停吞没，运行 INVALID——旧缺陷的复发信号恰恰是“帧不变”。

**停止条件**：第六条 `outer_wait` 记录与第六张结算帧双门通过后停止采证；或任一门超时/路线偏离即 INVALID 停止。本裁决只定合同，不授权开跑；重跑开始前无须再回答仪器问题（outer_wait 缺失已由输入代码闭环解释）。
