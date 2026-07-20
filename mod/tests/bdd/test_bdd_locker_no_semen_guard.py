#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
BDD 场景（近真实层）：无精液时衣柜菜单省略"用衣服冲，射在上面"

对应票据 .scratch/correct-semen-climax-flow/issues/03-hide-locker-ejaculation-without-semen.md：
玩家检查干员衣柜时，若基础精液与临时精液合计不超过 2ml，射精选项不再显示；
合计超过 2ml 时该选项保留；无论精液量多少，闻味道、偷内裤、偷袜子、返回等操作始终可用。

测试通过真实 near-real 引导载入配置与真实场景，在真实 Locker_Room 场景上构造包含衣物的
真实衣柜，直接驱动衣柜操作菜单构造（Script.UI.Panel.check_locker_panel），
捕获玩家可见的按钮文本进行断言，不启动 Tk/GUI。

运行方式（仓库根目录）：.venv/bin/pytest mod/tests/bdd/test_bdd_locker_no_semen_guard.py -v
"""

import os

import pytest

from mod.tests.bdd.near_real_boot import boot_game_once

# 面板中各按钮的玩家可见文本片段（去掉序号前缀，便于子串匹配）
SMELL_LABEL = "把内衣拿起来闻一闻味道"
STEAL_PAN_LABEL = "偷走内裤"
STEAL_SOCKS_LABEL = "偷走袜子"
SHOOT_LABEL = "用衣服冲，射在上面"
BACK_LABEL = "返回"

# 衣物类型编号：面板固定用 9=内裤、10=袜子；0 作为普通上装占位
PANTIES_TYPE = 9
SOCKS_TYPE = 10
UPPER_TYPE = 0


@pytest.fixture(scope="session")
def booted():
    """会话级近真实引导夹具。返回值类型：BootContext。"""
    return boot_game_once(enable_debug=True)


def _capture_locker_menu(booted, monkeypatch, semen_point: int, second_round_semen_point: int | None = None) -> tuple:
    """
    在真实 Locker_Room 场景上构造含衣物的真实衣柜并捕获菜单按钮文本

    参数:
    booted (BootContext) -- 近真实引导上下文
    monkeypatch (pytest.MonkeyPatch) -- 用于隔离缓存与阻断输入循环
    semen_point (int) -- 玩家第一轮基础精液量（临时精液置 0，合计即该值）
    second_round_semen_point (int | None) -- 非空时在第一轮输入后切换的第二轮基础精液量

    返回值类型：tuple[list[str], list[list[str]]]
    功能描述：把玩家放入真实衣柜间场景，给目标干员的浴场衣柜放入上衣/内裤/袜子，
    捕获 check_cloth 绘制出的全部按钮文本和每轮输入白名单后退出。
    """
    from Script.Core import cache_control, game_type, py_cmd
    from Script.Config import game_config
    from Script.UI.Panel import check_locker_panel

    cache = cache_control.cache

    # 定位任意一个真实 Locker_Room 场景，取其路径列表作为玩家所在位置
    locker_key = next(
        k for k, v in cache.scene_data.items() if "Locker_Room" in getattr(v, "scene_tag", "")
    )
    position = locker_key.split(os.sep)

    # 构造玩家：设置所在位置与合计精液量（临时精液为 0）
    player = game_type.Character()
    player.position = position
    player.semen_point = semen_point
    player.tem_extra_semen_point = 0

    # 构造目标干员并填充浴场衣柜：上衣 + 内裤 + 袜子各放一件真实服装
    npc_id = 900001
    target = game_type.Character()
    target.name = "测试干员"
    cloth_tem_id = next(iter(game_config.config_clothing_tem))
    clothing_types = list(game_config.config_clothing_type.keys())
    for clothing_type in clothing_types:
        target.cloth.cloth_locker_in_shower[clothing_type] = []
    target.cloth.cloth_locker_in_shower[UPPER_TYPE] = [cloth_tem_id]
    target.cloth.cloth_locker_in_shower[PANTIES_TYPE] = [cloth_tem_id]
    target.cloth.cloth_locker_in_shower[SOCKS_TYPE] = [cloth_tem_id]
    # 衣柜污浊信息按列表结构预填，避免面板走补齐分支（对不连续的类型编号做占位）
    type_config = game_config.config_clothing_type
    target.dirty.cloth_locker_semen = [
        [type_config[t].name if t in type_config else "", 0, 0, 0]
        for t in range(max(clothing_types) + 1)
    ]

    monkeypatch.setitem(cache.character_data, 0, player)
    monkeypatch.setitem(cache.character_data, npc_id, target)

    # 捕获按钮显示文本和每轮输入白名单
    captured = []
    accepted_options = []

    def _record_pcmd(cmd_str, cmd_id, *args, **kwargs):
        """参数：cmd_str(按钮显示文本)、cmd_id(返回值)及其余透传参数；返回：None；用途：记录玩家可见按钮文本。"""
        captured.append(cmd_str)

    def _askfor_all(return_list):
        """参数：return_list(list[str])输入白名单；返回：str；用途：记录每轮白名单并按需触发第二轮重绘。"""
        accepted_options.append(return_list.copy())
        if second_round_semen_point is not None and len(accepted_options) == 1:
            player.semen_point = second_round_semen_point
            return ""
        return BACK_LABEL

    monkeypatch.setattr(py_cmd, "pcmd", _record_pcmd)
    monkeypatch.setattr(check_locker_panel.flow_handle, "askfor_all", _askfor_all)

    find_draw = check_locker_panel.FindDraw(npc_id, check_locker_panel.window_width, True, True, 1)
    find_draw.check_cloth()

    return captured, accepted_options


def _has_label(captured: list, label: str) -> bool:
    """参数：captured(按钮文本列表)、label(标签片段)；返回：bool；用途：判断某标签是否出现在任一按钮文本中。"""
    return any(label in text for text in captured)


def test_locker_menu_hides_shoot_option_without_semen(booted, monkeypatch):
    """
    场景：合计精液不超过 2ml 时，衣柜菜单省略射精选项，其余操作保留

    验证点：无"用衣服冲，射在上面"；闻味道、偷内裤、偷袜子、返回均在。
    """
    captured, _ = _capture_locker_menu(booted, monkeypatch, semen_point=2)

    assert not _has_label(captured, SHOOT_LABEL)
    assert _has_label(captured, SMELL_LABEL)
    assert _has_label(captured, STEAL_PAN_LABEL)
    assert _has_label(captured, STEAL_SOCKS_LABEL)
    assert _has_label(captured, BACK_LABEL)


def test_locker_menu_keeps_shoot_option_with_semen(booted, monkeypatch):
    """
    场景：合计精液超过 2ml 时，射精选项继续显示

    验证点：控制组含"用衣服冲，射在上面"，其余操作同样保留。
    """
    captured, _ = _capture_locker_menu(booted, monkeypatch, semen_point=3)

    assert _has_label(captured, SHOOT_LABEL)
    assert _has_label(captured, SMELL_LABEL)
    assert _has_label(captured, STEAL_PAN_LABEL)
    assert _has_label(captured, STEAL_SOCKS_LABEL)
    assert _has_label(captured, BACK_LABEL)


def test_locker_menu_rebuilds_input_allowlist_after_semen_drops(booted, monkeypatch):
    """
    场景：同一衣柜菜单第一轮精液为 3ml，返回菜单前降为 2ml。
    验证点：第一轮输入白名单包含“4”，第二轮不再包含“4”，与第二轮显示按钮保持一致。
    """
    _, accepted_options = _capture_locker_menu(
        booted,
        monkeypatch,
        semen_point=3,
        second_round_semen_point=2,
    )

    assert len(accepted_options) == 2
    assert "4" in accepted_options[0]
    assert "4" not in accepted_options[1]
