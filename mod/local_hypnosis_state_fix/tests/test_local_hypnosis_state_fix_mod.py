# -*- coding: UTF-8 -*-
"""本地催眠状态修复测试。"""

import datetime
import json
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace


class DummyDraw:
    """参数：任意；返回：DummyDraw；用途：伪造绘制对象。"""

    def __init__(self, *args, **kwargs):
        """参数：任意；返回：None；用途：初始化伪绘制对象。"""
        self.text = ""
        self.style = ""

    def draw(self):
        """参数：无；返回：None；用途：伪造绘制。"""
        return None


class ChangeData:
    """参数：无；返回：ChangeData；用途：占位状态变更对象。"""

    def __init__(self):
        """参数：无；返回：None；用途：初始化占位对象。"""
        self.status_data = {}


def install_fake_modules(cache, calls=None, original_weight=None, hypnosis_predicate=None):
    """参数：cache(SimpleNamespace)为测试缓存，calls(list)为调用记录，original_weight(callable)为原口上权重函数；返回：tuple为恢复函数和催眠面板模块；用途：安装组件运行所需伪模块。"""
    calls = calls if calls is not None else []
    missing = object()

    script_module = ModuleType("Script")
    core_module = ModuleType("Script.Core")
    cache_control = ModuleType("Script.Core.cache_control")
    design_module = ModuleType("Script.Design")
    handle_premise = ModuleType("Script.Design.handle_premise")
    map_handle = ModuleType("Script.Design.map_handle")
    settle_module = ModuleType("Script.Settle")
    settle_default = ModuleType("Script.Settle.default")
    ui_module = ModuleType("Script.UI")
    panel_module = ModuleType("Script.UI.Panel")
    hypnosis_panel = ModuleType("Script.UI.Panel.hypnosis_panel")

    class FakeChooseHypnosisTypePanel:
        """参数：width(int)为宽度，instruct_flag(bool)为是否指令模式；返回：FakeChooseHypnosisTypePanel；用途：伪造催眠类型选择面板。"""

        def __init__(self, width, instruct_flag=False):
            """参数：width(int)为宽度，instruct_flag(bool)为是否指令模式；返回：None；用途：初始化伪面板。"""
            self.width = width
            self.instruct_flag = instruct_flag
            calls.append(("panel", width, instruct_flag))

        def draw(self):
            """参数：无；返回：None；用途：模拟玩家选择心控催眠。"""
            calls.append(("draw",))
            pl_data = cache.character_data[0]
            target_data = cache.character_data[pl_data.target_character_id]
            pl_data.pl_ability.hypnosis_type = 4
            target_data.sp_flag.unconscious_h = 7

        def change_hypnosis_type(self, hypnosis_type_cid):
            """参数：hypnosis_type_cid(int)为催眠类型；返回：None；用途：原面板方法占位。"""
            calls.append(("original_change", hypnosis_type_cid))

        def body_or_mind_control_option(self, flag):
            """参数：flag(int)为控制类型；返回：None；用途：记录心控/身控分支。"""
            calls.append(("body_or_mind", flag))

    cache_control.cache = cache
    constant = SimpleNamespace(settle_behavior_effect_data={})
    settle_default.handle_hypnosis_one = lambda character_id, add_time, change_data, now_time: calls.append(("original", character_id, add_time))
    if original_weight is None:
        def original_weight(premises, character_id, calculated, weight_all_to_1_flag=False, unconscious_pass_flag=False):
            """参数：同口上权重函数；返回：tuple为权重和缓存；用途：默认伪造催眠门禁权重。"""
            return (1 if unconscious_pass_flag else 0, calculated)

    handle_premise.get_weight_from_premise_dict = original_weight
    handle_premise.settle_chara_unnormal_flag = lambda character_id, flag_id: calls.append(("settle", character_id, flag_id))

    def default_hypnosis_predicate(character_id):
        """参数：character_id(int)为角色ID；返回：bool为目标是否处于催眠无意识；用途：默认伪造催眠前提。"""
        target_id = cache.character_data[character_id].target_character_id
        return cache.character_data[target_id].sp_flag.unconscious_h in {4, 5, 6, 7}

    handle_premise.handle_t_unconscious_hypnosis_flag = hypnosis_predicate or default_hypnosis_predicate
    map_handle.get_map_system_path_str_for_list = lambda position: "/".join(position)
    hypnosis_panel.cache = cache
    hypnosis_panel.window_width = 80
    hypnosis_panel.game_config = SimpleNamespace(
        config_hypnosis_type={
            0: SimpleNamespace(name="手动", hypnosis_degree=50),
            4: SimpleNamespace(name="心控", hypnosis_degree=200),
        }
    )
    hypnosis_panel.draw = SimpleNamespace(LineDraw=DummyDraw, WaitDraw=DummyDraw)
    hypnosis_panel._ = lambda text: text
    hypnosis_panel.Chose_Hypnosis_Type_Panel = FakeChooseHypnosisTypePanel

    script_module.Core = core_module
    script_module.Design = design_module
    script_module.Settle = settle_module
    script_module.UI = ui_module
    core_module.cache_control = cache_control
    core_module.constant = constant
    design_module.handle_premise = handle_premise
    design_module.map_handle = map_handle
    settle_module.default = settle_default
    ui_module.Panel = panel_module
    panel_module.hypnosis_panel = hypnosis_panel

    module_map = {
        "Script": script_module,
        "Script.Core": core_module,
        "Script.Core.cache_control": cache_control,
        "Script.Design": design_module,
        "Script.Design.handle_premise": handle_premise,
        "Script.Design.map_handle": map_handle,
        "Script.Settle": settle_module,
        "Script.Settle.default": settle_default,
        "Script.UI": ui_module,
        "Script.UI.Panel": panel_module,
        "Script.UI.Panel.hypnosis_panel": hypnosis_panel,
    }
    old_modules = {name: sys.modules.get(name, missing) for name in module_map}
    sys.modules.update(module_map)

    def restore():
        """参数：无；返回：None；用途：恢复测试前的模块表。"""
        for name, old_module in old_modules.items():
            if old_module is missing:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = old_module

    return restore, hypnosis_panel


