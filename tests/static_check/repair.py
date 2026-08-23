# -*- coding: UTF-8 -*-
"""
静态检查系统 - 载入存档时的保守自动修复
在载入存档完成后扫描已知的"逻辑不合法状态"，用保守策略修复（越界拉回、重复去重、悬空引用清除、
派生缓存按源数据重算），使刚读取的存档不再触发对应检查，防止祖传脏数据在修复前一直存在且永不自愈。

契约：
- 修复策略逐条挂在检查上（register_repair），只为语义清晰、有唯一保守答案的检查提供修复；
  语义模糊的检查宁可不修（检查级去重保证不修也只记一条日志）。
- 每条修复必须留痕：修了什么对象的什么字段、修复前值与修复后值，逐条写入static_check_error.log。
- 修复绝不让载入失败：每条修复规则独立try/except，修不动就跳过保留原样；入口函数永不向调用方抛异常。
- cache.debug_mode开启时全部跳过（与相应检查的debug豁免一致，debug面板改出的值视为有意为之）。
"""
from typing import Callable, Dict, List, Tuple

from Script.Config import game_config

from tests.static_check import check_log

# 修复注册表：check_id -> (修复名, 修复函数)。修复函数接收cache，返回修复记录列表（每条含check_id/target/field/old_value/new_value）
_repair_registry: Dict[str, Tuple[str, Callable[[object], List[dict]]]] = {}


def register_repair(check_id: str, repair_name: str):
    """
    参数:
        check_id (str): 该修复对应的检查id（与check_registry中注册的检查一一对应）
        repair_name (str): 修复策略的简短中文名
    返回值:
        Callable: 装饰器
    功能:
        将一个接收cache参数的修复函数注册到修复注册表；重复注册同一check_id抛ValueError（导入期即暴露配置错误）
    """

    def decorator(func: Callable[[object], List[dict]]):
        if check_id in _repair_registry:
            raise ValueError(f"重复注册修复: {check_id}")
        _repair_registry[check_id] = (repair_name, func)
        return func

    return decorator


def _record(check_id: str, target: str, field: str, old_value, new_value) -> dict:
    """
    参数:
        check_id (str): 检查id
        target (str): 修复对象描述（如"角色69(塔佳娜)"）
        field (str): 被修复的字段路径
        old_value: 修复前的值
        new_value: 修复后的值
    返回值:
        dict: 标准修复记录
    功能:
        构造一条留痕用的修复记录，旧值新值都完整保留
    """
    return {"check_id": check_id, "target": target, "field": field, "old_value": old_value, "new_value": new_value}


def _chara_label(cid, chara) -> str:
    """
    参数:
        cid: 角色id
        chara: 角色对象
    返回值:
        str: "角色id(名字)"形式的描述
    功能:
        构造修复记录中的角色描述文本
    """
    return f"角色{cid}({getattr(chara, 'name', '?')})"


@register_repair("NUM-27", "疲劳/饥饿/熟睡/醉酒越界拉回")
def repair_fatigue_family_range(cache) -> List[dict]:
    """
    参数:
        cache: 当前游戏缓存对象
    返回值:
        List[dict]: 修复记录列表
    功能:
        与NUM-27（含MIND-24的sleep_point子集）同语义：tired_point/hunger_point/sleep_point/drunk_point
        必须是[0,上界]内的int。非int（含None/bool）置0，越界钳制到边界
    """
    bounds = {"tired_point": 160, "hunger_point": 240, "sleep_point": 100, "drunk_point": 100}
    records = []
    for cid, chara in cache.character_data.items():
        for field, upper in bounds.items():
            v = getattr(chara, field, None)
            if type(v) is int and 0 <= v <= upper:
                continue
            new_v = min(max(v, 0), upper) if type(v) is int else 0
            setattr(chara, field, new_v)
            records.append(_record("NUM-27", _chara_label(cid, chara), field, v, new_v))
    return records


@register_repair("SUPP-05", "愤怒值下界钳制")
def repair_angry_point_lower_bound(cache) -> List[dict]:
    """
    参数:
        cache: 当前游戏缓存对象
    返回值:
        List[dict]: 修复记录列表
    功能:
        与SUPP-05同语义：angry_point必须是>=0的int。非int置0，负值拉回0
    """
    records = []
    for cid, chara in cache.character_data.items():
        v = getattr(chara, "angry_point", 0)
        if type(v) is int and v >= 0:
            continue
        new_v = max(v, 0) if type(v) is int else 0
        chara.angry_point = new_v
        records.append(_record("SUPP-05", _chara_label(cid, chara), "angry_point", v, new_v))
    return records


def _iter_cloth_containers(chara):
    """
    参数:
        chara: 角色对象
    返回值:
        Iterator[Tuple[str, dict]]: (容器名, 槽位字典)序列；cloth结构缺失时为空
    功能:
        遍历四个服装容器，结构非法的容器跳过（形状问题属BODY-01，不在修复范围）
    """
    cloth = getattr(chara, "cloth", None)
    if cloth is None:
        return
    for attr_name in ("cloth_wear", "cloth_off", "cloth_locker_in_shower", "cloth_locker_in_dormitory"):
        d = getattr(cloth, attr_name, None)
        if isinstance(d, dict):
            yield attr_name, d


