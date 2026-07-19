# -*- coding: UTF-8 -*-
"""苦痛快感化直接苦痛写入路径的生产函数回归测试。"""

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
    """参数：无；返回：ChangeData；用途：记录状态变化。"""

    def __init__(self):
        """参数：无；返回：None；用途：初始化状态变化容器。"""
        self.status_data = {}
        self.target_change = {}


class TargetChange:
    """参数：无；返回：TargetChange；用途：记录目标角色状态变化。"""

    def __init__(self):
        """参数：无；返回：None；用途：初始化目标角色状态变化容器。"""
        self.status_data = {}


def _find_function(source_path: Path, function_name: str):
    """参数：源码路径与函数名；返回：ast.FunctionDef；用途：读取指定生产函数。"""
    source_tree = ast.parse(source_path.read_text(encoding="utf-8"), filename=str(source_path))
    for node in source_tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            function_node = copy.deepcopy(node)
            function_node.decorator_list = []
            return function_node
    raise AssertionError(f"missing production function: {function_name}")


def _load_function(source_path: Path, function_name: str, namespace: dict):
    """参数：源码路径、函数名与命名空间；返回：生产函数；用途：隔离加载单个生产函数。"""
    function_node = _find_function(source_path, function_name)
    module_node = ast.fix_missing_locations(ast.Module(body=[function_node], type_ignores=[]))
    exec(compile(module_node, str(source_path), "exec"), namespace)
    return namespace[function_name]


def _build_direct_runtime(active: bool):
    """参数：苦痛快感化开关；返回：运行命名空间与记录；用途：建立直接写入路径的最小生产环境。"""
    character = SimpleNamespace(
        dead=False,
        name="测试角色",
        status_data={17: 0, 18: 0, 23: 0},
        ability={15: 0, 17: 0, 36: 5},
        hypnosis=SimpleNamespace(pain_as_pleasure=active),
        h_state=SimpleNamespace(extra_orgasm_count=1),
    )
    conversion_calls = []
    drawn_text = []

    def try_settle_pain_as_pleasure(character_id, pain_value, change_data=None, change_data_to_target_change=None):
        """参数：角色、苦痛值与记录；返回：bool；用途：模拟已验收的转换 owner 契约。"""
        conversion_calls.append((character_id, pain_value, change_data, change_data_to_target_change))
        if pain_value <= 0 or not character.hypnosis.pain_as_pleasure:
            return False
        psychological_value = int(pain_value * 2)
        character.status_data[23] += psychological_value
        if change_data is not None:
            change_data.status_data.setdefault(23, 0)
            change_data.status_data[23] += psychological_value
        return True

    class NormalDraw:
        """参数：无；返回：NormalDraw；用途：记录额外绝顶提示文本。"""

        def __init__(self):
            """参数：无；返回：None；用途：初始化绘制对象。"""
            self.text = ""
            self.width = 0

        def draw(self):
            """参数：无；返回：None；用途：保存绘制文本。"""
            drawn_text.append(self.text)

    namespace = {
        "cache": SimpleNamespace(character_data={1: character}),
        "attr_calculation": SimpleNamespace(get_mark_debuff_adjust=lambda _level: 1),
        "game_type": SimpleNamespace(CharacterStatusChange=ChangeData),
        "try_settle_pain_as_pleasure": try_settle_pain_as_pleasure,
        "draw": SimpleNamespace(NormalDraw=NormalDraw),
        "_": lambda text: text,
        "window_width": 120,
    }
    return namespace, character, conversion_calls, drawn_text


@pytest.mark.parametrize(
    ("function_name", "expected_pain"),
    (
        ("handle_add_small_pain", 20),
        ("handle_add_middle_pain", 100),
        ("handle_add_large_pain", 1000),
    ),
)
@pytest.mark.parametrize("active", (False, True))
def test_direct_pain_writers_use_one_conversion_owner(function_name, expected_pain, active):
    """参数：生产函数、源苦痛值与开关；返回：None；用途：验证直接写入只走一次转换 owner。"""
    namespace, character, conversion_calls, _drawn_text = _build_direct_runtime(active)
    handler = _load_function(SECOND_SOURCE, function_name, namespace)
    change = ChangeData()

    handler(1, change)

    assert len(conversion_calls) == 1
    assert conversion_calls[0][1] == expected_pain
    if active:
        assert character.status_data[17] == 0
        assert character.status_data[23] == expected_pain * 2
        assert change.status_data == {23: expected_pain * 2}
    else:
        assert character.status_data[17] == expected_pain
        assert character.status_data[23] == 0
        assert change.status_data == {17: expected_pain}


