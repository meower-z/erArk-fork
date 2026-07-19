# -*- coding: UTF-8 -*-
"""
催眠状态持久化与口上门禁修复。
"""

BEHAVIOR_EFFECT_HYPNOSIS_ONE = 1211
HYPNOSIS_UNCONSCIOUS_FLAGS = {4, 5, 6, 7}

_ORIGINAL_HYPNOSIS_ONE_EFFECT = None
_ORIGINAL_GET_WEIGHT_FROM_PREMISE_DICT = None
_ORIGINAL_CHANGE_HYPNOSIS_TYPE = None
_ORIGINAL_EVALUATE_HYPNOSIS_COMPLETION = None


def _cache():
    """参数：无；返回：Cache对象；用途：获取当前游戏缓存。"""
    from Script.Core import cache_control

    return cache_control.cache


def _manual_hypnosis_type_degree_threshold(hypnosis_panel) -> int:
    """参数：hypnosis_panel(module)为催眠面板模块；返回：int为手动选择阈值；用途：取得手动催眠类型选择的最低催眠度。"""
    try:
        return hypnosis_panel.game_config.config_hypnosis_type[0].hypnosis_degree
    except Exception:
        return 50


def _hypnosis_degree_need_for_current_type(hypnosis_panel, hypnosis_type: int) -> int:
    """参数：hypnosis_panel(module)为催眠面板模块，hypnosis_type(int)为催眠类型；返回：int为需要的催眠度；用途：取得当前催眠类型阈值。"""
    try:
        return hypnosis_panel.game_config.config_hypnosis_type[hypnosis_type].hypnosis_degree
    except Exception:
        return _manual_hypnosis_type_degree_threshold(hypnosis_panel)


def _apply_current_hypnosis_state(target_character_id: int) -> int:
    """参数：target_character_id(int)为目标角色ID；返回：int为是否成功套用状态；用途：按博士当前催眠类型修正目标催眠无意识状态。"""
    from Script.Design import handle_premise, map_handle
    from Script.UI.Panel import hypnosis_panel

    cache_obj = _cache()
    pl_character_data = cache_obj.character_data.get(0)
    target_character_data = cache_obj.character_data.get(target_character_id)
    if pl_character_data is None or target_character_data is None or target_character_id == 0:
        return 0

    hypnosis_type = getattr(getattr(pl_character_data, "pl_ability", None), "hypnosis_type", 0)
    if hypnosis_type == 0 or hypnosis_type not in hypnosis_panel.game_config.config_hypnosis_type:
        return 0

    hypnosis_degree = getattr(getattr(target_character_data, "hypnosis", None), "hypnosis_degree", 0)
    hypnosis_degree_need = _hypnosis_degree_need_for_current_type(hypnosis_panel, hypnosis_type)
    if hypnosis_degree < hypnosis_degree_need:
        return 0

    if hypnosis_type == 2:
        scene_path = map_handle.get_map_system_path_str_for_list(pl_character_data.position)
        scene_data = getattr(cache_obj, "scene_data", {}).get(scene_path)
        if scene_data is None or scene_data.close_type != 1:
            return 0
        if scene_data.close_flag == 0:
            scene_data.close_flag = scene_data.close_type
        pl_character_data.pl_ability.air_hypnosis_position = pl_character_data.position

    target_character_data.sp_flag.unconscious_h = hypnosis_type + 3
    handle_premise.settle_chara_unnormal_flag(target_character_id, 5)
    handle_premise.settle_chara_unnormal_flag(target_character_id, 6)
    return 1


def _is_active_hypnosis_flag(unconscious_h: int) -> bool:
    """参数：unconscious_h(int)为无意识标记；返回：bool为是否为催眠类无意识；用途：统一判断催眠生效标记。"""
    return unconscious_h in HYPNOSIS_UNCONSCIOUS_FLAGS


