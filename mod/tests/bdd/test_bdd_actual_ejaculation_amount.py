#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BDD 场景（近真实层）：临时精液参与时的实际射精量完整下游契约

对应 .scratch/correct-semen-climax-flow/issues/01-fix-actual-ejaculation-amount.md。
测试通过公开射精流程 ejaculation_panel.ejaculation_flow()，在未 mock 的真实 Script
模块、真实角色数据结构与真实配置数据上固定随机补正和加成前提，覆盖四个精液来源分区：
无临时精液、临时精液小于实际量、临时精液恰好等于实际量、临时精液大于实际量。

每个分区断言：显示量、common_ejaculation() 返回量、污浊写入量、目标口腔历史增量、
H 中射精量增量和全局射精量增量一致，且基础/临时精液按“临时优先”规则正确扣除。

运行方式：.venv/bin/pytest mod/tests/bdd/test_bdd_actual_ejaculation_amount.py -v
"""

import re

import pytest

from mod.tests.bdd.near_real_boot import boot_game_once


@pytest.fixture(scope="session")
def booted():
    """
    完成会话级近真实游戏引导

    参数：无。
    返回值类型：BootContext。
    功能描述：返回已载入真实配置、Script 模块与启用 mod 的测试上下文。
    """
    return boot_game_once(enable_debug=True)


def _make_characters(booted, base_semen_point: int, tem_extra_semen_point: int):
    """
    构造完整射精流程使用的玩家与目标角色

    参数:
    booted (BootContext): 近真实引导上下文。
    base_semen_point (int): 玩家基础精液值。
    tem_extra_semen_point (int): 玩家临时额外精液值。

    返回值类型：tuple[Character, Character]。
    功能描述：使用真实 Character 数据结构创建最小可用场景，射精部位固定为目标口腔。
    """
    from Script.Design import attr_calculation

    player = booted.game_type.Character()
    player.name = "玩家"
    player.target_character_id = 0
    player.semen_point = base_semen_point
    player.tem_extra_semen_point = tem_extra_semen_point
    player.second_behavior = {"p_orgasm_small": 1, "p_orgasm_normal": 0, "p_orgasm_strong": 0}
    player.action_info.day_first_shoot_semen = False
    player.dirty = attr_calculation.get_zero_dirty()
    player.dirty.penis_dirty_dict["semen"] = False
    player.h_state.orgasm_level[3] = 0
    player.h_state.body_item[13] = ["避孕套", False, None]

    target = booted.game_type.Character()
    target.cid = 1
    target.name = "目标"
    target.dirty = attr_calculation.get_zero_dirty()

    return player, target


def _run_ejaculation_flow(booted, monkeypatch, base_semen_point: int, tem_extra_semen_point: int):
    """
    在固定无加成条件下驱动一次完整射精流程并采集结果

    参数:
    booted (BootContext): 近真实引导上下文。
    monkeypatch (pytest.MonkeyPatch): pytest monkeypatch 夹具。
    base_semen_point (int): 玩家基础精液值。
    tem_extra_semen_point (int): 玩家临时额外精液值。

    返回值类型：dict。
    功能描述：调用 ejaculation_flow()，采集通用射精返回量、污浊写入量、目标口腔历史、
    H 中射精量、全局射精量以及基础/临时精液的前后值。
    """
    from Script.Config import game_config
    from Script.Design import pregnancy
    from Script.UI.Panel import ejaculation_panel

    cache = booted.cache
    player, target = _make_characters(booted, base_semen_point, tem_extra_semen_point)
    monkeypatch.setitem(cache.character_data, 0, player)
    monkeypatch.setitem(cache.character_data, 1, target)

    # 固定随机补正与全部加成前提，使实际射精量恒等于小量射精配置值。
    monkeypatch.setattr(ejaculation_panel.random, "uniform", lambda _a, _b: 1.0)
    monkeypatch.setattr(ejaculation_panel.handle_premise, "handle_pl_semen_le_2", lambda _cid: False)
    monkeypatch.setattr(ejaculation_panel.handle_premise, "handle_self_semen_energy_agent", lambda _cid: False)
    monkeypatch.setattr(ejaculation_panel.handle_premise, "handle_aromatherapy_flag_7", lambda _cid: False)
    monkeypatch.setattr(ejaculation_panel.handle_premise, "handle_pl_semen_tmp_ge_max", lambda _cid: False)
    monkeypatch.setattr(ejaculation_panel.handle_premise, "handle_self_semen_thick_1", lambda _cid: False)
    monkeypatch.setattr(ejaculation_panel.handle_premise, "handle_group_sex_mode_on", lambda _cid: False)
    monkeypatch.setattr(ejaculation_panel.handle_premise, "handle_hidden_sex_mode_ge_1", lambda _cid: False)
    monkeypatch.setattr(ejaculation_panel.handle_premise, "handle_exhibitionism_sex_mode_ge_1", lambda _cid: False)
    monkeypatch.setattr(ejaculation_panel.handle_premise, "handle_t_unconscious_flag_1", lambda _cid: False)
    monkeypatch.setattr(ejaculation_panel.handle_premise, "handle_unconscious_flag_ge_1", lambda _cid: False)
    monkeypatch.setattr(pregnancy, "get_fertilization_rate", lambda _cid: None)
    monkeypatch.setattr(ejaculation_panel.achievement_panel, "get_achievement_judge_by_value", lambda _achievement_id, _value: False)
    monkeypatch.setattr(ejaculation_panel.achievement_panel, "achievement_flow", lambda _achievement_type: None)

    trace = {"dirty_writer_amount": None}
    original_common_ejaculation = ejaculation_panel.common_ejaculation
    original_update_semen_dirty = ejaculation_panel.update_semen_dirty

    def trace_common_ejaculation():
        """参数：无；返回值类型：tuple[str, int]；记录通用射精返回值后原样返回。"""
        result = original_common_ejaculation()
        trace["common_return"] = result
        return result

    def trace_update_semen_dirty(
        character_id: int,
        part_cid: int,
        part_type: int,
        semen_count: int,
        update_shoot_position_flag: bool = True,
    ):
        """记录污浊写入参数并调用真实写入函数；参数与返回值同 update_semen_dirty()。"""
        trace["dirty_writer_amount"] = semen_count
        return original_update_semen_dirty(
            character_id,
            part_cid,
            part_type,
            semen_count,
            update_shoot_position_flag,
        )

    monkeypatch.setattr(ejaculation_panel, "common_ejaculation", trace_common_ejaculation)
    monkeypatch.setattr(ejaculation_panel, "update_semen_dirty", trace_update_semen_dirty)

    mouth_before = target.dirty.body_semen[2][3]
    shoot_before = player.h_state.shoot_semen_amount
    total_before = cache.rhodes_island.total_semen_count

    ejaculation_panel.ejaculation_flow(part_cid=2, part_type=0, target_character_id=1, draw_flag=False)

    semen_text, returned = trace["common_return"]
    return {
        "actual_amount": int(game_config.config_semen_shoot_amount[0].base_semen_amount),
        "returned": returned,
        "displayed": int(re.search(r"(\d+)ml", semen_text).group(1)),
        "dirty_writer_amount": trace["dirty_writer_amount"],
        "mouth_delta": target.dirty.body_semen[2][3] - mouth_before,
        "shoot_delta": player.h_state.shoot_semen_amount - shoot_before,
        "total_delta": cache.rhodes_island.total_semen_count - total_before,
        "base_before": base_semen_point,
        "base_after": player.semen_point,
        "tem_before": tem_extra_semen_point,
        "tem_after": player.tem_extra_semen_point,
    }


def _assert_full_downstream(result: dict):
    """
    断言完整射精下游与资源扣除契约

    参数:
    result (dict): _run_ejaculation_flow() 返回的采集结果。

    返回值类型：None。
    功能描述：验证实际射精量在显示、返回、污浊、H 状态、全局统计间保持一致，并验证临时精液优先扣除。
    """
    actual_amount = result["actual_amount"]
    expected_tem_deduct = min(result["tem_before"], actual_amount)
    expected_base_deduct = actual_amount - expected_tem_deduct

    assert result["displayed"] == actual_amount
    assert result["returned"] == result["dirty_writer_amount"] == result["mouth_delta"] == result["shoot_delta"] == result["total_delta"] == actual_amount
    assert result["tem_before"] - result["tem_after"] == expected_tem_deduct
    assert result["base_before"] - result["base_after"] == expected_base_deduct


def test_no_temporary_semen_reaches_full_downstream(booted, monkeypatch):
    """分区一：无临时精液时，完整下游均使用实际量，全部资源由基础精液承担。"""
    result = _run_ejaculation_flow(booted, monkeypatch, base_semen_point=100, tem_extra_semen_point=0)
    _assert_full_downstream(result)


def test_temporary_below_actual_reaches_full_downstream(booted, monkeypatch):
    """分区二：临时精液小于实际量时，下游使用完整实际量，资源先扣临时再扣基础。"""
    result = _run_ejaculation_flow(booted, monkeypatch, base_semen_point=100, tem_extra_semen_point=4)
    assert 0 < result["tem_before"] < result["actual_amount"]
    _assert_full_downstream(result)


def test_temporary_equals_actual_reaches_full_downstream(booted, monkeypatch):
    """分区三：临时精液恰好等于实际量时，下游仍使用正的完整实际量，基础精液不变。"""
    from Script.Config import game_config

    actual_amount = int(game_config.config_semen_shoot_amount[0].base_semen_amount)
    result = _run_ejaculation_flow(booted, monkeypatch, base_semen_point=0, tem_extra_semen_point=actual_amount)
    assert result["tem_before"] == actual_amount
    _assert_full_downstream(result)


def test_temporary_above_actual_reaches_full_downstream(booted, monkeypatch):
    """分区四：临时精液大于实际量时，下游使用完整实际量，只扣所需临时精液。"""
    from Script.Config import game_config

    actual_amount = int(game_config.config_semen_shoot_amount[0].base_semen_amount)
    result = _run_ejaculation_flow(booted, monkeypatch, base_semen_point=0, tem_extra_semen_point=actual_amount + 15)
    assert result["tem_before"] > actual_amount
    _assert_full_downstream(result)
