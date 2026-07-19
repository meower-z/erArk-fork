# -*- coding: UTF-8 -*-
"""
群交寸止释放修复。
"""

HN_AI = "Script.Design.handle_npc_ai"
HN_AI_H = "Script.Design.handle_npc_ai_in_h"

BEHAVIOR_EFFECT_END_H_ADD_HPMP_MAX = 528
BEHAVIOR_EFFECT_GROUP_SEX_END_H_ADD_HPMP_MAX = 529
ORGASM_PART_PREFIX = {0: "s", 1: "b", 2: "c", 4: "v", 5: "a", 6: "u", 7: "w", 21: "m", 22: "f", 23: "h"}

_ORIGINAL_END_H_ADD_HPMP_MAX = None
_ORIGINAL_GROUP_SEX_END_H_ADD_HPMP_MAX = None


def _cache():
    """参数：无；返回：Cache对象；用途：获取当前游戏缓存。"""
    from Script.Core import cache_control

    return cache_control.cache


def _is_orgasm_batch_settling(character_id: int) -> bool:
    """参数：character_id(int)为角色ID；返回：bool为是否处于绝顶批处理；用途：避免批处理中触发疲劳睡眠清理。"""
    try:
        from Script.Design import second_behavior

        checker = getattr(second_behavior, "local_h_orgasm_batch_fix_is_settling", None)
        if checker is None:
            checker = getattr(second_behavior, "local_bugfix_is_orgasm_batch_settling", None)
        return bool(checker and checker(character_id))
    except Exception:
        return False


def _stable_dedupe_character_ids(character_ids):
    """参数：character_ids(iterable)为角色ID序列；返回：list为去重后ID；用途：按首次出现顺序稳定去重。"""
    result = []
    seen = set()
    for character_id in character_ids:
        if not character_id or character_id in seen:
            continue
        seen.add(character_id)
        result.append(character_id)
    return result


def _ordered_character_ids(character_ids):
    """参数：character_ids(iterable)为角色ID集合或列表；返回：list为稳定遍历序列；用途：集合按排序输出，列表保留顺序。"""
    if isinstance(character_ids, set):
        return sorted(character_ids)
    return list(character_ids)


def _collect_group_template_character_ids():
    """参数：无；返回：list为群交模板角色ID；用途：收集群交模板中的参与者。"""
    try:
        from Script.System.Sex_System import group_sex_panel

        return [character_id for character_id in _ordered_character_ids(group_sex_panel.count_group_sex_character_list()) if character_id]
    except Exception:
        return []


def _collect_scene_h_character_ids():
    """参数：无；返回：list为当前场景H状态角色ID；用途：补充当前场景中仍处于H状态的群交参与者。"""
    try:
        from Script.Design import map_handle

        cache_obj = _cache()
        pl_character_data = cache_obj.character_data.get(0)
        if pl_character_data is None:
            return []

        scene_path_str = map_handle.get_map_system_path_str_for_list(pl_character_data.position)
        scene_data = cache_obj.scene_data.get(scene_path_str)
        if scene_data is None:
            return []

        character_ids = []
        for character_id in _ordered_character_ids(scene_data.character_list):
            if not character_id or character_id not in cache_obj.character_data:
                continue
            character_data = cache_obj.character_data[character_id]
            if getattr(character_data.sp_flag, "is_h", False):
                character_ids.append(character_id)
        return character_ids
    except Exception:
        return []


def _collect_group_sex_participant_ids():
    """参数：无；返回：list为群交上下文角色ID；用途：合并模板参与者和当前场景H状态角色。"""
    return _stable_dedupe_character_ids(_collect_group_template_character_ids() + _collect_scene_h_character_ids())


def _has_pending_edge_count(character_data) -> bool:
    """参数：character_data(Character)为角色数据；返回：bool为是否存在未释放寸止计数；用途：筛选需要释放的参与者。"""
    edge_count = getattr(character_data.h_state, "orgasm_edge_count", {})
    return any(value != 0 for value in edge_count.values())


