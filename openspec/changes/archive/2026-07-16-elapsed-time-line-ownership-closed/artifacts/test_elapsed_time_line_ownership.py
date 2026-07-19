# -*- coding: UTF-8 -*-
"""一次玩家点击的实际经过时间显示所有权回归。"""

import datetime
from pathlib import Path

import pytest

from Script.Config import game_config, normal_config

normal_config.init_normal_config()

from Script.Core import cache_control, game_type, io_init

cache_control.cache = game_type.Cache()
runtime_data = Path("/home/ubuntu/games/erArk/data")
game_config.data_path = str(runtime_data / "data.json")
game_config.character_path = str(runtime_data / "Character.json")
game_config.character_talk_path = str(runtime_data / "Character_Talk.json")
game_config.character_event_path = str(runtime_data / "Character_Event.json")
game_config.talk_common_path = str(runtime_data / "Talk_Common.json")
game_config.ui_text_path = str(runtime_data / "ui_text.json")
game_config.cook_question_path = str(runtime_data / "Cook_Question.json")
game_config.init()

import Script.Settle
from Script.Design import settle_behavior, update


def _panel_text(panel) -> str:
    """参数：结算面板；返回：面板纯文本；用途：读取真实结算面板形成的绘制内容。"""
    return "".join(draw_item.text for draw_row in panel.draw_list for draw_item in draw_row)


def _make_character(character_id: int, start_time: datetime.datetime) -> game_type.Character:
    """参数：角色编号和行动开始时间；返回：最小角色；用途：建立真实结算函数所需角色状态。"""
    character = game_type.Character()
    character.cid = character_id
    character.name = "博士" if character_id == 0 else f"NPC{character_id}"
    character.position = ["0", "0"]
    character.target_character_id = character_id
    character.behavior.start_time = start_time
    return character


def _install_cache(monkeypatch, *, web_mode: bool = False) -> game_type.Cache:
    """参数：pytest 补丁器和 Web 标志；返回：隔离缓存；用途：让真实入口共享同一测试缓存。"""
    cache = game_type.Cache()
    cache.game_time = datetime.datetime(2026, 7, 14, 12, 0)
    cache.pre_game_time = cache.game_time
    cache.web_mode = web_mode
    cache.web_instruct_texts = []
    cache.all_system_setting.draw_setting[6] = 1
    cache.all_system_setting.draw_setting[7] = 1
    monkeypatch.setattr(cache_control, "cache", cache)
    monkeypatch.setattr(settle_behavior, "cache", cache)
    monkeypatch.setattr(update.cache_control, "cache", cache)
    return cache


def _status_change(*_args, **_kwargs) -> game_type.CharacterStatusChange:
    """参数：真实结算入口参数；返回：含体力变化的结算；用途：稳定生成非空角色面板。"""
    change = game_type.CharacterStatusChange()
    change.hit_point = -1
    return change


def test_character_panels_do_not_repeat_elapsed_time(monkeypatch):
    """参数：pytest 补丁器；返回：无；用途：证明多个真实角色面板不再各自宣告同一段时间。"""
    cache = _install_cache(monkeypatch)
    start_time = cache.game_time
    cache.character_data = {
        0: _make_character(0, start_time),
        1: _make_character(1, start_time),
    }
    monkeypatch.setattr(settle_behavior, "handle_instruct_data", _status_change)
    monkeypatch.setattr(settle_behavior.handle_premise, "handle_group_sex_mode_on", lambda _character_id: False)

    panel_texts = [
        _panel_text(settle_behavior.handle_settle_behavior(character_id, start_time + datetime.timedelta(minutes=5)))
        for character_id in (0, 1)
    ]

    assert sum(text.count("5分钟过去了") for text in panel_texts) == 0
    assert all("体力" in text for text in panel_texts)


def test_exchange_panel_does_not_report_local_duration(monkeypatch):
    """参数：pytest 补丁器；返回：无；用途：保证 NPC 对玩家行动的角色面板不再报告局部时长。"""
    cache = _install_cache(monkeypatch)
    start_time = cache.game_time
    player = _make_character(0, start_time)
    npc = _make_character(1, start_time)
    npc.target_character_id = 0
    cache.character_data = {0: player, 1: npc}

    def target_status_change(*_args, **_kwargs):
        """参数：真实结算入口参数；返回：对玩家的体力变化；用途：触发 NPC 对玩家的交换输出。"""
        change = game_type.CharacterStatusChange()
        target_change = game_type.TargetChange()
        target_change.hit_point = -1
        change.target_change[0] = target_change
        return change

    monkeypatch.setattr(settle_behavior, "handle_instruct_data", target_status_change)

    text = _panel_text(settle_behavior.handle_settle_behavior(1, start_time + datetime.timedelta(minutes=5)))

    assert "该行动将持续" not in text
    assert "5分钟过去了" not in text


