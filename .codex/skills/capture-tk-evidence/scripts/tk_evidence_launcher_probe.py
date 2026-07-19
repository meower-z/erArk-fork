#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tk 取证启动器 + 只读按钮坐标探针。

与 _tk_evidence_launcher.py 相同（种子 + 最大化垫片 + 运行 cwd 的 game.py），
另外安装一个**只读**的循环：每 300ms 把当前屏幕上所有可点击按钮的
{返回值: [中心x, 中心y]} 写到 ERARK_BUTTONS_JSON 指向的文件。

它只读取 Tk 控件的 bbox，不改动任何游戏状态或逻辑，因此对 A/B 对照无影响。
视觉 agent 据此用**真实坐标**点击目标按钮，而不必从缩小的截图里估坐标。
"""
import json
import os
import random
import runpy
import sys
import tkinter
from pathlib import Path

import numpy

BUTTONS_JSON = os.environ.get(
    "ERARK_BUTTONS_JSON",
    "/tmp/claude-1000/-home-ubuntu-games-erArk/d024c6c3-9f42-4104-b312-8e624d412043/scratchpad/buttons.json",
)

_original_wm_state = tkinter.Wm.wm_state


def _linux_compatible_wm_state(window, newstate=None):
    if newstate == "zoomed":
        window.attributes("-zoomed", True)
        return None
    return _original_wm_state(window, newstate)


def _dump_buttons(root):
    """把当前可见按钮的 {返回值: [中心x,中心y]} 写入 BUTTONS_JSON（只读，容错）。"""
    try:
        import Script.Core.main_frame as mf
        tb = mf.textbox
        out = {}
        for cmd_number, tag in list(mf.cmd_tag_map.items()):
            rng = tb.tag_ranges(tag)
            if not rng:
                continue
            # 用按钮文本首字符的位置：首字符必在该按钮 tag 内，点它一定触发。
            # 范围尾端 bbox 在换行/行尾时会跑到很靠右，故不用来算中心。
            bb_start = tb.bbox(rng[0])
            if not bb_start:
                continue  # 不在可视区域内，暂不可点击
            x1, y1, w1, h1 = bb_start
            cx = x1 + max(w1 // 2, 4)
            cy = y1 + h1 // 2
            out[str(cmd_number)] = [int(cx), int(cy)]
        tmp = BUTTONS_JSON + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False)
        os.replace(tmp, BUTTONS_JSON)
    except Exception:
        pass
    root.after(300, lambda: _dump_buttons(root))


_real_mainloop = tkinter.Misc.mainloop


def _mainloop(self, *args, **kwargs):
    try:
        self.after(600, lambda: _dump_buttons(self))
    except Exception:
        pass
    return _real_mainloop(self, *args, **kwargs)


tkinter.Misc.mainloop = _mainloop

random.seed(20260719)
numpy.random.seed(20260719)
tkinter.Wm.wm_state = _linux_compatible_wm_state
tkinter.Wm.state = _linux_compatible_wm_state
sys.path.insert(0, str(Path.cwd()))
runpy.run_path("game.py", run_name="__main__")