def _character_can_release_group_edge(character_id: int, group_context_ids) -> bool:
    """参数：character_id(int)为角色ID，group_context_ids(iterable)为群交上下文；返回：bool为是否可释放；用途：避免非群交角色误触释放。"""
    cache_obj = _cache()
    if character_id == 0 or character_id not in cache_obj.character_data:
        return False

    character_data = cache_obj.character_data[character_id]
    if getattr(character_data.h_state, "orgasm_edge", 0) != 1 or not _has_pending_edge_count(character_data):
        return False

    in_group_context = character_id in set(group_context_ids)
    in_h_state = bool(getattr(character_data.sp_flag, "is_h", False))
    return in_h_state or in_group_context


def _new_character_status_change():
    """参数：无；返回：CharacterStatusChange；用途：创建角色状态变化记录。"""
    from Script.Core import game_type

    return game_type.CharacterStatusChange()


def _get_release_change_data(character_id: int, owner_character_id: int, change_data):
    """参数：character_id(int)为释放角色，owner_character_id(int)为主记录角色，change_data(CharacterStatusChange)为变更对象；返回：object为写入对象；用途：把非主角色变更写入target_change。"""
    if character_id == owner_character_id:
        return change_data

    target_change_dict = getattr(change_data, "target_change", None)
    if target_change_dict is None:
        return change_data

    if character_id not in target_change_dict:
        try:
            from Script.Core import game_type

            target_change_dict[character_id] = game_type.TargetChange()
        except Exception:
            target_change_dict[character_id] = change_data
    return target_change_dict[character_id]


def _get_pending_edge_count_snapshot(character_data) -> dict:
    """参数：character_data(Character)为角色数据；返回：dict为未释放寸止计数；用途：释放前保存快照。"""
    return {state_id: count for state_id, count in getattr(character_data.h_state, "orgasm_edge_count", {}).items() if count != 0}


def _clear_orgasm_edge_count(character_data) -> None:
    """参数：character_data(Character)为角色数据；返回：None；用途：清空寸止计数。"""
    edge_count = getattr(character_data.h_state, "orgasm_edge_count", {})
    state_ids = set(edge_count.keys())
    try:
        from Script.Config import game_config

        for state_id, state_data in game_config.config_character_state.items():
            if getattr(state_data, "type", None) == 0:
                state_ids.add(state_id)
    except Exception:
        pass

    for state_id in state_ids:
        edge_count[state_id] = 0


def _is_release_second_behavior(second_behavior_id: str) -> bool:
    """参数：second_behavior_id(str)为二段行为ID；返回：bool为是否为绝顶释放行为；用途：筛选本次释放产生的二段行为。"""
    return "orgasm" in second_behavior_id


def _collect_new_release_second_behaviors(character_data, before_second_behavior: dict):
    """参数：character_data(Character)为角色数据，before_second_behavior(dict)为释放前二段；返回：list为新增释放二段；用途：无记录钩子时兜底收集新增绝顶行为。"""
    result = []
    for second_behavior_id, behavior_value in getattr(character_data, "second_behavior", {}).items():
        if behavior_value == 0:
            continue
        if before_second_behavior.get(second_behavior_id, 0) != 0:
            continue
        if _is_release_second_behavior(second_behavior_id):
            result.append(second_behavior_id)
    return result


def _remove_second_behavior_from_must_lists(character_data, second_behavior_id: str) -> None:
    """参数：character_data(Character)为角色数据，second_behavior_id(str)为二段ID；返回：None；用途：移除已处理的必须结算/显示标记。"""
    for list_name in ("must_settle_second_behavior_id_list", "must_show_second_behavior_id_list"):
        behavior_list = getattr(character_data, list_name, [])
        while second_behavior_id in behavior_list:
            behavior_list.remove(second_behavior_id)


def _clear_queued_orgasm_edge_second_behaviors(character_data) -> None:
    """参数：character_data(Character)为角色数据；返回：None；用途：清除释放后的旧寸止二段队列。"""
    second_behavior = getattr(character_data, "second_behavior", {})
    for part_prefix in ORGASM_PART_PREFIX.values():
        second_behavior_id = f"{part_prefix}_orgasm_edge"
        if second_behavior_id in second_behavior:
            second_behavior[second_behavior_id] = 0
        _remove_second_behavior_from_must_lists(character_data, second_behavior_id)