def load_component():
    """参数：无；返回：dict为组件脚本命名空间；用途：加载组件脚本但不加载其他mod。"""
    mod_root = Path(__file__).resolve().parents[1]
    script_path = mod_root / "scripts" / "local_hypnosis_state_fix.py"
    namespace = {"__builtins__": __builtins__, "__name__": "mod_local_hypnosis_state_fix_test"}
    exec(compile(script_path.read_text(encoding="utf-8"), str(script_path), "exec"), namespace)
    return namespace


def make_cache(hypnosis_type=0, target_degree=200, target_unconscious=0, sanity_point=1):
    """参数：hypnosis_type(int)为博士催眠类型，target_degree(int)为目标催眠度，target_unconscious(int)为目标无意识标记，sanity_point(int)为理智；返回：SimpleNamespace为测试缓存；用途：快速构造催眠测试缓存。"""
    pl_data = SimpleNamespace(
        name="博士",
        dead=False,
        sanity_point=sanity_point,
        target_character_id=1,
        position=["room"],
        pl_ability=SimpleNamespace(hypnosis_type=hypnosis_type),
    )
    target_data = SimpleNamespace(
        name="亚叶",
        hypnosis=SimpleNamespace(hypnosis_degree=target_degree, increase_body_sensitivity=False, blockhead=False, active_h=False, pain_as_pleasure=False, roleplay=[]),
        sp_flag=SimpleNamespace(unconscious_h=target_unconscious),
        h_state=SimpleNamespace(npc_active_h=0),
    )
    return SimpleNamespace(character_data={0: pl_data, 1: target_data}, scene_data={})