def _air_hypnosis_blocked_by_room(pl_character_data) -> bool:
    """参数：pl_character_data(Character)为玩家角色；返回：bool为当前地点是否因不可锁门而阻止空气催眠；用途：区分空气催眠失败原因以给出正确提示。"""
    try:
        from Script.Design import map_handle

        cache_obj = _cache()
        scene_path = map_handle.get_map_system_path_str_for_list(pl_character_data.position)
        scene_data = getattr(cache_obj, "scene_data", {}).get(scene_path)
        return scene_data is not None and scene_data.close_type != 1
    except Exception:
        return False


def _resettle_unnormal_flags(character_id: int) -> None:
    """参数：character_id(int)为角色ID；返回：None；用途：修改无意识标记后重算异常标记位5/6，避免前提缓存滞留旧值。"""
    from Script.Design import handle_premise

    handle_premise.settle_chara_unnormal_flag(character_id, 5)
    handle_premise.settle_chara_unnormal_flag(character_id, 6)


def patched_evaluate_hypnosis_completion(character_id: int):
    """参数：character_id(int)为目标角色ID；返回：int为催眠完成判定结果；用途：默认催眠类型为无(0)时保留目标既有的催眠无意识状态。

    上游 evaluate_hypnosis_completion 在催眠完成且博士当前类型为0时会把
    sp_flag.unconscious_h 置0，误清此前手动/一次性套用的催眠态4/5/6/7。
    单人催眠(1211)与群体催眠(1212)都调用该函数，在源头包装可同时覆盖两条路径。
    """
    cache_obj = _cache()
    target_character_data = cache_obj.character_data.get(character_id)
    old_unconscious_h = getattr(getattr(target_character_data, "sp_flag", None), "unconscious_h", 0)

    result = _ORIGINAL_EVALUATE_HYPNOSIS_COMPLETION(character_id)

    if result != 1 or target_character_data is None or not _is_active_hypnosis_flag(old_unconscious_h):
        return result
    pl_character_data = cache_obj.character_data.get(0)
    hypnosis_type = getattr(getattr(pl_character_data, "pl_ability", None), "hypnosis_type", 0) if pl_character_data is not None else 0
    if hypnosis_type == 0 and target_character_data.sp_flag.unconscious_h == 0:
        target_character_data.sp_flag.unconscious_h = old_unconscious_h
        _resettle_unnormal_flags(character_id)
    return result


def _clear_hypnosis_runtime_flags(target_character_data) -> None:
    """参数：target_character_data(Character)为目标角色；返回：None；用途：催眠结束时清除依赖当前催眠态的短期子状态。"""
    hypnosis_data = getattr(target_character_data, "hypnosis", None)
    if hypnosis_data is None:
        return
    if hasattr(hypnosis_data, "increase_body_sensitivity"):
        hypnosis_data.increase_body_sensitivity = False
    if hasattr(hypnosis_data, "blockhead"):
        hypnosis_data.blockhead = False
    if hasattr(hypnosis_data, "active_h"):
        hypnosis_data.active_h = False
    h_state_data = getattr(target_character_data, "h_state", None)
    if h_state_data is not None and hasattr(h_state_data, "npc_active_h"):
        h_state_data.npc_active_h = 0
    if hasattr(hypnosis_data, "pain_as_pleasure"):
        hypnosis_data.pain_as_pleasure = False
    if hasattr(hypnosis_data, "roleplay"):
        hypnosis_data.roleplay = []


def _should_prompt_manual_hypnosis_type(character_id: int) -> bool:
    """参数：character_id(int)为施术者ID；返回：bool为是否应弹出手动类型选择；用途：默认无催眠类型时让玩家选择本次效果。"""
    cache_obj = _cache()
    character_data = cache_obj.character_data.get(character_id)
    if character_data is None or getattr(character_data, "dead", False):
        return False

    pl_ability = getattr(character_data, "pl_ability", None)
    if getattr(pl_ability, "hypnosis_type", 0) != 0:
        return False

    if getattr(character_data, "sanity_point", 1) == 0:
        return False

    target_character_id = getattr(character_data, "target_character_id", 0)
    if not target_character_id or target_character_id not in cache_obj.character_data:
        return False

    target_character_data = cache_obj.character_data[target_character_id]
    if getattr(getattr(target_character_data, "sp_flag", None), "unconscious_h", 0):
        return False

    from Script.UI.Panel import hypnosis_panel

    hypnosis_degree = getattr(getattr(target_character_data, "hypnosis", None), "hypnosis_degree", 0)
    return hypnosis_degree >= _manual_hypnosis_type_degree_threshold(hypnosis_panel)