def _flush_release_second_behavior(character_id: int, change_data, second_behavior_id: str) -> None:
    """参数：character_id(int)为角色ID，change_data(CharacterStatusChange)为变更对象，second_behavior_id(str)为二段ID；返回：None；用途：同步结算释放产生的二段行为。"""
    from Script.Config import game_config
    from Script.Core import constant
    from Script.Design import settle_behavior, talk

    cache_obj = _cache()
    character_data = cache_obj.character_data[character_id]
    if character_data.second_behavior.get(second_behavior_id, 0) == 0:
        _remove_second_behavior_from_must_lists(character_data, second_behavior_id)
        return

    talk.handle_second_talk(character_id, second_behavior_id)
    if second_behavior_id in game_config.config_behavior_effect_data:
        for effect_id in game_config.config_behavior_effect_data[second_behavior_id]:
            if isinstance(effect_id, str) and "CVE" in effect_id:
                effect_all_value_list = effect_id.split("_")[1:]
                settle_behavior.handle_comprehensive_value_effect(character_id, effect_all_value_list, change_data)
            elif effect_id in constant.settle_second_behavior_effect_data:
                constant.settle_second_behavior_effect_data[effect_id](character_id, change_data)

    character_data.second_behavior[second_behavior_id] = 0
    _remove_second_behavior_from_must_lists(character_data, second_behavior_id)


def _stable_dedupe_second_behavior_ids(second_behavior_ids):
    """参数：second_behavior_ids(iterable)为二段ID序列；返回：list为稳定去重ID；用途：避免同一释放二段重复结算。"""
    result = []
    seen = set()
    for second_behavior_id in second_behavior_ids:
        if not second_behavior_id or second_behavior_id in seen:
            continue
        seen.add(second_behavior_id)
        result.append(second_behavior_id)
    return result


def _restore_preexisting_second_behavior(character_data, second_behavior_id: str, before_second_behavior: dict, before_must_settle: list, before_must_show: list) -> None:
    """参数：character_data(Character)为角色数据，second_behavior_id(str)为二段ID，before_second_behavior(dict)和列表为释放前状态；返回：None；用途：恢复释放前已有的同名二段。"""
    if before_second_behavior.get(second_behavior_id, 0) == 0:
        return

    character_data.second_behavior[second_behavior_id] = before_second_behavior[second_behavior_id]
    character_data.must_settle_second_behavior_id_list = before_must_settle.copy()
    character_data.must_show_second_behavior_id_list = before_must_show.copy()


def _flush_release_second_behavior_with_restore(character_id: int, change_data, second_behavior_id: str, before_second_behavior: dict, before_must_settle: list, before_must_show: list) -> None:
    """参数：同释放二段结算并附释放前状态；返回：None；用途：结算释放二段后恢复原有同名标记。"""
    character_data = _cache().character_data[character_id]
    _flush_release_second_behavior(character_id, change_data, second_behavior_id)
    _restore_preexisting_second_behavior(character_data, second_behavior_id, before_second_behavior, before_must_settle, before_must_show)


