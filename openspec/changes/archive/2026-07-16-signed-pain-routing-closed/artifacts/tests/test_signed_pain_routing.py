# -*- coding: UTF-8 -*-
"""苦痛快感化正向门槛的生产函数回归测试。"""

import ast
import copy
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Optional, Union

import pytest


REPO_ROOT = Path(os.environ.get("ERARK_REPO_ROOT", Path(__file__).resolve().parents[1]))
COMMON_SOURCE = REPO_ROOT / "Script" / "Settle" / "common_default.py"
SECOND_SOURCE = REPO_ROOT / "Script" / "Settle" / "Second_effect.py"


class ChangeData:
    """参数：无；返回：ChangeData；用途：记录生产结算函数写入的状态和经验变化。"""

    def __init__(self):
        """参数：无；返回：None；用途：初始化变化记录容器。"""
        self.status_data = {}
        self.experience = []
        self.target_change = {}


class TargetChange:
    """参数：无；返回：TargetChange；用途：记录交互对象的状态变化。"""

    def __init__(self):
        """参数：无；返回：None；用途：初始化目标变化容器。"""
        self.status_data = {}


def _find_function(function_name: str, source_path: Path = COMMON_SOURCE):
    """参数：函数名与源码路径；返回：ast.FunctionDef；用途：读取指定生产函数。"""
    source_tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
    for node in source_tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            function_node = copy.deepcopy(node)
            function_node.decorator_list = []
            return function_node
    raise AssertionError(f"missing production function: {function_name}")


def _load_functions(namespace: dict):
    """参数：namespace(dict)；返回：dict；用途：隔离执行真实通用结算与额外快感函数。"""
    function_nodes = [_find_function("extra_feel_settle"), _find_function("try_settle_pain_as_pleasure"), _find_function("base_chara_state_common_settle")]
    module_node = ast.fix_missing_locations(ast.Module(body=function_nodes, type_ignores=[]))
    exec(compile(module_node, str(COMMON_SOURCE), "exec"), namespace)
    return namespace


def _load_second_function(function_name: str, namespace: dict):
    """参数：二段结算函数名与命名空间；返回：生产函数；用途：隔离加载直接苦痛写入函数。"""
    function_node = _find_function(function_name, SECOND_SOURCE)
    module_node = ast.fix_missing_locations(ast.Module(body=[function_node], type_ignores=[]))
    exec(compile(module_node, str(SECOND_SOURCE), "exec"), namespace)
    return namespace[function_name]


def _build_runtime(*, active: bool, masochism_level: int):
    """参数：active(bool)、masochism_level(int)；返回：运行命名空间与记录；用途：建立生产函数最小运行环境。"""
    character = SimpleNamespace(
        dead=False,
        status_data={state_id: 0 for state_id in range(30)},
        ability={state_id: 0 for state_id in range(120)},
        hypnosis=SimpleNamespace(pain_as_pleasure=active),
    )
    character.status_data[17] = 100
    character.status_data[23] = 200
    character.ability[36] = masochism_level
    player = SimpleNamespace(target_character_id=1)
    cache = SimpleNamespace(character_data={0: player, 1: character}, pl_pre_behavior_instruce=[])
    states = {state_id: SimpleNamespace(type=1, name=str(state_id)) for state_id in range(30)}
    states[23] = SimpleNamespace(type=0, name="心理")
    experience_calls = []
    feel_adjust_calls = []
    namespace = {
        "cache": cache,
        "game_config": SimpleNamespace(config_character_state=states),
        "game_type": SimpleNamespace(Character=object, CharacterStatusChange=ChangeData, TargetChange=TargetChange),
        "handle_premise": SimpleNamespace(
            handle_unconscious_flag_ge_1=lambda _character_id: False,
            handle_action_sleep=lambda _character_id: False,
            handle_normal_6=lambda _character_id: True,
            handle_hypnosis_pain_as_pleasure=lambda _character_id: character.hypnosis.pain_as_pleasure,
        ),
        "chara_base_state_adjust": lambda *_args: 1,
        "chara_feel_state_adjust": lambda *_args: feel_adjust_calls.append(_args) or 2,
        "base_chara_experience_common_settle": lambda character_id, experience_id, **_kwargs: experience_calls.append((character_id, experience_id)),
        "_": lambda text: text,
        "Optional": Optional,
        "Union": Union,
    }
    _load_functions(namespace)
    production_settle = namespace["base_chara_state_common_settle"]
    settle_calls = []

    def tracked_settle(*args, **kwargs):
        """参数：与生产函数一致；返回：生产函数返回值；用途：记录递归状态结算入口。"""
        settle_calls.append((args, kwargs))
        return production_settle(*args, **kwargs)

    namespace["base_chara_state_common_settle"] = tracked_settle
    return namespace, character, experience_calls, feel_adjust_calls, settle_calls


@pytest.mark.parametrize("final_delta", (0, -40))
@pytest.mark.parametrize("masochism_level", (4, 5))
def test_non_positive_pain_uses_complete_ordinary_state_path(final_delta, masochism_level):
    """参数：最终苦痛值与受虐能力；返回：None；用途：验证非正值落回完整普通苦痛结算。"""
    namespace, character, experience_calls, feel_adjust_calls, settle_calls = _build_runtime(active=True, masochism_level=masochism_level)
    change = ChangeData()

    namespace["base_chara_state_common_settle"](1, final_delta, 17, base_value=0, tenths_add=False, change_data=change)

    assert character.status_data[17] == max(0, 100 + final_delta)
    assert change.status_data[17] == final_delta
    recursive_calls = settle_calls[1:]
    if masochism_level >= 5:
        assert character.status_data[23] == 220
        assert change.status_data[23] == 20
        assert experience_calls == [(1, 155)]
        assert len(feel_adjust_calls) == 1
        assert len(recursive_calls) == 1
        assert recursive_calls[0][0][1:3] == (10, 23)
    else:
        assert character.status_data[23] == 200
        assert 23 not in change.status_data
        assert experience_calls == []
        assert feel_adjust_calls == []
        assert recursive_calls == []