def test_manifest_has_hidden_hypnosis_hooks_only():
    """参数：无；返回：None；用途：验证组件清单仅加载隐藏催眠补丁脚本。"""
    mod_root = Path(__file__).resolve().parents[1]
    manifest = json.loads((mod_root / "mod_info.json").read_text(encoding="utf-8"))

    assert manifest["mod_id"] == "local_hypnosis_state_fix"
    assert manifest["dependencies"] == []
    assert manifest["scripts"][0]["functions"] == []


def test_hypnosis_target_talk_bypasses_unconscious_gate():
    """参数：无；返回：None；用途：验证催眠类无意识目标绕过通用口上门禁。"""
    calls = []

    def fake_original(premises, character_id, calculated, weight_all_to_1_flag=False, unconscious_pass_flag=False):
        """参数：同原函数；返回：tuple；用途：记录门禁参数。"""
        calls.append((set(premises), character_id, unconscious_pass_flag))
        return (1 if unconscious_pass_flag else 0), calculated

    for hypnosis_flag in (4, 5, 6, 7):
        cache = make_cache(target_unconscious=hypnosis_flag)
        restore, _hypnosis_panel = install_fake_modules(cache, original_weight=fake_original)
        try:
            namespace = load_component()

            weight, calculated = namespace["patched_get_weight_from_premise_dict"]({"high_1"}, 0, {})

            assert weight == 1
            assert calculated == {}
        finally:
            restore()

    assert calls == [
        ({"high_1"}, 0, True),
        ({"high_1"}, 0, True),
        ({"high_1"}, 0, True),
        ({"high_1"}, 0, True),
    ]


def test_sleep_target_talk_keeps_unconscious_gate():
    """参数：无；返回：None；用途：验证普通睡眠无意识目标不绕过口上门禁。"""
    cache = make_cache(target_unconscious=1)
    calls = []

    def fake_original(premises, character_id, calculated, weight_all_to_1_flag=False, unconscious_pass_flag=False):
        """参数：同原函数；返回：tuple；用途：记录门禁参数。"""
        calls.append((set(premises), character_id, unconscious_pass_flag))
        return (1 if unconscious_pass_flag else 0), calculated

    restore, _hypnosis_panel = install_fake_modules(cache, original_weight=fake_original)
    try:
        namespace = load_component()

        weight, calculated = namespace["patched_get_weight_from_premise_dict"]({"high_1"}, 0, {})

        assert weight == 0
        assert calculated == {}
        assert calls == [({"high_1"}, 0, False)]
    finally:
        restore()


def test_hypnosis_talk_gate_uses_current_premise_predicate():
    """参数：无；返回：None；用途：验证口上门禁使用当前前提谓词而不是只看原始无意识标记。"""
    calls = []
    cache = make_cache(target_unconscious=1)

    def fake_original(premises, character_id, calculated, weight_all_to_1_flag=False, unconscious_pass_flag=False):
        """参数：同原函数；返回：tuple；用途：记录门禁参数。"""
        calls.append((character_id, unconscious_pass_flag))
        return (1 if unconscious_pass_flag else 0), calculated

    restore, _hypnosis_panel = install_fake_modules(cache, original_weight=fake_original, hypnosis_predicate=lambda character_id: True)
    try:
        namespace = load_component()

        weight, calculated = namespace["patched_get_weight_from_premise_dict"]({"high_1"}, 0, {})

        assert weight == 1
        assert calculated == {}
        assert calls == [(0, True)]
    finally:
        restore()

    calls.clear()
    cache = make_cache(target_unconscious=7)
    restore, _hypnosis_panel = install_fake_modules(cache, original_weight=fake_original, hypnosis_predicate=lambda character_id: False)
    try:
        namespace = load_component()

        weight, calculated = namespace["patched_get_weight_from_premise_dict"]({"high_1"}, 0, {})

        assert weight == 0
        assert calculated == {}
        assert calls == [(0, False)]
    finally:
        restore()