@pytest.mark.parametrize("active", (False, True))
def test_extra_orgasm_routes_pain_without_skipping_terror_or_reset(active):
    """参数：苦痛快感化开关；返回：None；用途：验证额外绝顶路由、恐怖、文本与清零。"""
    namespace, character, conversion_calls, drawn_text = _build_direct_runtime(active)
    handler = _load_function(SECOND_SOURCE, "handle_extra_orgasm", namespace)
    change = ChangeData()

    handler(1, change)

    assert len(conversion_calls) == 1
    assert conversion_calls[0][1] == 120
    assert character.status_data[18] == 120
    assert character.h_state.extra_orgasm_count == 0
    if active:
        assert character.status_data[17] == 0
        assert character.status_data[23] == 240
        assert change.status_data == {23: 240, 18: 120}
        assert "心理快感和恐怖" in drawn_text[0]
    else:
        assert character.status_data[17] == 120
        assert character.status_data[23] == 0
        assert change.status_data == {17: 120, 18: 120}
        assert "苦痛和恐怖" in drawn_text[0]


def test_conversion_owner_delegates_active_positive_value_once():
    """参数：无；返回：None；用途：验证转换 owner 只委托一次 canonical state 23。"""
    character = SimpleNamespace(ability={36: 5}, hypnosis=SimpleNamespace(pain_as_pleasure=True))
    settle_calls = []
    namespace = {
        "cache": SimpleNamespace(character_data={1: character}),
        "handle_premise": SimpleNamespace(handle_hypnosis_pain_as_pleasure=lambda _character_id: character.hypnosis.pain_as_pleasure),
        "base_chara_state_common_settle": lambda *args, **kwargs: settle_calls.append((args, kwargs)),
        "game_type": SimpleNamespace(CharacterStatusChange=ChangeData, TargetChange=TargetChange),
        "Optional": Optional,
        "Union": Union,
    }
    owner = _load_function(COMMON_SOURCE, "try_settle_pain_as_pleasure", namespace)
    change = ChangeData()
    target_change = ChangeData()

    assert owner(1, 70, change, target_change) is True
    assert len(settle_calls) == 1
    args, kwargs = settle_calls[0]
    assert args[:4] == (1, 70, 23, 0)
    assert kwargs["ability_level"] == 5
    assert kwargs["tenths_add"] is False
    assert kwargs["change_data"] is change
    assert kwargs["change_data_to_target_change"] is target_change


@pytest.mark.parametrize(("active", "pain_value"), ((False, 70), (True, 0), (True, -70)))
def test_conversion_owner_leaves_inactive_or_nonpositive_value_unhandled(active, pain_value):
    """参数：开关与苦痛值；返回：None；用途：验证未转换值不进入 canonical state 23。"""
    character = SimpleNamespace(ability={36: 5}, hypnosis=SimpleNamespace(pain_as_pleasure=active))
    settle_calls = []
    namespace = {
        "cache": SimpleNamespace(character_data={1: character}),
        "handle_premise": SimpleNamespace(handle_hypnosis_pain_as_pleasure=lambda _character_id: character.hypnosis.pain_as_pleasure),
        "base_chara_state_common_settle": lambda *args, **kwargs: settle_calls.append((args, kwargs)),
        "game_type": SimpleNamespace(CharacterStatusChange=ChangeData, TargetChange=TargetChange),
        "Optional": Optional,
        "Union": Union,
    }
    owner = _load_function(COMMON_SOURCE, "try_settle_pain_as_pleasure", namespace)

    assert owner(1, pain_value) is False
    assert settle_calls == []


@pytest.mark.parametrize("guard_name", ("sleep", "unconscious"))
def test_direct_writer_does_not_fall_back_when_canonical_psychological_settlement_returns_early(guard_name):
    """参数：心理快感抑制条件；返回：None；用途：验证 canonical 提前返回后不回落写苦痛。"""
    character = SimpleNamespace(
        status_data={17: 0, 23: 0},
        ability={15: 0, 36: 5},
        hypnosis=SimpleNamespace(pain_as_pleasure=True),
    )
    settle_calls = []
    namespace = {
        "cache": SimpleNamespace(character_data={1: character}),
        "handle_premise": SimpleNamespace(handle_hypnosis_pain_as_pleasure=lambda _character_id: True),
        "base_chara_state_common_settle": lambda *args, **kwargs: settle_calls.append((guard_name, args, kwargs)),
        "attr_calculation": SimpleNamespace(get_mark_debuff_adjust=lambda _level: 1),
        "game_type": SimpleNamespace(CharacterStatusChange=ChangeData, TargetChange=TargetChange),
        "Optional": Optional,
        "Union": Union,
    }
    namespace["try_settle_pain_as_pleasure"] = _load_function(COMMON_SOURCE, "try_settle_pain_as_pleasure", namespace)
    handler = _load_function(SECOND_SOURCE, "handle_add_small_pain", namespace)
    change = ChangeData()

    handler(1, change)

    assert len(settle_calls) == 1
    assert settle_calls[0][1][:3] == (1, 20, 23)
    assert character.status_data == {17: 0, 23: 0}
    assert change.status_data == {}
