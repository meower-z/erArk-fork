from Script.Core import cache_control, game_type
from Script.Design import handle_premise


cache: game_type.Cache = cache_control.cache
"""游戏缓存数据"""


def clear_hypnosis_runtime_state(target_character_id: int) -> None:
    """
    清理目标角色依赖当前催眠状态的运行数据，并保留持久催眠数据与其他无意识来源。
    Keyword arguments:
    target_character_id -- 目标角色id
    Return arguments:
    None
    """
    target_character_data: game_type.Character = cache.character_data[target_character_id]

    # 仅清理催眠类无意识状态，保留睡眠、醉酒与时停
    if target_character_data.sp_flag.unconscious_h in {4, 5, 6, 7}:
        target_character_data.sp_flag.unconscious_h = 0

    # 清理依赖当前催眠状态的子状态
    target_character_data.hypnosis.increase_body_sensitivity = False
    target_character_data.hypnosis.blockhead = False
    target_character_data.hypnosis.active_h = False
    target_character_data.hypnosis.pain_as_pleasure = False
    target_character_data.hypnosis.roleplay = []
    target_character_data.h_state.npc_active_h = False

    # 重算意识相关异常标记
    handle_premise.settle_chara_unnormal_flag(target_character_id, 5)
    handle_premise.settle_chara_unnormal_flag(target_character_id, 6)