def test_change_hypnosis_type_in_instruct_mode_applies_current_target():
    """参数：无；返回：None；用途：验证指令模式切换催眠类型会立即套用目标状态。"""
    cache = make_cache(hypnosis_type=0, target_degree=200, target_unconscious=0)
    calls = []
    restore, _hypnosis_panel = install_fake_modules(cache, calls=calls)
    try:
        namespace = load_component()
        panel = SimpleNamespace(width=80, instruct_flag=True, body_or_mind_control_option=lambda flag: calls.append(("body_or_mind", flag)))

        namespace["patched_change_hypnosis_type"](panel, 4)

        assert cache.character_data[0].pl_ability.hypnosis_type == 4
        assert cache.character_data[1].sp_flag.unconscious_h == 7
        assert ("body_or_mind", 1) in calls
    finally:
        restore()


def test_change_hypnosis_type_outside_instruct_mode_only_changes_default():
    """参数：无；返回：None；用途：验证非指令模式只修改默认催眠类型。"""
    cache = make_cache(hypnosis_type=0, target_degree=200, target_unconscious=0)
    calls = []
    restore, _hypnosis_panel = install_fake_modules(cache, calls=calls)
    try:
        namespace = load_component()
        panel = SimpleNamespace(width=80, instruct_flag=False, body_or_mind_control_option=lambda flag: calls.append(("body_or_mind", flag)))

        namespace["patched_change_hypnosis_type"](panel, 4)

        assert cache.character_data[0].pl_ability.hypnosis_type == 4
        assert cache.character_data[1].sp_flag.unconscious_h == 0
        assert ("body_or_mind", 1) not in calls
    finally:
        restore()


def test_change_hypnosis_type_air_blocked_room_draws_warning():
    """参数：无；返回：None；用途：验证指令模式下空气催眠因地点不可锁门失败时给出与上游一致的警告，而非静默返回。"""
    cache = make_cache(hypnosis_type=0, target_degree=200, target_unconscious=0)
    cache.scene_data["room"] = SimpleNamespace(close_type=0, close_flag=0)
    calls = []
    restore, _hypnosis_panel = install_fake_modules(cache, calls=calls)
    _hypnosis_panel.game_config.config_hypnosis_type[2] = SimpleNamespace(name="空气", hypnosis_degree=100)

    class RecordingWaitDraw:
        """参数：无；返回：RecordingWaitDraw；用途：记录警告绘制文本。"""

        def __init__(self, *args, **kwargs):
            """参数：任意；返回：None；用途：初始化。"""
            self.text = ""
            self.style = ""

        def draw(self):
            """参数：无；返回：None；用途：记录绘制内容。"""
            calls.append(("warn", self.text))

    _hypnosis_panel.draw.WaitDraw = RecordingWaitDraw
    try:
        namespace = load_component()
        panel = SimpleNamespace(width=80, instruct_flag=True, body_or_mind_control_option=lambda flag: None)

        namespace["patched_change_hypnosis_type"](panel, 2)

        warn_texts = [text for tag, text in [c for c in calls if c[0] == "warn"]]
        assert any("不能锁门" in text for text in warn_texts), "不可锁门地点应绘制空气催眠失败警告"
        assert cache.character_data[1].sp_flag.unconscious_h == 0
    finally:
        restore()


def test_change_hypnosis_type_air_degree_insufficient_stays_silent():
    """参数：无；返回：None；用途：验证空气催眠因催眠度不足失败时不误报锁门警告。"""
    cache = make_cache(hypnosis_type=0, target_degree=10, target_unconscious=0)
    cache.scene_data["room"] = SimpleNamespace(close_type=1, close_flag=0)
    calls = []
    restore, _hypnosis_panel = install_fake_modules(cache, calls=calls)
    _hypnosis_panel.game_config.config_hypnosis_type[2] = SimpleNamespace(name="空气", hypnosis_degree=100)

    class RecordingWaitDraw:
        """参数：无；返回：RecordingWaitDraw；用途：记录警告绘制文本。"""

        def __init__(self, *args, **kwargs):
            """参数：任意；返回：None；用途：初始化。"""
            self.text = ""
            self.style = ""

        def draw(self):
            """参数：无；返回：None；用途：记录绘制内容。"""
            calls.append(("warn", self.text))

    _hypnosis_panel.draw.WaitDraw = RecordingWaitDraw
    try:
        namespace = load_component()
        panel = SimpleNamespace(width=80, instruct_flag=True, body_or_mind_control_option=lambda flag: None)

        namespace["patched_change_hypnosis_type"](panel, 2)

        warn_texts = [text for tag, text in [c for c in calls if c[0] == "warn"]]
        assert not any("不能锁门" in text for text in warn_texts), "催眠度不足时不应误报锁门警告"
    finally:
        restore()


