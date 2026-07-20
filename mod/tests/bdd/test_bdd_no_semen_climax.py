#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BDD 场景（近真实层）：共享玩家高潮入口的无精液高潮分支

对应规格 .scratch/correct-semen-climax-flow/spec.md 与 issue 02：
当玩家射精槽达到高潮阈值、但基础精液与临时精液合计不超过 2 ml 时，
共享玩家高潮判断入口 second_behavior.orgasm_judge(0, ...) 应作为“无精液高潮”结算——
登记专用二段行为 p_no_semen_climax、不打开射精对象/部位选择面板，并清空射精槽与忍住不射次数；
合计精液超过 2 ml 时仍进入既有普通射精选择路径。

测试缝：共享玩家高潮判断入口 second_behavior.orgasm_judge。
运行方式（仓库根目录）：.venv/bin/pytest mod/tests/bdd/test_bdd_no_semen_climax.py -v
"""

from collections import defaultdict
from types import SimpleNamespace

import pytest

from mod.tests.bdd.near_real_boot import boot_game_once


@pytest.fixture(scope="session")
def booted():
    """返回值类型：BootContext；用途：会话级近真实引导（真实配置+真实mod加载）。"""
    return boot_game_once(enable_debug=True)


def _make_player(semen_point: int, tem_extra_semen_point: int, endure_not_shot_count: int = 0, eja_point: int = 100):
    """
    参数：semen_point(int)基础精液、tem_extra_semen_point(int)临时精液、endure_not_shot_count(int)忍住不射次数、eja_point(int)射精槽；
    返回：SimpleNamespace 玩家角色桩；
    用途：构造玩家角色，供共享高潮入口驱动。
    """
    return SimpleNamespace(
        semen_point=semen_point,
        tem_extra_semen_point=tem_extra_semen_point,
        eja_point=eja_point,
        eja_point_max=100,
        second_behavior={},
        must_settle_second_behavior_id_list=[],
        must_show_second_behavior_id_list=[],
        h_state=SimpleNamespace(endure_not_shot_count=endure_not_shot_count),
    )


class _PanelSpy:
    """用途：射精对象/部位选择面板的探针，记录是否被实例化与绘制。"""

    draw_count = 0

    def __init__(self, width):
        """参数：width(int)绘制宽度；用途：记录面板被实例化。"""
        type(self).draw_count += 1

    def draw(self):
        """用途：占位绘制，避免真实面板进入交互循环。"""
        return None


def _patch_common(booted, monkeypatch, panel_spy_cls):
    """
    参数：booted(BootContext)、monkeypatch、panel_spy_cls(面板探针类)；
    返回：None；
    用途：将玩家高潮入口下游的面板与绘制替换为无副作用桩，其余仍走真实逻辑。
    """
    from Script.Design import second_behavior

    panel_spy_cls.draw_count = 0
    # 射精对象/部位选择面板替换为探针，既能断言是否被绘制，又避免进入交互循环
    monkeypatch.setattr(second_behavior.ejaculation_panel, "Ejaculation_Panel", panel_spy_cls)
    # 忍耐面板默认返回未忍耐，保证正量精液走普通射精而非提前 return
    monkeypatch.setattr(second_behavior.ejaculation_panel, "show_endure_ejaculation_panel", lambda: False)
    # 分隔线绘制在无 GUI 下无实际输出，替换为无副作用桩
    monkeypatch.setattr(second_behavior.draw, "LineDraw", lambda *a, **k: SimpleNamespace(draw=lambda: None))


def test_no_semen_climax_registers_dedicated_behavior_and_skips_panel(booted, monkeypatch):
    """
    场景：玩家在高潮阈值、合计精液不超过 2 ml。
    验证点：登记 p_no_semen_climax、不登记 p_orgasm_small、不绘制射精选择面板、
    射精槽与忍住不射次数清零。
    """
    from Script.Design import second_behavior

    player = _make_player(semen_point=1, tem_extra_semen_point=1, endure_not_shot_count=3)
    monkeypatch.setitem(booted.cache.character_data, 0, player)
    _patch_common(booted, monkeypatch, _PanelSpy)

    change_data = SimpleNamespace(status_data=defaultdict(int), target_change={})
    second_behavior.orgasm_judge(0, change_data)

    assert player.second_behavior.get("p_no_semen_climax") == 1
    assert "p_orgasm_small" not in player.second_behavior
    assert "p_orgasm_normal" not in player.second_behavior
    assert "p_orgasm_strong" not in player.second_behavior
    assert _PanelSpy.draw_count == 0
    assert player.eja_point == 0
    assert player.h_state.endure_not_shot_count == 0


def test_skip_endure_releases_no_semen_climax_below_threshold(booted, monkeypatch):
    """
    场景：停止忍耐时射精槽尚未达阈值，且合计精液不超过 2 ml。
    验证点：skip_undure 强制登记专用行为、不打开面板，并清空射精槽与忍耐次数。
    """
    from Script.Design import second_behavior

    player = _make_player(semen_point=0, tem_extra_semen_point=2, endure_not_shot_count=2, eja_point=40)
    monkeypatch.setitem(booted.cache.character_data, 0, player)
    _patch_common(booted, monkeypatch, _PanelSpy)

    change_data = SimpleNamespace(status_data=defaultdict(int), target_change={})
    second_behavior.orgasm_judge(0, change_data, skip_undure=True)

    assert player.second_behavior.get("p_no_semen_climax") == 1
    assert "p_orgasm_small" not in player.second_behavior
    assert _PanelSpy.draw_count == 0
    assert player.eja_point == 0
    assert player.h_state.endure_not_shot_count == 0


def test_positive_semen_uses_ordinary_ejaculation_path(booted, monkeypatch):
    """
    场景：玩家在高潮阈值、合计精液超过 2 ml（对照组）。
    验证点：仍登记普通射精 p_orgasm_small、不登记 p_no_semen_climax、绘制射精选择面板。
    """
    from Script.Design import second_behavior

    player = _make_player(semen_point=50, tem_extra_semen_point=0, endure_not_shot_count=0)
    monkeypatch.setitem(booted.cache.character_data, 0, player)
    _patch_common(booted, monkeypatch, _PanelSpy)

    change_data = SimpleNamespace(status_data=defaultdict(int), target_change={})
    second_behavior.orgasm_judge(0, change_data)

    assert player.second_behavior.get("p_orgasm_small") == 1
    assert "p_no_semen_climax" not in player.second_behavior
    assert _PanelSpy.draw_count == 1
    assert player.eja_point == 0


def test_no_semen_climax_executes_climax_effects_without_ejaculation_results(booted, monkeypatch):
    """
    场景：实际执行 p_no_semen_climax 的完整二段效果集合。
    验证点：体力/气力减少、双方插入位置清理、隐奸暴露入口被调用，射精次数/经验、润滑、射精位置与污浊不增加。
    """
    from Script.Core import game_type
    from Script.Design import second_behavior
    from Script.System.Sex_System import hidden_sex_panel

    player = game_type.Character()
    target = game_type.Character()
    player.target_character_id = 1
    target.target_character_id = 0
    player.hit_point = player.hit_point_max = 100
    player.mana_point = player.mana_point_max = 100
    player.h_state.insert_position = 6
    target.h_state.insert_position = 6
    player.h_state.orgasm_count[3] = [4, 5]
    player.h_state.shoot_position_body = 2
    player.h_state.shoot_position_cloth = 7
    target.status_data[8] = 123
    target.dirty.body_semen[2] = ["口", 3, 1, 3]
    player.experience[21] = 9
    player.sp_flag.hidden_sex_mode = 1
    player.second_behavior["p_no_semen_climax"] = 1
    monkeypatch.setitem(booted.cache.character_data, 0, player)
    monkeypatch.setitem(booted.cache.character_data, 1, target)
    monkeypatch.setattr(second_behavior.talk, "handle_second_talk", lambda *a, **k: None)
    hidden_calls = []
    monkeypatch.setattr(hidden_sex_panel, "handle_hidden_sex_flow", lambda **kwargs: hidden_calls.append(kwargs))

    change_data = game_type.CharacterStatusChange()
    second_behavior.second_behavior_effect(0, change_data, ["p_no_semen_climax"])

    assert (player.hit_point, player.mana_point) == (90, 40)
    assert (change_data.hit_point, change_data.mana_point) == (-10, -60)
    assert player.h_state.insert_position == target.h_state.insert_position == -1
    assert hidden_calls == [{"character_id": 0, "add_flag": True, "now_duration": 5, "now_intensity": 2}]
    assert player.experience[21] == 9
    assert player.h_state.orgasm_count[3] == [4, 5]
    assert target.status_data[8] == 123
    assert (player.h_state.shoot_position_body, player.h_state.shoot_position_cloth) == (2, 7)
    assert target.dirty.body_semen == {2: ["口", 3, 1, 3]}
    assert player.second_behavior["p_no_semen_climax"] == 0


def test_no_semen_climax_system_talk_states_climax_without_ejaculation(booted):
    """
    场景：专用系统二段口上的加载与行为映射。
    验证点：玩家可见文本明确写出高潮和未排精，并且不复用普通 orgasm 射精行为的口上映射。
    """
    from Script.Config import game_config

    talk_ids = game_config.config_talk_data_by_chara_adv["p_no_semen_climax"][0][1]
    texts = [game_config.config_talk[talk_id].context for talk_id in talk_ids]
    ordinary_ids = set(game_config.config_talk_data_by_chara_adv["p_orgasm_small"][0][1])

    assert talk_ids
    assert set(talk_ids).isdisjoint(ordinary_ids)
    assert any("高潮" in text and "精液" in text and any(word in text for word in ("射不出", "没有", "未排出")) for text in texts)


def test_no_semen_climax_behavior_effect_set_excludes_ejaculation_effects(booted):
    """
    场景：无精液高潮专用二段行为的效果集合（数据契约）。
    验证点：只保留效果 231/232/411/501/997（体力、气力、隐奸暴露、插入位置清理、必须结算），
    不含射精经验 221、目标润滑 225、人力发电 415 或目标精液经验综合数值效果。
    """
    from Script.Config import game_config

    effect_list = game_config.config_behavior_effect_data.get("p_no_semen_climax")
    assert effect_list is not None, "p_no_semen_climax 未在行为结算器数据中声明，需先构建数据"
    assert set(effect_list) == {231, 232, 411, 501, 997}
    # 显式否定：不得混入射精专属效果
    for banned in (221, 225, 415):
        assert banned not in effect_list
    assert not any(isinstance(e, str) and "CVE" in e for e in effect_list)
