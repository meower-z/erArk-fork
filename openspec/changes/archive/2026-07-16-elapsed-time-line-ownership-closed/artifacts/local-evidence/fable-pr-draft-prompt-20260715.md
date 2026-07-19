/investigate-game-bug
/review-erark-pr-artifacts

请为一个即将创建到 Godofcong-1/erArk:master 的 Draft PR 生成中文标题和正文。不要编辑文件，只输出以下格式：
TITLE:
单行标题
BODY:
完整 Markdown 正文

候选 worktree：/home/ubuntu/games/erArk-pr-elapsed-time
精确 base：58587deac62149d80c82b5a3c98ad29f51cfe2b4
精确 head：b9ed4a91b117dafeb7f71ce890b33d350b359571
请亲自运行 git -C /home/ubuntu/games/erArk-pr-elapsed-time diff 58587deac...b9ed4a91b 并只按该提交 diff 写作。

已确认的玩家可见问题：多角色结算时，每个非空角色面板都会在末尾用该角色自己的局部行为时长追加一条 X分钟过去了；NPC 对玩家的兄弟路径则追加该行动将持续X分钟。一次游戏时钟推进因此被多个角色面板分别宣告，群交时尤其误导。

最终修复边界：角色结算面板不再拥有任何局部时长宣告；最外层 game_update_flow 在全部玩家和 NPC 结算结束后，只按入口前后游戏时钟的净正向分钟差输出一次 X分钟过去了。嵌套更新不单独输出；净差为零或负数不输出。Tk 仍用原输出，Web 仍写入原 web_instruct_texts 并以 instruct 类型推送，只从多条变成一条。最外层身份依赖已合入上游的更新深度修复。

可公开验证事实只有：
- python -m py_compile Script/Design/update.py Script/Design/settle_behavior.py 通过。
- git diff --check 通过。

严格禁止：
- 不得引用 local_tests、11 passed、pytest、工作树、本地路径、Fable、OpenSpec、penalty、调查过程或未提交材料。
- 不得声称最新代码已有可发布的 Tk 前后截图；截图尚未单独授权发布，而且现有最终帧不是最终 commit。
- 不得嵌入占位图片 URL、本地路径或 HTML 图片占位。
- 这是 Draft PR，可以在验证段末尾诚实写一句最新代码的 Tk 对照截图尚待补充，但不能让这句去补救前文的过度验证主张。
- 正文按玩家可见问题、原因、修复、验证的顺序；保持与上游 PR 210/211/206 的高度和简洁度，不要文件清单或非目标列表。

请确保任何关于唯一一条、净时钟差、Web 语义的描述都能由精确 diff 直接支持。
