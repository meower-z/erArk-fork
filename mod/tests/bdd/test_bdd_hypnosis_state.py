#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BDD 场景（近真实层）LB-BDD-005/006 扩展：催眠状态保留

通过真实 ModManager 加载全部 mod 后，在未 mock 的真实
Script.UI.Panel.hypnosis_panel.evaluate_hypnosis_completion（已被
local_hypnosis_state_fix 包装）上驱动催眠完成判定，验证：
- 博士默认催眠类型为无(0)且目标催眠度达标时，上游原本会把目标既有的
  催眠无意识态(4/5/6/7)清零；包装后既有状态被保留（单人1211与群体1212
  催眠结算都经由该函数，属于同一根因修复点）；
- 已选择催眠类型时正常写入新催眠态，包装不干预。

运行方式：.venv/bin/pytest mod/tests/bdd/test_bdd_hypnosis_state.py -v
"""

import pytest

from mod.tests.bdd.near_real_boot import boot_game_once
from mod.tests.bdd.test_bdd_pain_as_pleasure import _make_character


@pytest.fixture(scope="session")
def booted():
    """会话级近真实引导夹具；返回值类型：BootContext。"""
    return boot_game_once(enable_debug=True)


def _reset_hypnosis_scene(booted, hypnosis_type: int, target_flag: int, degree: float = 200.0):
    """
    重置催眠场景：玩家(0)与目标(1)

    参数:
    booted (BootContext): 引导上下文
    hypnosis_type (int): 博士当前催眠类型（0为无）
    target_flag (int): 目标既有无意识标记
    degree (float): 目标催眠度

    返回值类型：tuple(player, target)
    """
    booted.cache.character_data.clear()
    player = _make_character(booted, 0, target_id=1)
    target = _make_character(booted, 1, target_id=0)
    player.pl_ability.hypnosis_type = hypnosis_type
    target.hypnosis.hypnosis_degree = degree
    target.sp_flag.unconscious_h = target_flag
    return player, target


def test_patch_installed_on_real_hypnosis_panel(booted):
    """
    场景：催眠完成判定包装已安装到真实 hypnosis_panel 模块

    验证点：evaluate_hypnosis_completion 为 mod 实现且保留原函数引用。
    """
    from Script.UI.Panel import hypnosis_panel

    func = hypnosis_panel.evaluate_hypnosis_completion
    assert "local_hypnosis_state_fix" in func.__module__
    assert getattr(func, "_local_hypnosis_state_original", None) is not None


def test_default_type_completion_preserves_active_hypnosis(booted):
    """
    场景：默认类型为无(0)时催眠完成不清掉既有催眠态（真实上游函数）

    验证点：目标带催眠无意识态7、催眠度200，经真实（被包装的）
    evaluate_hypnosis_completion 判定后状态仍为7。未修复前上游类型0分支
    会把该标记清零（hypnosis_panel.py 类型0分支 unconscious_h = 0）。
    """
    from Script.UI.Panel import hypnosis_panel

    _, target = _reset_hypnosis_scene(booted, hypnosis_type=0, target_flag=7)

    result = hypnosis_panel.evaluate_hypnosis_completion(1)

    assert result == 1, "催眠度达标时应判定完成"
    assert target.sp_flag.unconscious_h == 7, "既有催眠态不应被类型0完成判定清零"


def test_selected_type_completion_writes_new_flag(booted):
    """
    场景：已选择催眠类型时正常写入新催眠态（包装不干预）

    验证点：博士类型为4（心控），目标催眠度达标，判定后目标标记为 4+3=7。
    """
    from Script.UI.Panel import hypnosis_panel

    _, target = _reset_hypnosis_scene(booted, hypnosis_type=4, target_flag=0, degree=999.0)

    result = hypnosis_panel.evaluate_hypnosis_completion(1)

    assert result == 1
    assert target.sp_flag.unconscious_h == 7, "已选类型应写入对应催眠无意识态"