@register_repair("BODY-02", "非法服装id清除与错位归正")
def repair_cloth_id_validity(cache) -> List[dict]:
    """
    参数:
        cache: 当前游戏缓存对象
    返回值:
        List[dict]: 修复记录列表
    功能:
        与BODY-02同语义：四容器内配置中不存在的服装id（含非int与0占位）直接移除（悬空引用清除，
        旧版本遗留的已删除服装id属此类）；id有效但clothing_type与所在槽位不符的，移动到同容器的正确槽位
        （若正确槽位已含该id则仅从错误槽位移除）
    """
    tem = getattr(game_config, "config_clothing_tem", None)
    if not tem:
        return []
    records = []
    for cid, chara in cache.character_data.items():
        for attr_name, d in _iter_cloth_containers(chara):
            for t, lst in list(d.items()):
                if not isinstance(lst, list):
                    continue
                invalid = [c for c in lst if type(c) is not int or c == 0 or c not in tem]
                misplaced = [c for c in lst if type(c) is int and c in tem and getattr(tem[c], "clothing_type", None) != t]
                if not invalid and not misplaced:
                    continue
                old_list = list(lst)
                lst[:] = [c for c in lst if c not in invalid and c not in misplaced]
                for c in misplaced:
                    correct_t = getattr(tem[c], "clothing_type", None)
                    if correct_t in d and isinstance(d[correct_t], list) and c not in d[correct_t]:
                        d[correct_t].append(c)
                records.append(_record("BODY-02", _chara_label(cid, chara), f"cloth.{attr_name}[{t}]", old_list, list(lst)))
    return records


@register_repair("BODY-03", "同槽位重复服装去重")
def repair_cloth_slot_duplicates(cache) -> List[dict]:
    """
    参数:
        cache: 当前游戏缓存对象
    返回值:
        List[dict]: 修复记录列表
    功能:
        与BODY-03同语义：同一容器同一槽位列表内重复的服装id只保留首个，其余移除（保持原有顺序）
    """
    records = []
    for cid, chara in cache.character_data.items():
        for attr_name, d in _iter_cloth_containers(chara):
            for t, lst in d.items():
                if not isinstance(lst, list) or len(lst) == len(set(lst)):
                    continue
                old_list = list(lst)
                seen = set()
                lst[:] = [c for c in lst if not (c in seen or seen.add(c))]
                records.append(_record("BODY-03", _chara_label(cid, chara), f"cloth.{attr_name}[{t}]", old_list, list(lst)))
    return records


@register_repair("BODY-05", "跨位置重复服装归位")
def repair_cloth_cross_location(cache) -> List[dict]:
    """
    参数:
        cache: 当前游戏缓存对象
    返回值:
        List[dict]: 修复记录列表
    功能:
        与BODY-05同语义：同一服装id同时出现在穿着/宿舍衣柜/大浴场衣柜中的多处时，只保留优先级最高的一处
        （穿着 > 宿舍衣柜 > 大浴场衣柜：穿在身上的以身上为准，两柜重复时宿舍衣柜是持久归属位），
        其余位置移除。cloth_off与检查同样排除
    """
    priority = ("cloth_wear", "cloth_locker_in_dormitory", "cloth_locker_in_shower")
    records = []
    for cid, chara in cache.character_data.items():
        cloth = getattr(chara, "cloth", None)
        if cloth is None:
            continue
        containers = []
        for attr_name in priority:
            d = getattr(cloth, attr_name, None)
            if isinstance(d, dict):
                containers.append((attr_name, d))
        # 服装id -> 首个（最高优先级）出现位置的容器名
        first_seen: Dict[int, str] = {}
        for attr_name, d in containers:
            for t, lst in d.items():
                if not isinstance(lst, list):
                    continue
                for c in lst:
                    if type(c) is int:
                        first_seen.setdefault(c, attr_name)
        for attr_name, d in containers:
            for t, lst in d.items():
                if not isinstance(lst, list):
                    continue
                dup = [c for c in lst if type(c) is int and first_seen.get(c) != attr_name]
                if not dup:
                    continue
                old_list = list(lst)
                lst[:] = [c for c in lst if c not in dup]
                records.append(_record("BODY-05", _chara_label(cid, chara), f"cloth.{attr_name}[{t}]", old_list, list(lst)))
    return records