def _settle_edge_count_release(character_id: int, change_data, release_count: dict) -> None:
    """参数：character_id(int)为角色ID，change_data(CharacterStatusChange)为变更对象，release_count(dict)为本次释放计数；返回：None；用途：一次性结算待释放寸止并保留重复部位计数。"""
    from Script.Design import second_behavior

    cache_obj = _cache()
    character_data = cache_obj.character_data[character_id]
    before_second_behavior = dict(getattr(character_data, "second_behavior", {}))
    before_must_settle = list(getattr(character_data, "must_settle_second_behavior_id_list", []))
    before_must_show = list(getattr(character_data, "must_show_second_behavior_id_list", []))
    generated_second_behavior_ids = []
    original_get_second_behavior = getattr(second_behavior, "character_get_second_behavior", None)

    if original_get_second_behavior is not None:

        def record_release_second_behavior(record_character_id: int, second_behavior_id: str, reset: bool = False):
            if record_character_id == character_id and not reset and _is_release_second_behavior(second_behavior_id):
                generated_second_behavior_ids.append(second_behavior_id)
            return original_get_second_behavior(record_character_id, second_behavior_id, reset=reset)

        second_behavior.character_get_second_behavior = record_release_second_behavior

    try:
        second_behavior.orgasm_settle(character_id, change_data, un_count_orgasm_dict=release_count)
    finally:
        if original_get_second_behavior is not None:
            second_behavior.character_get_second_behavior = original_get_second_behavior

    if generated_second_behavior_ids:
        release_second_behavior_ids = _stable_dedupe_second_behavior_ids(generated_second_behavior_ids)
    else:
        release_second_behavior_ids = _collect_new_release_second_behaviors(character_data, before_second_behavior)

    owned_behavior_ids = set()
    owned_behavior_func = getattr(second_behavior, "local_h_orgasm_batch_fix_release_owned_behavior_ids", None)
    if callable(owned_behavior_func):
        owned_behavior_ids = owned_behavior_func(change_data, character_id)
    for second_behavior_id in release_second_behavior_ids:
        if second_behavior_id in owned_behavior_ids:
            continue
        _flush_release_second_behavior_with_restore(character_id, change_data, second_behavior_id, before_second_behavior, before_must_settle, before_must_show)


def _release_group_edge_for_character(character_id: int, change_data, owner_character_id: int = 0, group_context_ids=None) -> bool:
    """参数：character_id(int)为角色ID，change_data(CharacterStatusChange)为变更对象，owner_character_id(int)为主记录角色，group_context_ids(iterable)为群交上下文；返回：bool为是否释放；用途：释放单个群交参与者寸止计数。"""
    group_context_ids = group_context_ids or []
    if not _character_can_release_group_edge(character_id, group_context_ids):
        return False

    cache_obj = _cache()
    character_data = cache_obj.character_data[character_id]
    pending_edge_count = _get_pending_edge_count_snapshot(character_data)
    if not pending_edge_count:
        return False

    if not getattr(character_data.sp_flag, "is_h", False):
        _clear_orgasm_edge_count(character_data)
        _clear_queued_orgasm_edge_second_behaviors(character_data)
        if getattr(character_data.h_state, "orgasm_edge", 0) in (1, 2):
            character_data.h_state.orgasm_edge = 0
        return True

    release_change_data = _get_release_change_data(character_id, owner_character_id, change_data)

    character_data.h_state.orgasm_edge = 2
    try:
        _settle_edge_count_release(character_id, release_change_data, pending_edge_count)
    finally:
        _clear_orgasm_edge_count(character_data)
        _clear_queued_orgasm_edge_second_behaviors(character_data)
        if getattr(character_data.h_state, "orgasm_edge", 0) == 2:
            character_data.h_state.orgasm_edge = 0

    return True


def _release_group_edge_for_characters(character_ids, change_data=None, owner_character_id: int = 0, group_context_ids=None):
    """参数：character_ids(iterable)为角色ID，change_data(CharacterStatusChange)为变更对象，owner_character_id(int)为主记录角色，group_context_ids(iterable)为群交上下文；返回：list为实际释放ID；用途：批量释放寸止计数。"""
    if change_data is None:
        change_data = _new_character_status_change()

    group_context_ids = group_context_ids or character_ids
    released_character_ids = []
    for character_id in _stable_dedupe_character_ids(character_ids):
        if _release_group_edge_for_character(character_id, change_data, owner_character_id, group_context_ids):
            released_character_ids.append(character_id)
    return released_character_ids


def _is_group_sex_npc_hp_0_end(character_id: int) -> bool:
    """参数：character_id(int)为角色ID；返回：bool为是否群交NPC体力耗尽退出；用途：识别单个NPC离场释放时机。"""
    from Script.Core import constant

    cache_obj = _cache()
    if character_id not in cache_obj.character_data:
        return False
    behavior_id = cache_obj.character_data[character_id].behavior.behavior_id
    return behavior_id == getattr(constant.Behavior, "GROUP_SEX_NPC_HP_0_END", "group_sex_npc_hp_0_end")