def _draw_manual_hypnosis_type_selector(character_id: int) -> None:
    """参数：character_id(int)为施术者ID；返回：None；用途：绘制手动催眠类型选择并保持默认类型仍为无。"""
    from Script.UI.Panel import hypnosis_panel

    cache_obj = _cache()
    character_data = cache_obj.character_data[character_id]
    old_hypnosis_type = character_data.pl_ability.hypnosis_type
    now_panel = hypnosis_panel.Chose_Hypnosis_Type_Panel(hypnosis_panel.window_width, True)
    now_panel.draw()
    if old_hypnosis_type == 0:
        character_data.pl_ability.hypnosis_type = old_hypnosis_type


def _target_is_in_hypnosis_unconscious_state(character_id: int) -> bool:
    """参数：character_id(int)为说话者ID；返回：bool为其目标是否处于催眠类无意识；用途：限定口上门禁绕过范围。"""
    try:
        from Script.Design import handle_premise

        predicate = getattr(handle_premise, "handle_t_unconscious_hypnosis_flag", None)
        if predicate is not None:
            return bool(predicate(character_id))

        cache_obj = _cache()
        character_data = cache_obj.character_data.get(character_id)
        if character_data is None:
            return False

        target_character_id = getattr(character_data, "target_character_id", 0)
        target_data = cache_obj.character_data.get(target_character_id)
        if target_data is None:
            return False

        return getattr(getattr(target_data, "sp_flag", None), "unconscious_h", 0) in HYPNOSIS_UNCONSCIOUS_FLAGS
    except Exception:
        return False


def patched_get_weight_from_premise_dict(talk_premise_dict: set, character_id: int, calculated_premise_dict: dict, weight_all_to_1_flag: bool = False, unconscious_pass_flag: bool = False):
    """参数：talk_premise_dict(set)为口上前提，character_id(int)为说话者ID，calculated_premise_dict(dict)为缓存前提；返回：tuple为权重与缓存；用途：催眠态口上不被通用无意识门禁吞掉。"""
    if not unconscious_pass_flag and _target_is_in_hypnosis_unconscious_state(character_id):
        unconscious_pass_flag = True
    return _ORIGINAL_GET_WEIGHT_FROM_PREMISE_DICT(
        talk_premise_dict,
        character_id,
        calculated_premise_dict,
        weight_all_to_1_flag=weight_all_to_1_flag,
        unconscious_pass_flag=unconscious_pass_flag,
    )


def patched_handle_hypnosis_one(character_id: int, add_time: int, change_data, now_time):
    """参数：character_id(int)为施术者ID，add_time(int)为结算值，change_data(CharacterStatusChange)为变更对象，now_time(datetime)为当前时间；返回：object为原结算返回值；用途：单人催眠后幂等校正当前目标催眠状态。"""
    cache_obj = _cache()
    character_data = cache_obj.character_data.get(character_id)
    target_character_id = getattr(character_data, "target_character_id", 0) if character_data is not None else 0
    target_character_data = cache_obj.character_data.get(target_character_id)
    old_unconscious_h = getattr(getattr(target_character_data, "sp_flag", None), "unconscious_h", 0)

    result = _ORIGINAL_HYPNOSIS_ONE_EFFECT(character_id, add_time, change_data, now_time)
    if not add_time:
        return result

    if character_data is None:
        return result

    if target_character_data is not None:
        now_unconscious_h = getattr(getattr(target_character_data, "sp_flag", None), "unconscious_h", 0)
        if getattr(character_data, "sanity_point", 1) == 0:
            if _is_active_hypnosis_flag(now_unconscious_h):
                target_character_data.sp_flag.unconscious_h = 0
                # 本组件改写标记后需同步重算异常标记位，原逻辑清零路径由上游自带重算
                _resettle_unnormal_flags(target_character_id)
            _clear_hypnosis_runtime_flags(target_character_data)
            return result
        if _is_active_hypnosis_flag(old_unconscious_h) and now_unconscious_h == 0:
            target_character_data.sp_flag.unconscious_h = old_unconscious_h
            _resettle_unnormal_flags(target_character_id)
            return result

    if _apply_current_hypnosis_state(target_character_id):
        return result

    if _should_prompt_manual_hypnosis_type(character_id):
        _draw_manual_hypnosis_type_selector(character_id)
    return result