@register_repair("BODY-35", "个人服装模板列表无效项清除")
def repair_clothing_tem_list(cache) -> List[dict]:
    """
    参数:
        cache: 当前游戏缓存对象
    返回值:
        List[dict]: 修复记录列表
    功能:
        与BODY-35同语义：clothing_tem列表中配置已不存在的服装模板id（含非int项）移除
    """
    tem = getattr(game_config, "config_clothing_tem", None)
    if not tem:
        return []
    records = []
    for cid, chara in cache.character_data.items():
        lst = getattr(getattr(chara, "cloth", None), "clothing_tem", None)
        if not isinstance(lst, list):
            continue
        bad = [x for x in lst if type(x) is not int or x not in tem]
        if not bad:
            continue
        old_list = list(lst)
        lst[:] = [x for x in lst if x not in bad]
        records.append(_record("BODY-35", _chara_label(cid, chara), "cloth.clothing_tem", old_list, list(lst)))
    return records


@register_repair("ISLAND-09", "岗位集合按在编名单重算")
def repair_work_npc_set(cache) -> List[dict]:
    """
    参数:
        cache: 当前游戏缓存对象
    返回值:
        List[dict]: 修复记录列表
    功能:
        与ISLAND-09同语义：all_work_npc_set是可由角色work.work_type逐人重算的派生缓存，
        调用游戏自身的维护函数basement.update_work_people()整体重算（源数据即真相），留痕各岗位集合的前后差异
    """
    from Script.Design import basement

    ri = cache.rhodes_island
    old_sets = {wid: set(s) for wid, s in getattr(ri, "all_work_npc_set", {}).items() if isinstance(s, set)}
    # 唯一例外：游戏既有维护函数内部读取全局cache；此处只调用它重算派生岗位集合，不改造该函数本身
    basement.update_work_people()
    records = []
    new_sets = getattr(ri, "all_work_npc_set", {})
    for wid in set(old_sets) | set(new_sets):
        old_s = old_sets.get(wid, set())
        new_s = new_sets.get(wid, set())
        if old_s != new_s:
            records.append(_record("ISLAND-09", "罗德岛岗位集合", f"all_work_npc_set[{wid}]", sorted(old_s), sorted(new_s)))
    return records


@register_repair("ISLAND-28", "主供能调控员非法槽位清空")
def repair_main_power_operator_slots(cache) -> List[dict]:
    """
    参数:
        cache: 当前游戏缓存对象
    返回值:
        List[dict]: 修复记录列表
    功能:
        与ISLAND-28同语义：main_power_facility_operator_ids四槽中，指向不存在角色或work_type!=11角色的槽位
        置0（空槽标记）；同一cid重复占多槽时保留首个、其余置0
    """
    ri = cache.rhodes_island
    cd = cache.character_data
    slots = getattr(ri, "main_power_facility_operator_ids", None)
    if not (isinstance(slots, list) and len(slots) == 4):
        return []
    old_slots = list(slots)
    seen = set()
    for i, m in enumerate(slots):
        if not m:
            continue
        if m in seen or not (m in cd and getattr(getattr(cd[m], "work", None), "work_type", None) == 11):
            slots[i] = 0
        else:
            seen.add(m)
    if slots == old_slots:
        return []
    return [_record("ISLAND-28", "罗德岛主供能设施", "main_power_facility_operator_ids", old_slots, list(slots))]


@register_repair("ISLAND-29", "监狱长悬空引用修正")
def repair_warden_reference(cache) -> List[dict]:
    """
    参数:
        cache: 当前游戏缓存对象
    返回值:
        List[dict]: 修复记录列表
    功能:
        与ISLAND-29（引用子句，兼ROSTER-12）同语义：current_warden_id非0但指向的角色不存在或work_type!=191时，
        若恰有一名角色work_type==191则改指该角色，否则置0（无监狱长）。囚犯表子句语义不在本修复范围
    """
    ri = cache.rhodes_island
    cd = cache.character_data
    warden_id = getattr(ri, "current_warden_id", 0)
    if warden_id == 0 or (warden_id in cd and getattr(getattr(cd[warden_id], "work", None), "work_type", None) == 191):
        return []
    actual_wardens = [cid for cid, ch in cd.items() if getattr(getattr(ch, "work", None), "work_type", None) == 191]
    new_id = actual_wardens[0] if len(actual_wardens) == 1 else 0
    ri.current_warden_id = new_id
    return [_record("ISLAND-29", "罗德岛监狱", "current_warden_id", warden_id, new_id)]


def apply_all_repairs(cache) -> List[dict]:
    """
    参数:
        cache: 当前游戏缓存对象
    返回值:
        List[dict]: 全部实际发生的修复记录（供门面返回；游戏侧无需使用返回值）
    功能:
        debug_mode开启时整体跳过修复，而静态检查仍照常运行。否则逐条执行注册表中的修复策略并写入留痕；
        每条修复独立隔离，单条失败只记录检查器自身异常，不影响其余修复。本函数的总兜底与就绪守卫由门面负责
    """
    all_records: List[dict] = []
    if getattr(cache, "debug_mode", False):
        return all_records
    for check_id, (repair_name, repair_func) in _repair_registry.items():
        try:
            all_records.extend(repair_func(cache))
        except Exception as e:
            check_log.write_self_error_log(e)
    if all_records:
        check_log.write_repair_log(all_records, cache)
    return all_records