def test_hypnosis_one_manual_type_prompts_and_applies_current_target():
    """参数：无；返回：None；用途：验证默认无类型的单人催眠会弹出手动选择并保持默认类型为无。"""
    cache = make_cache(hypnosis_type=0, target_degree=200, target_unconscious=0)
    calls = []
    restore, _hypnosis_panel = install_fake_modules(cache, calls=calls)
    try:
        namespace = load_component()
        namespace["_ORIGINAL_HYPNOSIS_ONE_EFFECT"] = lambda character_id, add_time, change_data, now_time: calls.append(("original", character_id, add_time))

        namespace["patched_handle_hypnosis_one"](0, 1, ChangeData(), datetime.datetime(2026, 1, 1, 12, 0))

        assert calls == [("original", 0, 1), ("panel", 80, True), ("draw",)]
        assert cache.character_data[1].sp_flag.unconscious_h == 7
        assert cache.character_data[0].pl_ability.hypnosis_type == 0
    finally:
        restore()


def test_hypnosis_one_default_type_does_not_prompt_again():
    """参数：无；返回：None；用途：验证已有默认催眠类型时直接校正状态而不再弹选择。"""
    cache = make_cache(hypnosis_type=4, target_degree=200, target_unconscious=7)
    calls = []
    restore, _hypnosis_panel = install_fake_modules(cache, calls=calls)
    try:
        namespace = load_component()
        namespace["_ORIGINAL_HYPNOSIS_ONE_EFFECT"] = lambda character_id, add_time, change_data, now_time: calls.append(("original", character_id, add_time))

        namespace["patched_handle_hypnosis_one"](0, 1, ChangeData(), datetime.datetime(2026, 1, 1, 12, 0))

        assert calls == [("original", 0, 1), ("settle", 1, 5), ("settle", 1, 6)]
        assert cache.character_data[1].sp_flag.unconscious_h == 7
        assert cache.character_data[0].pl_ability.hypnosis_type == 4
    finally:
        restore()


def test_hypnosis_one_does_not_apply_when_degree_is_not_enough():
    """参数：无；返回：None；用途：验证催眠度不足时不强行套用状态。"""
    cache = make_cache(hypnosis_type=4, target_degree=199, target_unconscious=0)
    calls = []
    restore, _hypnosis_panel = install_fake_modules(cache, calls=calls)
    try:
        namespace = load_component()
        namespace["_ORIGINAL_HYPNOSIS_ONE_EFFECT"] = lambda character_id, add_time, change_data, now_time: calls.append(("original", character_id, add_time))

        namespace["patched_handle_hypnosis_one"](0, 1, ChangeData(), datetime.datetime(2026, 1, 1, 12, 0))

        assert calls == [("original", 0, 1)]
        assert cache.character_data[1].sp_flag.unconscious_h == 0
    finally:
        restore()