def test_positive_pain_preserves_existing_conversion_recursion():
    """参数：无；返回：None；用途：验证正向苦痛仍只经过一次原心理快感递归。"""
    namespace, character, experience_calls, feel_adjust_calls, settle_calls = _build_runtime(active=True, masochism_level=5)
    change = ChangeData()

    namespace["base_chara_state_common_settle"](1, 40, 17, base_value=0, tenths_add=False, change_data=change)

    assert character.status_data[17] == 100
    assert character.status_data[23] == 280
    assert change.status_data == {23: 80}
    assert experience_calls == []
    assert len(feel_adjust_calls) == 1
    assert len(settle_calls) == 2
    assert settle_calls[1][0][1:3] == (40, 23)


def test_positive_conversion_forwards_both_change_records():
    """参数：无；返回：None；用途：验证正向转换只向两类记录写入心理快感。"""
    namespace, character, experience_calls, feel_adjust_calls, settle_calls = _build_runtime(active=True, masochism_level=5)
    change = ChangeData()
    target_change = ChangeData()

    namespace["base_chara_state_common_settle"](1, 40, 17, base_value=0, tenths_add=False, change_data=change, change_data_to_target_change=target_change)

    assert character.status_data[17] == 100
    assert character.status_data[23] == 280
    assert change.status_data == {23: 80}
    assert target_change.target_change[1].status_data == {23: 80}
    assert experience_calls == []
    assert len(feel_adjust_calls) == 1
    assert len(settle_calls) == 2


@pytest.mark.parametrize("guard_name", ("sleep", "unconscious"))
def test_positive_conversion_preserves_psychological_admission_guard(guard_name):
    """参数：心理快感抑制条件；返回：None；用途：验证转换后由心理快感通用入口决定是否结算。"""
    namespace, character, experience_calls, feel_adjust_calls, settle_calls = _build_runtime(active=True, masochism_level=5)
    if guard_name == "sleep":
        namespace["handle_premise"].handle_action_sleep = lambda _character_id: True
    else:
        namespace["handle_premise"].handle_unconscious_flag_ge_1 = lambda _character_id: True
    change = ChangeData()
    target_change = ChangeData()

    namespace["base_chara_state_common_settle"](1, 40, 17, base_value=0, tenths_add=False, change_data=change, change_data_to_target_change=target_change)

    assert character.status_data[17] == 100
    assert character.status_data[23] == 200
    assert change.status_data == {}
    assert target_change.target_change == {}
    assert experience_calls == []
    assert feel_adjust_calls == []
    assert len(settle_calls) == 2


@pytest.mark.parametrize(
    ("active", "guard_name", "expected_pain", "expected_psychological", "expected_change", "expected_feel_calls"),
    (
        (False, None, 125, 200, {17: 25}, 0),
        (True, None, 100, 250, {23: 50}, 1),
        (True, "sleep", 100, 200, {}, 0),
        (True, "unconscious", 100, 200, {}, 0),
    ),
)
def test_direct_small_pain_uses_canonical_psychological_settlement_once(active, guard_name, expected_pain, expected_psychological, expected_change, expected_feel_calls):
    """参数：开关、抑制条件与预期值；返回：None；用途：验证直接苦痛只调用一次心理快感通用结算。"""
    namespace, character, experience_calls, feel_adjust_calls, settle_calls = _build_runtime(active=active, masochism_level=5)
    namespace["attr_calculation"] = SimpleNamespace(get_mark_debuff_adjust=lambda _ability_level: 1)
    if guard_name == "sleep":
        namespace["handle_premise"].handle_action_sleep = lambda _character_id: True
    elif guard_name == "unconscious":
        namespace["handle_premise"].handle_unconscious_flag_ge_1 = lambda _character_id: True
    handler = _load_second_function("handle_add_small_pain", namespace)
    change = ChangeData()

    handler(1, change)

    assert character.status_data[17] == expected_pain
    assert character.status_data[23] == expected_psychological
    assert change.status_data == expected_change
    assert experience_calls == []
    assert len(feel_adjust_calls) == expected_feel_calls
    assert len(settle_calls) == (1 if active else 0)


@pytest.mark.parametrize("final_delta", (-40, 40))
def test_inactive_flag_keeps_ordinary_state_path(final_delta):
    """参数：最终苦痛值；返回：None；用途：验证开关关闭时正负苦痛均保持上游普通结算。"""
    namespace, character, experience_calls, feel_adjust_calls, settle_calls = _build_runtime(active=False, masochism_level=4)
    change = ChangeData()

    namespace["base_chara_state_common_settle"](1, final_delta, 17, base_value=0, tenths_add=False, change_data=change)

    assert character.status_data[17] == 100 + final_delta
    assert character.status_data[23] == 200
    assert change.status_data == {17: final_delta}
    assert experience_calls == []
    assert feel_adjust_calls == []
    assert len(settle_calls) == 1