def patched_change_hypnosis_type(self, hypnosis_type_cid):
    """参数：self(Chose_Hypnosis_Type_Panel)为面板实例，hypnosis_type_cid(int)为催眠类型；返回：None；用途：切换催眠模式时在指令模式下立即套用当前目标。"""
    from Script.UI.Panel import hypnosis_panel

    pl_character_data = hypnosis_panel.cache.character_data[0]
    pl_character_data.pl_ability.hypnosis_type = hypnosis_type_cid
    target_data = hypnosis_panel.cache.character_data[pl_character_data.target_character_id]
    line_draw = hypnosis_panel.draw.LineDraw("-", self.width)
    line_draw.draw()

    if hypnosis_type_cid > 0:
        hypnosis_type_name = hypnosis_panel.game_config.config_hypnosis_type[hypnosis_type_cid].name
        now_draw = hypnosis_panel.draw.WaitDraw()
        draw_text = hypnosis_panel._("\n已切换为{0}催眠模式\n\n").format(hypnosis_type_name)
        now_draw.style = "pink"
        now_draw.text = draw_text
        now_draw.draw()
        if self.instruct_flag and pl_character_data.target_character_id:
            if _apply_current_hypnosis_state(pl_character_data.target_character_id) == 0:
                # 与上游一致给出失败原因反馈：空气催眠要求可锁门地点（hypnosis_panel 原路径会绘制该警告）。
                # 仅在锁门条件确为失败原因时提示，催眠度不足时沿用静默（后续施术会给出不足提示）。
                if hypnosis_type_cid == 2 and _air_hypnosis_blocked_by_room(pl_character_data):
                    now_draw = hypnosis_panel.draw.WaitDraw()
                    now_draw.text = hypnosis_panel._("\n当前地点不能锁门，无法进行空气催眠\n")
                    now_draw.draw()
                return
            now_draw = hypnosis_panel.draw.WaitDraw()
            now_draw.style = "pink"
            if hypnosis_type_cid == 1:
                draw_text = hypnosis_panel._("\n{0}会理所当然地接受{1}的不合理行为了\n\n").format(target_data.name, pl_character_data.name)
                now_draw.text = draw_text
                now_draw.draw()
            elif hypnosis_type_cid == 2:
                draw_text = hypnosis_panel._("\n{0}会把{1}视为空气了\n\n").format(target_data.name, pl_character_data.name)
                now_draw.text = draw_text
                now_draw.draw()
            elif hypnosis_type_cid == 3:
                draw_text = hypnosis_panel._("\n{0}可以随意地操纵{1}的身体了\n\n").format(pl_character_data.name, target_data.name)
                now_draw.text = draw_text
                now_draw.draw()
                self.body_or_mind_control_option(0)
            elif hypnosis_type_cid == 4:
                draw_text = hypnosis_panel._("\n{0}可以向{1}的潜意识灌输指令了\n\n").format(pl_character_data.name, target_data.name)
                now_draw.text = draw_text
                now_draw.draw()
                self.body_or_mind_control_option(1)


