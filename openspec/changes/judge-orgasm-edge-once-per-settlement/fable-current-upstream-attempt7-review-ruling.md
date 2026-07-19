`REVISE` — 拒绝按所述前提批准 attempt8：它要修的"过早判帧"问题不存在。我对主证据独立复核后，事实 3 和事实 4 的推论均被推翻，唯一需要改的是一项判据——把结果帧身份从 **PNG 容器字节哈希** 改为 **解码像素栅格的精确哈希**。其余全部合同（38 物理输入、wrapper、RNG、六次路线、candidate 禁令）逐字不变。

**独立复核出的决定性事实（推翻提交的事实 3/4）：**

1. `frame-28-post-wait-1.png` 与 attempt4 的 `b28-w1-result.png`（即字节哈希 `00f5d13c...` 的那一帧）**逐像素完全相同**。我用 ImageMagick `compare -metric AE` 和独立的 numpy 逐元素比较各验证一次：AE=0、RMSE=0、`(a==b).all()==True`，尺寸同为 2100×1079。attempt7 目录里已有的 `frame-28-pixel-ae.txt`（0）与 `frame-28-pixel-rmse.txt`（0）记录的正是同一结论，却被 INVALID.md 以"pixel comparison does not rescue"忽略了。
2. 因此 frame-28 **不是**黑屏中间重绘帧——它就是已结算的主指令面板，底部可见 `凯尔希阴道小绝顶` 结果行，与 attempt4 的正常结果帧无一像素差异。"几乎全黑"是对暗色主题 UI 的误读（全帧平均亮度 23.8/255，attempt4 的合格结果帧亮度完全相同）。
3. 字节哈希不等的唯一原因是 PNG **编码**差异：833,672 字节 vs 830,208 字节，像素相同。门禁在测量编码器，不是测量游戏画面。
4. trace 中缺失 `outer_wait` 记录**不能**推出"截帧时等待尚未返回"：画面已是结算完成后等待下一输入的状态。launcher 的记录写在 `init_character_behavior` 的 `finally` 里且行缓冲即时落盘（`diagnostic_tk_launcher.py:164-173`、`:329`），等待若已返回、`boundary_wait` 为真则记录必然在文件里。记录缺失说明 `begin_outer_entry` 的边界谓词（`behavior_id != "wait" or duration != 5`，`:135`）或深度条件在真实运行里**没有认出这次等待**——这是 attempt7 真正暴露的仪器缺陷，也是 attempt8 必须先解决的问题，否则即使门禁通过，诊断 A 依然零数据。

**为什么不是 PASS：** attempt8 的两个新判据都建立在错误诊断上。判据 (a)"等 `outer_wait` 记录出现再判帧"会把上述谓词缺陷烧进控制器——本次运行里画面早已结算而记录永远不来，attempt8 只会在等待上限处作废，且归因仍然错误。判据 (b) 已经被满足过了。而保留的字节哈希门禁会再次拒绝像素相同的帧，attempt8 将与 attempt7 以完全相同的方式失败。

**为什么不是 BLOCKED：** 中间重绘与结果帧完全可区分——本次就区分出来了：结果帧与已归档参考帧像素相等。

**唯一修改的判据：** 结果帧门禁改为——捕获帧解码为 8-bit RGB 原始栅格后，其 SHA-256 必须等于从 attempt4 归档参考帧 `b28-w1-result.png` 解码得到的
`a16009f709c1885cd214e66f60bf99faeb0c997f3843dc0e23f29ef875987536`
（命令形式 `convert frame.png -depth 8 rgb:- | sha256sum`；尺寸必须同为 2100×1079）。这不是放宽：零像素容差、单一参考、精确相等，只是把身份锚在画面内容而非 PNG 编码器输出上。我已验证 attempt4 参考帧与 attempt7 frame-28 都解码到该栅格哈希。捕获时机维持原合同（每次 Return 后捕获判帧），不引入 trace 依赖的等待逻辑。

**附带的事实性指令（非判据修改）：** 在重跑任何门禁路线之前，先在只读诊断里解释为什么 wait 1 完整结算后 `outer_wait` 记录缺失——最可疑处是 `:135` 的谓词在外层进入时读到的 `behavior_id`/`duration` 值与假设不符，其次是 `:128` 的 `update_depth == 1` 条件。带着零数据的仪器重跑 38 输入没有意义。attempt7 的 INVALID 结论维持（按当时合同停止是对的），但其"过早判帧/黑屏中间帧"的归因文本应予更正存档。
