---
timestamp: 2026-07-19
---
# Tk/Web 输入与等待契约

两种渲染模式的 UI 骨架见上游文档 [`Tk绘制模式.md`](../../.github/prompts/数据处理工作流/Tk绘制模式.md) 与 [`Web绘制模式.md`](../../.github/prompts/数据处理工作流/Web绘制模式.md)。本页只记录 grep 看不出来的东西：等待语义、标志所有权、时序坑。与 [`CONTEXT.md`](../../CONTEXT.md) 的"Tk 输入与渲染"节分工——那里是一句话原则,这里是机制细节。

## Tk 模式

`flow_handle` 的三个等待入口都在 `order_deal`(`Script/Core/flow_handle.py:378`)上轮询 order 队列:

- **`askfor_all(input_list)`**(`:456`):循环取输入,命中 `input_list` 才执行绑定命令并返回;空串 `continue`,非法值打印"选项无效"重试。选项闭集用它。
- **`askfor_wait()`**(`:530`):先把 `w_frame_up` 清 0(`:548`),再循环等到它被置 1(`:549`);`benchmark_mode` 下直接 return 不阻塞(`:545`)。"按任意键继续"用它。
- 每次进入 `order_deal` 先 `io_init.arm_input()`(`:402`)给渲染门禁上膛,见下。

### 标志所有权

三个标志各有唯一的置位/清位所有者,越权改动就是 bug 来源。

- **`w_frame_up`**(逐字/等待推进旗;`game_type.py:19` 默认 2):所有者是 `askfor_wait`。它清 0 开始等待,鼠标/回车经 `set_wframe_up()`(`key_listion_event.py:161`)置 1 推进。谁清谁负责等到它被别人置位——中途别的代码写这个标志会打乱等待配对。
- **`input_armed`**(渲染期输入门禁;`main_frame.py:394`,仅 GUI 线程读写):所有者是 `main_frame` 的队列泵。**只有** `read_queue` 处理到 `input_arm` 标记时经 `root.after_idle(_do_arm)` 上膛(`:497`);撤膛有两条路——drain 里遇到任何内容消息(`:503`)、以及每次接受输入后一次性撤膛(`send_input:413`、`mouse_left_check:80`)。是一次性门:一次输入撤一次膛,下一屏 `order_deal` 重新上膛。
- **`w_frame_skip_wait_mouse`**(显式跳过逐字等待;`game_type.py:31` 默认 0):所有者是**具体调用点**——`see_map_panel.py`、`navigation_panel.py:141`、`handle_instruct.py:842`、右键(`key_listion_event.py:93`)在需要整屏直出时置 1。**只在** `LineFeedWaitDraw`(`draw.py:172`)和 `panel.py:311` 被读取;`askfor_wait` 全局等待**不看它**,不会因它跳过。谁置 1 谁负责在自己作用域结束时清 0(如 `in_scene_panel.py:113`)。

### 时序坑:渲染期滞留点击门禁(上游 PR #236 线)

黑屏/逐字滚动期间界面还没定型,此时到来的点击(命中了还没画完的新按钮)或回车会"提前吃掉"下一个提示。门禁拦这个:

- **上膛标记恒排在一屏内容之后**。`arm_input` 把 `{"input_arm": True}` push 进 `_send_queue`(`io_init.py:224`),依赖"绘制队列单生产者(flow 线程)、push 后 flow 即阻塞等输入"这一隐性前提(`io_init.py:221` 注释),故标记必是该屏批尾。
- **不能在 drain 里直接把门置开**。标记常和整屏内容落在同一 `read_queue` 批,而玩家点击此刻滞留在 Tk 事件队列、批返回后才派发。所以 `_do_arm` 走 `after_idle`(`main_frame.py:499`):只在事件队列无待派发事件时才运行——滞留点击必先被派发(那时仍未上膛→被 `send_input:409`/`mouse_left_check:73` 丢弃),之后才真正开门。
- **迟到的内容批撤膛**。drain 每遇一条非标记内容就撤膛并 `after_cancel` 挂起的上膛回调(`:503-506`),防止"标记批之后又来内容批"时旧回调迟到误开门。
- 右键"催渲染跳过"是本职,未上膛也保留其三标志置位(`key_listion_event.py:93`),但未上膛时同样不推进等待、不注入命令(`:96`)。

### 新鲜输入原则

一次用户输入不能既推进指令、又推进其后的等待。`order_deal` 每次进入都重新 `arm_input`("重新上膛"是允许且正确的,`flow_handle.py:398` 注释);上膛门 + `w_frame_up` 清位共同保证:渲染期滞留的点击/回车被排空,只有界面定型后的新鲜输入被接受。

## Web 模式

`flow_handle_web` 是轮询模型:`askfor_all`(`flow_handle_web.py:182`)先 `update_game_state` 推送 `cache.current_draw_elements` 缓冲的元素,再 `while response is None` 每 0.1s 轮询 `get_button_response()`(`:226-302`);`askfor_wait` 轮询 `get_wait_response()`(`:337`);`askfor_str/int` 轮询 `get_input_response()`。绘制不直写,全部缓冲进 `current_draw_elements`,由 `io_web.era_print` 追加、`clear_screen` 清空。

### 已知架构缺口:输入是进程全局变量

Web 端的用户输入存成模块级全局量:`button_click_response`、`wait_response_triggered`、`input_response`(`web_server.py:103-105`)。HTTP 处理器直接写全局(`:170`,无客户端信息),getter 读后清空(`:2566`、`:2583`、`:2601`)。**没有 prompt ID、响应类型、客户端归属**——多客户端/嵌套提示下无法判断某次响应属于哪个等待点。当前唯一缓解是 `get_button_response` 的执行线程 id 守卫(`:2558`):指令执行中只许该 SocketIO 线程消费,避免与嵌套面板抢输入。完整协议化(统一 Tk/Web 的 prompt 契约)记在 [`spec.md`](../../.scratch/refactor-local-bugfixes-by-root-cause/spec.md)。

## 对 UI 开发者的约束

- 所有输出走抽象绘制类(`draw.py` / `flow_handle` 的 `print_cmd` 等),两模式各自 patch;别直接碰 Tk widget 或拼 HTML。
- 改动任一等待/输入路径都要**两模式都测**:Tk 走事件队列 + 门禁,Web 走 HTTP 轮询 + 全局量,行为差异大。
- 别在 UI 代码里裸写 `w_frame_up`/`input_armed`;它们各有唯一所有者,越权写入会破坏等待配对与门禁时序。`w_frame_skip_wait_mouse` 可在显式直出场景置位,但记得在作用域结束时清 0,且知道它对全局 `askfor_wait` 无效。
