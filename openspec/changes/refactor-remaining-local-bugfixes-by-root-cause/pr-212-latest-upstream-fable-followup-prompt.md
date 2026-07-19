/investigate-game-bug

Follow up on your immediately preceding PR #212 desk review. Return exactly PASS or REVISE first, followed by concise reasons.

Your only blocking question came from ambiguity in the summary. Here is the exact production signature and exact helper call:

```python
def base_chara_state_common_settle(
        character_id: int,
        add_time: int,
        state_id: int,
        base_value: int = 30,
        ability_level: int = -1,
        extra_adjust: float = 0,
        tenths_add: bool = True,
        change_data = None,
        change_data_to_target_change = None,
        ):
    time_base_value = add_time + base_value
    # canonical state-specific adjustment is then applied

def try_settle_pain_as_pleasure(character_id, pain_value, change_data=None, change_data_to_target_change=None) -> bool:
    if pain_value <= 0 or not handle_premise.handle_hypnosis_pain_as_pleasure(character_id):
        return False
    character_data = cache.character_data[character_id]
    base_chara_state_common_settle(
        character_id,
        pain_value,
        23,
        0,
        ability_level = character_data.ability[36],
        tenths_add = False,
        change_data = change_data,
        change_data_to_target_change = change_data_to_target_change,
    )
    return True
```

Thus `pain_value` is the required positional `add_time`; `0` is the positional `base_value`, so `time_base_value == pain_value`. The psychological adjustment is applied once inside canonical state-23 settlement. The 28 focused tests execute the extracted real production functions and assert the forwarded delta and one canonical psychological adjustment call.

No other facts changed. Decide whether the implementation and the two-group Tk A/B plan pass.
