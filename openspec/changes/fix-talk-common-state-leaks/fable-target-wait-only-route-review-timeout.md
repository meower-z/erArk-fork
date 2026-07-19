Script error:
Exit code: 124
Wall time: 120.1 seconds
Output:
command timed out after 120076 milliseconds

Fable 没有返回任何 verdict；本次结果只能记录为“Fable 不可用/无裁决”，不能记为通过或否决。

勘误：原样保存的 prompt 第 13 行陈述和第 17 行问题把跨日刷新顺序写反。生产源码实际先调用 `get_chara_entertainment()` 清除 `sp_flag.swim`，再增加 `desire_point`。该顺序不改变 wait147 前欲望最多为 16 的结论；prompt 本身保留原文，不把未返回的 Fable 调用当作复核。