def test_hypnosis_one_mind_control_ends_on_last_sanity_cost():
    """参数：无；返回：None；用途：验证理智耗尽导致催眠结束时不会重新写回催眠态。"""
    cache = make_cache(hypnosis_type=4, target_degree=200, target_unconscious=0, sanity_point=1)
    cache.character_data[1].hypnosis.increase_body_sensitivity = True
    cache.character_data[1].hypnosis.active_h = True
    cache.character_data[1].h_state.npc_active_h = 1
    cache.character_data[1].hypnosis.pain_as_pleasure = True
    cache.character_data[1].hypnosis.roleplay = [1]
    calls = []
    restore, _hypnosis_panel = install_fake_modules(cache, calls=calls)

    def fake_original(character_id, add_time, change_data, now_time):
        """参数：同原效果；返回：None；用途：模拟原效果因理智耗尽清掉催眠无意识。"""
        calls.append(("original_sanity", cache.character_data[0].sanity_point))
        character_data = cache.character_data[character_id]
        target_character_data = cache.character_data[character_data.target_character_id]
        character_data.sanity_point = max(character_data.sanity_point - 1, 0)
        target_character_data.sp_flag.unconscious_h = character_data.pl_ability.hypnosis_type + 3
        if character_data.sanity_point == 0 and target_character_data.sp_flag.unconscious_h:
            target_character_data.sp_flag.unconscious_h = 0

    try:
        namespace = load_component()
        namespace["_ORIGINAL_HYPNOSIS_ONE_EFFECT"] = fake_original

        namespace["patched_handle_hypnosis_one"](0, 1, ChangeData(), datetime.datetime(2026, 1, 1, 12, 0))

        assert calls == [("original_sanity", 1)]
        assert cache.character_data[0].sanity_point == 0
        assert cache.character_data[1].sp_flag.unconscious_h == 0
        assert cache.character_data[1].hypnosis.increase_body_sensitivity is False
        assert cache.character_data[1].hypnosis.active_h is False
        assert cache.character_data[1].h_state.npc_active_h == 0
        assert cache.character_data[1].hypnosis.pain_as_pleasure is False
        assert cache.character_data[1].hypnosis.roleplay == []
    finally:
        restore()


def test_hypnosis_one_preserves_active_hypnosis_when_original_clears_default_type():
    """参数：无；返回：None；用途：验证默认无类型不会把仍有理智的既有催眠态错误清掉。"""
    cache = make_cache(hypnosis_type=0, target_degree=200, target_unconscious=7, sanity_point=1)
    cache.character_data[1].hypnosis.pain_as_pleasure = True
    calls = []
    restore, _hypnosis_panel = install_fake_modules(cache, calls=calls)

    def fake_original(character_id, add_time, change_data, now_time):
        """参数：同原效果；返回：None；用途：模拟原效果因默认催眠类型为0清掉旧催眠态。"""
        calls.append(("original_clear", character_id, add_time))
        target_character_data = cache.character_data[cache.character_data[character_id].target_character_id]
        target_character_data.sp_flag.unconscious_h = 0

    try:
        namespace = load_component()
        namespace["_ORIGINAL_HYPNOSIS_ONE_EFFECT"] = fake_original

        namespace["patched_handle_hypnosis_one"](0, 1, ChangeData(), datetime.datetime(2026, 1, 1, 12, 0))

        # 恢复既有催眠态后需重算异常标记位5/6，避免前提缓存滞留旧值
        assert calls == [("original_clear", 0, 1), ("settle", 1, 5), ("settle", 1, 6)]
        assert cache.character_data[1].sp_flag.unconscious_h == 7
        assert cache.character_data[1].hypnosis.pain_as_pleasure is True
    finally:
        restore()


def test_evaluate_completion_restores_active_hypnosis_for_default_type():
    """参数：无；返回：None；用途：验证催眠完成判定包装在默认类型为无(0)时恢复被上游清零的既有催眠态（1211与1212群体催眠共用此路径）。"""
    cache = make_cache(hypnosis_type=0, target_degree=200, target_unconscious=7, sanity_point=1)
    calls = []
    restore, _hypnosis_panel = install_fake_modules(cache, calls=calls)

    def fake_original(character_id):
        """参数：character_id(int)为目标角色ID；返回：int为完成判定；用途：模拟上游类型0完成催眠并清零无意识标记。"""
        calls.append(("original_evaluate", character_id))
        cache.character_data[character_id].sp_flag.unconscious_h = 0
        return 1

    try:
        namespace = load_component()
        namespace["_ORIGINAL_EVALUATE_HYPNOSIS_COMPLETION"] = fake_original

        result = namespace["patched_evaluate_hypnosis_completion"](1)

        assert result == 1
        assert cache.character_data[1].sp_flag.unconscious_h == 7, "类型0完成催眠不应清掉既有催眠态"
        assert ("settle", 1, 5) in calls and ("settle", 1, 6) in calls
    finally:
        restore()


