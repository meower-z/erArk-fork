"""普通效果接口测试。用标准库隔离加载生产函数，不启动界面或指令线程。"""

import ast
import datetime
import inspect
import sys
import unittest
from functools import wraps
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from Script.Core import constant_effect, game_type


def load_functions(path, namespace, predicate):
    """输入文件路径、命名空间和筛选函数；编译生产函数，返回函数名列表。"""
    tree = ast.parse((ROOT / path).read_text(encoding="utf-8"))
    nodes = [node for node in tree.body if isinstance(node, ast.FunctionDef) and predicate(node)]
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(ROOT / path), "exec"), namespace)
    return [node.name for node in nodes]


def ordinary_effect(node):
    """输入函数语法节点；返回是否注册为普通效果的布尔值。"""
    return any(isinstance(item, ast.Call) and isinstance(item.func, ast.Attribute) and item.func.attr == "add_settle_behavior_effect" for item in node.decorator_list)


class EffectInterfaceTest(unittest.TestCase):
    """验证真实注册函数、明确目标以及调用顺序。"""

    def setUp(self):
        """无输入和返回值；创建角色、注册表和隔离的生产函数环境。"""
        self.now = datetime.datetime(2026, 1, 1, 12)
        characters = {}
        for cid in range(4):
            character = game_type.Character()
            character.cid = cid
            character.target_character_id = (cid + 1) % 4
            character.behavior.start_time = self.now
            character.behavior.duration = 1
            character.event.skip_instruct_talk = True
            characters[cid] = character
        self.cache = SimpleNamespace(character_data=characters)
        self.constants = SimpleNamespace(settle_behavior_effect_data={}, Behavior=SimpleNamespace(TIME_STOP_OFF="time_stop_off"))
        self.config = SimpleNamespace(config_behavior_effect_data={}, config_behavior={}, config_event={})
        self.ns = {
            "cache": self.cache,
            "constant": self.constants,
            "constant_effect": constant_effect,
            "game_type": game_type,
            "datetime": datetime,
            "wraps": wraps,
            "game_config": self.config,
            "talk": SimpleNamespace(handle_talk=Mock()),
            "second_behavior": SimpleNamespace(check_second_effect=Mock()),
            "extra_exp_settle": Mock(),
            "game_time": SimpleNamespace(get_sub_date=lambda **kwargs: self.now),
            "_": lambda value: value,
        }
        load_functions("Script/Design/settle_behavior.py", self.ns, lambda node: node.name in {"add_settle_behavior_effect", "handle_instruct_data", "handle_event_data"})
        self.ns["settle_behavior"] = SimpleNamespace(add_settle_behavior_effect=self.ns["add_settle_behavior_effect"])
        self.effect_names = []
        for filename in ("default.py", "default_cloth.py", "item_effect.py"):
            self.effect_names.extend(load_functions("Script/Settle/" + filename, self.ns, ordinary_effect))
        self.effects = self.constants.settle_behavior_effect_data

    def test_registry_requires_explicit_target(self):
        """所有注册效果接受五个必填参数，且注册表保留原函数；无返回值。"""
        expected = ["character_id", "target_character_id", "add_time", "change_data", "now_time"]
        self.assertEqual(len(self.effects), len(self.effect_names))
        for effect in self.effects.values():
            with self.subTest(effect=effect.__name__):
                signature = inspect.signature(effect)
                self.assertEqual(list(signature.parameters), expected)
                self.assertTrue(all(param.default is inspect.Parameter.empty for param in signature.parameters.values()))
                self.assertFalse(hasattr(effect, "__wrapped__"))
                signature.bind(1, 2, 1, game_type.CharacterStatusChange(), self.now)
                with self.assertRaises(TypeError):
                    signature.bind(1, 1, game_type.CharacterStatusChange(), self.now)

    def test_registration_preserves_function(self):
        """注册器直接保存和返回原函数，不增加转发层；无返回值。"""
        effect = self.ns["handle_nothing"]
        registered = self.ns["add_settle_behavior_effect"](-1)(effect)
        self.assertIs(registered, effect)
        self.assertIs(self.effects[-1], effect)

    def test_equipment_uses_supplied_target(self):
        """装备开关只修改明确目标的指定槽位，不读取角色选择；无返回值。"""
        for item, slot in (("nipple_clamp", 0), ("clit_clamp", 1), ("vibrator", 2), ("anal_vibrator", 3)):
            for operation, active in (("on", True), ("off", False)):
                for duration in (0, 1):
                    with self.subTest(item=item, operation=operation, duration=duration):
                        for character in self.cache.character_data.values():
                            character.h_state.body_item = {key: [17, not active, 23] for key in range(5)}
                        # 执行者选择角色1，但本次明确作用于角色2。
                        self.cache.character_data[0].target_character_id = 1
                        self.ns[f"handle_target_{item}_{operation}"](0, 2, duration, game_type.CharacterStatusChange(), self.now)
                        for cid, character in self.cache.character_data.items():
                            for key, value in character.h_state.body_item.items():
                                expected = active if duration and cid == 2 and key == slot else not active
                                self.assertEqual(value, [17, expected, 23])
                        self.assertEqual(self.cache.character_data[0].target_character_id, 1)

    def test_explicit_player_target(self):
        """目标0表示玩家，不是回读当前选择的特殊值；无返回值。"""
        for character in self.cache.character_data.values():
            character.h_state.body_item = {2: [0, False]}
        self.ns["handle_target_vibrator_on"](1, 0, 1, game_type.CharacterStatusChange(), self.now)
        self.assertTrue(self.cache.character_data[0].h_state.body_item[2][1])
        self.assertFalse(self.cache.character_data[2].h_state.body_item[2][1])

    def run_target_switch(self, event=False, facility=False):
        """输入事件和设施分支标志；执行真实效果切换顺序并断言结果，无返回值。"""
        ids = constant_effect.BehaviorEffect
        sequence = [ids.TARGET_TO_PLAYER, ids.TARGET_VIBRATOR_ON]
        for character in self.cache.character_data.values():
            character.h_state.body_item = {2: [0, False]}
        changes = game_type.CharacterStatusChange()
        if event:
            self.config.config_event["example"] = SimpleNamespace(effect=[str(item) for item in sequence])
            self.ns["handle_event_data"]("example", 1, 1, changes, self.now)
        else:
            self.config.config_behavior_effect_data["example"] = sequence
            if facility:
                self.config.config_behavior["example"] = SimpleNamespace(tag=["工作"])
                self.effects[1751] = Mock()
            self.ns["handle_instruct_data"](1, "example", self.now, 1, changes)
            if facility:
                self.effects[1751].assert_called_once_with(1, 0, 1, changes, self.now)
        self.assertEqual(self.cache.character_data[1].target_character_id, 0)
        self.assertTrue(self.cache.character_data[0].h_state.body_item[2][1])
        self.assertFalse(self.cache.character_data[2].h_state.body_item[2][1])

    def test_instruction_target_switch(self):
        """普通效果间的主动目标切换对后续效果生效；无返回值。"""
        self.run_target_switch()

    def test_event_target_switch(self):
        """事件效果间的主动目标切换对后续效果生效；无返回值。"""
        self.run_target_switch(event=True)

    def test_facility_target_switch(self):
        """额外设施效果也接收调用时的目标；无返回值。"""
        self.run_target_switch(facility=True)

    def test_nested_call_uses_new_actors_target(self):
        """效果委派给另一执行者时，传入该执行者的目标；无返回值。"""
        self.cache.character_data[1].angry_point = 50
        effect = Mock(wraps=self.ns["handle_mood_to_good"])
        self.ns["handle_mood_to_good"] = effect
        changes = game_type.CharacterStatusChange()
        self.ns["handle_target_mood_to_good"](0, 1, 1, changes, self.now)
        effect.assert_called_once_with(1, 2, 1, changes, self.now)
        self.assertEqual(self.cache.character_data[1].angry_point, 0)

    def test_self_effect_does_not_need_target_state(self):
        """自身效果可以忽略目标参数，不访问目标角色；无返回值。"""
        self.cache.character_data[1].angry_point = 50
        self.ns["handle_mood_to_good"](1, 9999, 1, game_type.CharacterStatusChange(), self.now)
        self.assertEqual(self.cache.character_data[1].angry_point, 0)


if __name__ == "__main__":
    unittest.main()