def _release_group_sex_to_h_leavers(pre_transition_character_ids, owner_character_id: int = 0):
    """参数：pre_transition_character_ids(iterable)为转换前参与者，owner_character_id(int)为主记录角色；返回：list为释放ID；用途：群交转单人H时释放离开群交上下文的角色。"""
    from Script.Core import constant

    cache_obj = _cache()
    pl_character_data = cache_obj.character_data.get(0)
    if pl_character_data is None:
        return []

    if pl_character_data.behavior.behavior_id != getattr(constant.Behavior, "GROUP_SEX_TO_H", "group_sex_to_h"):
        return []

    continuing_target_id = pl_character_data.target_character_id
    leaver_ids = [character_id for character_id in pre_transition_character_ids if character_id != continuing_target_id]
    return _release_group_edge_for_characters(
        leaver_ids,
        _new_character_status_change(),
        owner_character_id=owner_character_id,
        group_context_ids=pre_transition_character_ids,
    )


def _group_sex_mode_is_on(character_id: int) -> bool:
    """参数：character_id(int)为角色ID；返回：bool为群交模式是否开启；用途：兼容前提系统失败时的缓存标记。"""
    try:
        from Script.Design import handle_premise

        return bool(handle_premise.handle_group_sex_mode_on(character_id))
    except Exception:
        return bool(getattr(_cache(), "group_sex_mode", False))


def _should_release_before_unconscious_recovery(character_id: int) -> bool:
    """参数：character_id(int)为角色ID；返回：bool为恢复无意识前是否应释放；用途：避免模板清空前丢失群交寸止。"""
    cache_obj = _cache()
    character_data = cache_obj.character_data.get(character_id)
    if character_data is None:
        return False

    target_character_id = getattr(character_data, "target_character_id", character_id)
    target_data = cache_obj.character_data.get(target_character_id)
    if target_data is None or getattr(target_data.sp_flag, "unconscious_h", 0) == 0:
        return False

    return _group_sex_mode_is_on(character_id)


def patched_handle_group_sex_end_h_add_hpmp_max(character_id: int, add_time: int, change_data, now_time):
    """参数：同原效果；返回：object为原效果结果；用途：群交结束上限结算前释放所有参与者寸止。"""
    if add_time:
        participant_ids = _collect_group_sex_participant_ids()
        _release_group_edge_for_characters(participant_ids, change_data, owner_character_id=character_id, group_context_ids=participant_ids)
    return _ORIGINAL_GROUP_SEX_END_H_ADD_HPMP_MAX(character_id, add_time, change_data, now_time)


def patched_handle_end_h_add_hpmp_max(character_id: int, add_time: int, change_data, now_time):
    """参数：同原效果；返回：object为原效果结果；用途：群交NPC单人退出上限结算前释放该NPC寸止。"""
    if add_time and _is_group_sex_npc_hp_0_end(character_id):
        participant_ids = _stable_dedupe_character_ids(_collect_group_sex_participant_ids() + [character_id])
        _release_group_edge_for_character(character_id, change_data, owner_character_id=character_id, group_context_ids=participant_ids)
    return _ORIGINAL_END_H_ADD_HPMP_MAX(character_id, add_time, change_data, now_time)


def patched_recover_from_unconscious_h(character_id: int, info_text: str = ""):
    """参数：character_id(int)为角色ID，info_text(str)为恢复提示；返回：object为原函数返回值；用途：无意识恢复清空群交模板前释放寸止。"""
    if _should_release_before_unconscious_recovery(character_id):
        participant_ids = _collect_group_sex_participant_ids()
        _release_group_edge_for_characters(
            participant_ids,
            _new_character_status_change(),
            owner_character_id=character_id,
            group_context_ids=participant_ids,
        )
    return call_original(HN_AI_H, "recover_from_unconscious_h", character_id, info_text)


