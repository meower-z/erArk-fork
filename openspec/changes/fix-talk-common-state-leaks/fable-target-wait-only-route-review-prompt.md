/investigate-game-bug

请以怀疑视角审查下面的 current-upstream 静态结论与一次无 seed 生产样本。不要默认结论正确；请寻找任何能让 save99 的九名候选在只重复真实 6001 等待、每次结果后输入空 Return、发现面板选择 4 的路径中最终命中 target86 的遗漏分支。需要给出 verdict：有限 N_min、不存在有限 N、或仍有精确未决分支。事实必须服从源码；你可以检查仓库。

基线：commit 72e28051e，save99，2019-12-29 11:52，场景为人力发电室，候选 CID 7,10,56,130,241,308,385,4080,4122；desire_point 均为0，talent222=0，body_manage23=body_manage25=0。输入流是真实 handle_wait_5_min_in_h，每次玩家结算 WaitDraw 后空 Return；CID7/10 首次发现面板真实选4。没有 seed/GUI，也没有生产文件修改。

源码时序：6001 先把全局时间加5分钟，再运行 init_character_behavior。日结算只在整个 NPC 循环后执行。纯等待下 desire_point 唯一正写者是日结算：每人加 randint(ability33, 2*ability33)。target86 位于 type11，前提 normal_1267、desire_point_ge_100、sexual_ignorance_0、not_ask_not_masturbation；type11 使用 get_first_only。

饭点：eat_time 读取 NPC behavior.start_time.hour，不读全局时间。首次全局12:02时，NPC start 仍为11:45到11:59，所以 target41 当时不成立。SM75 会设 eat_food=1，使 normal1 失败；下一 pass 先走 type12 的 target42/43，早于 target86。助理陈的 target521 会设 help_make_food=1，随后 type12 target91 可在不经过 target86 时执行，但实际样本中她此前已离场并 is_h=False。

一次获准的无 seed 真实样本：wait1 七名命中 target9/SM2；CID7/10先各处理一次发现4。wait2 起 CID7,56,130,308,385,4080 由当前工作或娱乐自动路线移动离开；CID10由 target61/62 休息路线离开；这些角色离开玩家场景后 handle_npc_ai_in_h 将 is_h=False。CID241与4122在 wait2 命中 target461/SM82，随后 target462/SM612；由于 MOVE_TO_TRAINING_LOCKER_ROOM 找不到以中文字符串训练开头的 Locker_Room，SM612不写行为，留下 share_blankly duration0、start=11:46、同场且is_h=True。样本跑到wait15，这两人持续相同状态。样本只能说明这一实际运行，不能代表随机规律。

CID241/4122 的静态闭环：两者 ability33=8，work_type=193，body_manage 31=1、36=1、37=1，因此 ask_one_exercises 为真；两者均无隶属系陷落，且宿舍不在人力发电室。第一次跨午夜在 wait146，NPC target search 仍先发生，desire仍0；随后日结算各加8..16，并调用 get_chara_entertainment，第一句将 sp_flag.swim=0。wait147 时 target86因 desire最多16必败。全局日期已是工作日，角色本地start仍11:46，work_time成立；target802 前提 normal_all、work_is_sex_trainee、ask_one_exercises、work_time、self_not_fall_obey、not_in_dor 全部成立，SM502移动回宿舍。下一 NPC pass 因不在玩家场景而清 is_h。之后不再是该群交路线。

算术反事实：若外力保持路线不退出，ability8 最早第7次日增量后、wait1875才可能达到100；概率为 49548/9^7 约1.0359256%。但真实路线在wait147确定退出，所以该条件事件的生存概率看起来为0。若强行令 target86 到达，SM91内部逆推率为CID241 20%、CID4122 50%；但真实路径从不到达。

请核查：1）12:02/SM75链是否遗漏回到target86的同场路径；2）日结算是否确实先加欲望再清游泳，及这两者顺序对wait147是否有别；3）target802/SM502是否存在不离场或不清H的反例；4）是否还有 writer 能在wait147前把欲望直接提到100；5）最终结论和最简洁、可信的人类表述。