def test_evaluate_completion_keeps_new_flag_for_selected_type():
    """参数：无；返回：None；用途：验证已选择催眠类型时包装不干预上游写入的新催眠态。"""
    cache = make_cache(hypnosis_type=4, target_degree=200, target_unconscious=4, sanity_point=1)
    calls = []
    restore, _hypnosis_panel = install_fake_modules(cache, calls=calls)

    def fake_original(character_id):
        """参数：character_id(int)为目标角色ID；返回：int为完成判定；用途：模拟上游按类型4写入新催眠态。"""
        cache.character_data[character_id].sp_flag.unconscious_h = 7
        return 1

    try:
        namespace = load_component()
        namespace["_ORIGINAL_EVALUATE_HYPNOSIS_COMPLETION"] = fake_original

        result = namespace["patched_evaluate_hypnosis_completion"](1)

        assert result == 1
        assert cache.character_data[1].sp_flag.unconscious_h == 7, "已选类型的新催眠态不应被回滚"
        assert ("settle", 1, 5) not in calls, "未改写标记时不应额外重算异常标记"
    finally:
        restore()


def test_evaluate_completion_incomplete_result_untouched():
    """参数：无；返回：None；用途：验证催眠未完成(返回0)时包装不做任何状态干预。"""
    cache = make_cache(hypnosis_type=0, target_degree=10, target_unconscious=7, sanity_point=1)
    calls = []
    restore, _hypnosis_panel = install_fake_modules(cache, calls=calls)

    def fake_original(character_id):
        """参数：character_id(int)为目标角色ID；返回：int为完成判定；用途：模拟上游催眠度不足未完成。"""
        return 0

    try:
        namespace = load_component()
        namespace["_ORIGINAL_EVALUATE_HYPNOSIS_COMPLETION"] = fake_original

        result = namespace["patched_evaluate_hypnosis_completion"](1)

        assert result == 0
        assert cache.character_data[1].sp_flag.unconscious_h == 7
        assert calls == []
    finally:
        restore()


def main():
    """参数：无；返回：None；用途：直接运行全部本组件测试。"""
    test_manifest_has_hidden_hypnosis_hooks_only()
    test_hypnosis_target_talk_bypasses_unconscious_gate()
    test_sleep_target_talk_keeps_unconscious_gate()
    test_hypnosis_talk_gate_uses_current_premise_predicate()
    test_change_hypnosis_type_in_instruct_mode_applies_current_target()
    test_change_hypnosis_type_outside_instruct_mode_only_changes_default()
    test_change_hypnosis_type_air_blocked_room_draws_warning()
    test_change_hypnosis_type_air_degree_insufficient_stays_silent()
    test_hypnosis_one_manual_type_prompts_and_applies_current_target()
    test_hypnosis_one_default_type_does_not_prompt_again()
    test_hypnosis_one_does_not_apply_when_degree_is_not_enough()
    test_hypnosis_one_mind_control_ends_on_last_sanity_cost()
    test_hypnosis_one_preserves_active_hypnosis_when_original_clears_default_type()
    test_evaluate_completion_restores_active_hypnosis_for_default_type()
    test_evaluate_completion_keeps_new_flag_for_selected_type()
    test_evaluate_completion_incomplete_result_untouched()
    print("local_hypnosis_state_fix mod tests passed", flush=True)


if __name__ == "__main__":
    main()