def _patch_hypnosis_one_effect() -> None:
    """参数：无；返回：None；用途：安装单人催眠结算补丁。"""
    global _ORIGINAL_HYPNOSIS_ONE_EFFECT

    from Script.Core import constant
    from Script.Settle import default as settle_default

    current_effect = constant.settle_behavior_effect_data.get(BEHAVIOR_EFFECT_HYPNOSIS_ONE, settle_default.handle_hypnosis_one)
    if _ORIGINAL_HYPNOSIS_ONE_EFFECT is None:
        _ORIGINAL_HYPNOSIS_ONE_EFFECT = getattr(
            current_effect,
            "_local_hypnosis_state_original",
            getattr(current_effect, "_local_bugfix_original", current_effect),
        )
    patched_handle_hypnosis_one._local_hypnosis_state_original = _ORIGINAL_HYPNOSIS_ONE_EFFECT
    constant.settle_behavior_effect_data[BEHAVIOR_EFFECT_HYPNOSIS_ONE] = patched_handle_hypnosis_one
    settle_default.handle_hypnosis_one = patched_handle_hypnosis_one


def _patch_get_weight_from_premise_dict() -> None:
    """参数：无；返回：None；用途：安装催眠态口上前提权重包装。"""
    global _ORIGINAL_GET_WEIGHT_FROM_PREMISE_DICT

    from Script.Design import handle_premise

    current_func = handle_premise.get_weight_from_premise_dict
    if _ORIGINAL_GET_WEIGHT_FROM_PREMISE_DICT is None:
        _ORIGINAL_GET_WEIGHT_FROM_PREMISE_DICT = getattr(
            current_func,
            "_local_hypnosis_state_original",
            getattr(current_func, "_local_bugfix_original", current_func),
        )
    patched_get_weight_from_premise_dict._local_hypnosis_state_original = _ORIGINAL_GET_WEIGHT_FROM_PREMISE_DICT
    handle_premise.get_weight_from_premise_dict = patched_get_weight_from_premise_dict


def _patch_hypnosis_panel() -> None:
    """参数：无；返回：None；用途：安装切换催眠模式面板补丁。"""
    global _ORIGINAL_CHANGE_HYPNOSIS_TYPE

    from Script.UI.Panel import hypnosis_panel

    current_method = hypnosis_panel.Chose_Hypnosis_Type_Panel.change_hypnosis_type
    if _ORIGINAL_CHANGE_HYPNOSIS_TYPE is None:
        _ORIGINAL_CHANGE_HYPNOSIS_TYPE = getattr(
            current_method,
            "_local_hypnosis_state_original",
            getattr(current_method, "_local_bugfix_original", current_method),
        )
    patched_change_hypnosis_type._local_hypnosis_state_original = _ORIGINAL_CHANGE_HYPNOSIS_TYPE
    hypnosis_panel.Chose_Hypnosis_Type_Panel.change_hypnosis_type = patched_change_hypnosis_type


def _patch_evaluate_hypnosis_completion() -> None:
    """参数：无；返回：None；用途：安装催眠完成判定包装，使单人(1211)与群体(1212)催眠共用既有催眠态保留逻辑。"""
    global _ORIGINAL_EVALUATE_HYPNOSIS_COMPLETION

    from Script.UI.Panel import hypnosis_panel

    current_func = getattr(hypnosis_panel, "evaluate_hypnosis_completion", None)
    if current_func is None:
        return
    if _ORIGINAL_EVALUATE_HYPNOSIS_COMPLETION is None:
        _ORIGINAL_EVALUATE_HYPNOSIS_COMPLETION = getattr(
            current_func,
            "_local_hypnosis_state_original",
            getattr(current_func, "_local_bugfix_original", current_func),
        )
    patched_evaluate_hypnosis_completion._local_hypnosis_state_original = _ORIGINAL_EVALUATE_HYPNOSIS_COMPLETION
    hypnosis_panel.evaluate_hypnosis_completion = patched_evaluate_hypnosis_completion


def _install_registry_patches() -> None:
    """参数：无；返回：None；用途：安装催眠状态相关运行时补丁。"""
    _patch_hypnosis_panel()
    _patch_hypnosis_one_effect()
    _patch_get_weight_from_premise_dict()
    _patch_evaluate_hypnosis_completion()


_install_registry_patches()
