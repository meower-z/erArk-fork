---
timestamp: 2026-07-19
---
# 数据构建链与验收

CSV/JSON 源如何被逐行解析成运行时数据，见 [CSV数据加载机制说明](../../.github/prompts/数据处理工作流/CSV数据加载机制说明.md)；本页只讲两条构建路径的差异、PO 保护、以及"改完 CSV 之后怎样才算完成"。

## 两条路径

- **全量 `buildconfig.py`**：所有 flag 硬编码为 `True`（`BUILD_TALK` 在 `buildconfig.py:54`），无条件重扫 `data/talk/`、`data/talk_common/`，并写出 `Script/Config/config_def.py`（`buildconfig.py:686`）。
- **增量 `auto_build_config.py`**（游戏启动时 `game.py` 自动跑）：若 `data/Character_Talk.json` 已存在则 `BUILD_TALK=False`（`auto_build_config.py:59`），`Talk_Common.json` 存在则 `BUILD_TALK_COMMON=False`（`auto_build_config.py:62`）——口上是最大最慢的数据，跳过它是增量的全部意义。**并且写 `config_def.py` 的两行被注释掉了**（`auto_build_config.py:569`，注释"玩家版本里不需要"）。

**什么时候增量不够、必须跑全量：**
- 改了 `data/talk/` 或 `data/talk_common/` 里的口上——增量看到旧 JSON 就整段跳过；要么删掉对应 JSON，要么跑 `buildconfig.py`。
- 给 CSV 加了新表或新列——增量不重写 `config_def.py`，而 `game_config.py:3` 把它当类型定义 import（`config_def.BarConfig` 等，`game_config.py:34` 起）。数据进了 `data.json`，但类型定义会滞后。

## 产物与消费方

`buildconfig.py` 全量写出：`config_def.py`（687）、`data.json`（689）、`Cook_Question.json`（691）、`Character.json`（682）、`ui_text.json`（695）、`Character_Talk.json`（551）、`Talk_Common.json`（621）、`Character_Event.json`（671）。运行时由 `game_config.py`（`data_path` 在 `game_config.py:8`）读入，键入以 `config_def` 的类为类型的字典。`init_data.py` 不产出数据，只预热缓存（`game_config.init()` + `map_config.init_map_data()`，`init_data.py:10,17`），CI 在构建后跑它。

## PO 文件保护

`data/po/` 是人工翻译成果。触碰它的脚本：
- `buildconfig.py` / `auto_build_config.py`：重写 `data/po/zh_CN/LC_MESSAGES/` 下 5 个抽取型 po（`erArk_csv`/`cook_question`/`talk`/`event`/`common_talk`，`buildconfig.py:698-712`），msgid 从 CSV 抽出、msgstr 恒为空。
- `buildpo.py`：只删+重生 `erArk_py.po`（`buildpo.py:9-11`，`xgettext` 扫 `.py`）。
- `buildmo.py`：读 `en_US` 的 `.po` 编译成 `.mo`（`buildmo.py:58`），**不改** `.po`。翻译正本（有 msgstr）在 `en_US`，构建链两脚本从不碰它。

**怎样证明未损坏（字节对比）**：重建后 `git diff data/po/` 只应出现你有意增删的 msgid，`en_US/` 必须零改动（一旦有改动即为串写）。**坑**：`buildconfig.py:404` 往 po 头写 `datetime.now()`，每次跑头部字节都变，字节对比要排除 `POT-Creation-Date` 行；`auto_build_config.py:398` 用硬编码日期，输出是确定的——想做干净字节对比就走增量。

## 验收标准

改 `data/csv/*.csv` **不算完成**。必须重建，并结构化读取 `data/data.json` 确认新数据在、旧数据不在，同时按上文证明 PO 字节未被顺手改写。完整标准与理由见 [ADR-0005](../adr/0005-runtime-data-verification-standard.md)。

## 命名陷阱

`buildata.py` 名字像构建脚本，但**不在构建链上**：它是 premise/settle 脚手架，靠顶部 `mode` 变量（`buildata.py:9`）在"前提↔CSV""结算↔CSV"之间转换、往 `constant_promise.py` / `handle_premise.py` 追加样板（入口 `buildata.py:252`）。跑它不会重建任何 `data/*.json`。