def _run_update(monkeypatch, *, start_time=None, settle=None, web_mode=False):
    """参数：补丁器、开始时间、结算替身和 Web 标志；返回：缓存、Tk 输出和实时输出；用途：通过真实更新入口观测唯一时间提示。"""
    cache = _install_cache(monkeypatch, web_mode=web_mode)
    cache.game_time = start_time or cache.game_time
    cache.pre_game_time = cache.game_time
    tk_output = []
    realtime_output = []

    def add_time(minute=0, **_kwargs):
        """参数：分钟及兼容参数；返回：无；用途：保留真实更新入口的可控游戏时钟变化。"""
        cache.game_time += datetime.timedelta(minutes=minute)

    monkeypatch.setattr(update.game_time, "sub_time_now", add_time)
    monkeypatch.setattr(update.character_behavior, "init_character_behavior", settle or (lambda: None))
    monkeypatch.setattr(update.py_cmd, "focus_cmd", lambda: None)
    monkeypatch.setattr(update, "io_init", io_init, raising=False)
    monkeypatch.setattr(update.io_init, "era_print", lambda text, *_args, **_kwargs: tk_output.append(text))
    monkeypatch.setattr(update.web_server, "emit_realtime_text", lambda text, text_type="other": realtime_output.append((text, text_type)))
    return cache, tk_output, realtime_output


def test_outer_update_displays_time_without_character_panels(monkeypatch):
    """参数：pytest 补丁器；返回：无；用途：验证无角色面板时最外层入口仍显示实际经过时间。"""
    _cache, tk_output, _realtime_output = _run_update(monkeypatch)

    update.game_update_flow(5)

    assert "".join(tk_output).count("5分钟过去了") == 1


def test_nested_update_is_folded_into_outer_elapsed_time(monkeypatch):
    """参数：pytest 补丁器；返回：无；用途：验证嵌套更新不单独显示且外层报告总净时间。"""
    nested = False

    def settle_with_nested_update():
        """参数：无；返回：无；用途：在外层结算内触发一次真实嵌套更新入口。"""
        nonlocal nested
        if not nested:
            nested = True
            update.game_update_flow(2)

    _cache, tk_output, _realtime_output = _run_update(monkeypatch, settle=settle_with_nested_update)

    update.game_update_flow(5)

    text = "".join(tk_output)
    assert text.count("分钟过去了") == 1
    assert "7分钟过去了" in text


@pytest.mark.parametrize(
    ("rollback_minutes", "expected_text"),
    [
        (5, ""),
        (7, ""),
        (2, "3分钟过去了"),
    ],
)
def test_elapsed_time_uses_positive_net_clock_change(monkeypatch, rollback_minutes, expected_text):
    """参数：补丁器、回退分钟和预期文本；返回：无；用途：验证完整回退不显示、部分回退显示净时间。"""
    cache = None

    def settle_with_rollback():
        """参数：无；返回：无；用途：模拟时停或其他结算对游戏时钟的回退。"""
        cache.game_time -= datetime.timedelta(minutes=rollback_minutes)

    cache, tk_output, _realtime_output = _run_update(monkeypatch, settle=settle_with_rollback)

    update.game_update_flow(5)

    text = "".join(tk_output)
    assert ("分钟过去了" in text) is bool(expected_text)
    if expected_text:
        assert expected_text in text


def test_nested_exception_does_not_split_elapsed_time(monkeypatch):
    """参数：pytest 补丁器；返回：无；用途：验证内层异常被外层捕获后仍由外层统一显示净时间。"""
    cache = None

    def settle_with_nested_exception():
        """参数：无；返回：无；用途：在内层抛错并让外层继续完成。"""
        if cache.game_update_flow_running == 1:
            try:
                update.game_update_flow(2)
            except RuntimeError:
                pass
        else:
            raise RuntimeError("nested settlement failed")

    cache, tk_output, _realtime_output = _run_update(monkeypatch, settle=settle_with_nested_exception)

    update.game_update_flow(5)

    text = "".join(tk_output)
    assert cache.game_update_flow_running == 0
    assert text.count("分钟过去了") == 1
    assert "7分钟过去了" in text


def test_elapsed_time_handles_midnight(monkeypatch):
    """参数：pytest 补丁器；返回：无；用途：验证跨日仍按 datetime 净差显示分钟数。"""
    start_time = datetime.datetime(2026, 7, 14, 23, 58)
    _cache, tk_output, _realtime_output = _run_update(monkeypatch, start_time=start_time)

    update.game_update_flow(5)

    assert "5分钟过去了" in "".join(tk_output)


def test_next_update_is_clean_after_exception(monkeypatch):
    """参数：pytest 补丁器；返回：无；用途：验证异常点击不会污染下一次成功点击的时间提示。"""
    should_raise = True

    def settle_once_with_exception():
        """参数：无；返回：无；用途：仅让第一次结算失败。"""
        nonlocal should_raise
        if should_raise:
            should_raise = False
            raise RuntimeError("settlement failed")

    cache, tk_output, _realtime_output = _run_update(monkeypatch, settle=settle_once_with_exception)

    with pytest.raises(RuntimeError, match="settlement failed"):
        update.game_update_flow(5)
    update.game_update_flow(3)

    assert cache.game_update_flow_running == 0
    assert "".join(tk_output).count("3分钟过去了") == 1


def test_web_history_records_one_elapsed_time(monkeypatch):
    """参数：pytest 补丁器；返回：无；用途：验证 Web 文本回溯与实时推送只记录一次。"""
    cache, tk_output, realtime_output = _run_update(monkeypatch, web_mode=True)

    update.game_update_flow(5)

    assert tk_output == []
    assert cache.web_instruct_texts == ["\n\n 5分钟过去了\n"]
    assert realtime_output == [("\n\n 5分钟过去了\n", "instruct")]