def patched_judge_character_tired_sleep(character_id: int):
    """参数：character_id(int)为角色ID；返回：object为原函数返回值；用途：疲劳/睡眠清理前处理群交转单人H离场与批处理保护。"""
    cache_obj = _cache()
    pre_group_sex_character_ids = []
    if character_id and character_id in cache_obj.character_data and _group_sex_mode_is_on(character_id):
        pre_group_sex_character_ids = _collect_group_sex_participant_ids()

    if character_id in cache_obj.character_data:
        character_data = cache_obj.character_data[character_id]
        if _is_orgasm_batch_settling(character_id) or (character_id == 0 and _is_orgasm_batch_settling(character_data.target_character_id)):
            return

    from Script.Design import attr_calculation, character_behavior, handle_premise

    should_rejudge_status = False
    if character_id and character_id in cache_obj.character_data:
        character_data = cache_obj.character_data[character_id]
        if (character_data.sp_flag.is_h or character_data.sp_flag.is_follow) and handle_premise.handle_group_sex_mode_on(character_id):
            should_rejudge_status = (
                character_data.hit_point <= 1
                or character_data.sp_flag.tired
                or attr_calculation.get_tired_level(character_data.tired_point) >= 2
            )

    result = call_original(HN_AI, "judge_character_tired_sleep", character_id)
    if pre_group_sex_character_ids:
        _release_group_sex_to_h_leavers(pre_group_sex_character_ids, owner_character_id=0)
    # 仅当原逻辑本次确实分配了群交退出行为（事后状态）才补结算：
    # 补结算的目的只在于让新分配的 GROUP_SEX_NPC_HP_0_END 的效果链先于
    # H无意识判定覆盖行为前完成；疲劳跟随者走上游跟随分支时不产生新行为，
    # 事前条件下的无条件补结算会对其造成一次多余的行为中途结算。
    if should_rejudge_status and _is_group_sex_npc_hp_0_end(character_id):
        character_behavior.judge_character_status(character_id)
    return result


def _patch_group_sex_edge_release_effects() -> None:
    """参数：无；返回：None；用途：安装群交寸止释放相关行为效果包装。"""
    global _ORIGINAL_END_H_ADD_HPMP_MAX, _ORIGINAL_GROUP_SEX_END_H_ADD_HPMP_MAX

    from Script.Core import constant
    from Script.Settle import default as settle_default

    current_group_end_effect = constant.settle_behavior_effect_data.get(
        BEHAVIOR_EFFECT_GROUP_SEX_END_H_ADD_HPMP_MAX,
        settle_default.handle_group_sex_end_h_add_hpmp_max,
    )
    if _ORIGINAL_GROUP_SEX_END_H_ADD_HPMP_MAX is None:
        _ORIGINAL_GROUP_SEX_END_H_ADD_HPMP_MAX = getattr(
            current_group_end_effect,
            "_local_group_edge_release_original",
            getattr(current_group_end_effect, "_local_bugfix_original", current_group_end_effect),
        )
    patched_handle_group_sex_end_h_add_hpmp_max._local_group_edge_release_original = _ORIGINAL_GROUP_SEX_END_H_ADD_HPMP_MAX
    constant.settle_behavior_effect_data[BEHAVIOR_EFFECT_GROUP_SEX_END_H_ADD_HPMP_MAX] = patched_handle_group_sex_end_h_add_hpmp_max
    settle_default.handle_group_sex_end_h_add_hpmp_max = patched_handle_group_sex_end_h_add_hpmp_max

    current_end_h_effect = constant.settle_behavior_effect_data.get(BEHAVIOR_EFFECT_END_H_ADD_HPMP_MAX, settle_default.handle_end_h_add_hpmp_max)
    if _ORIGINAL_END_H_ADD_HPMP_MAX is None:
        _ORIGINAL_END_H_ADD_HPMP_MAX = getattr(
            current_end_h_effect,
            "_local_group_edge_release_original",
            getattr(current_end_h_effect, "_local_bugfix_original", current_end_h_effect),
        )
    patched_handle_end_h_add_hpmp_max._local_group_edge_release_original = _ORIGINAL_END_H_ADD_HPMP_MAX
    constant.settle_behavior_effect_data[BEHAVIOR_EFFECT_END_H_ADD_HPMP_MAX] = patched_handle_end_h_add_hpmp_max
    settle_default.handle_end_h_add_hpmp_max = patched_handle_end_h_add_hpmp_max


_patch_group_sex_edge_release_effects()
