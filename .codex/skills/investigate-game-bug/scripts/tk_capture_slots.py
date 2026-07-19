#!/usr/bin/env python3
"""在三个隔离槽位中运行本地 Tk 证据命令。"""

from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import select
import signal
import subprocess
import sys
import time


SLOT_COUNT = 3
STATE_DIR = Path("/tmp/erark-tk-capture-slots")


def pid_alive(pid: int) -> bool:
    """输入进程号，返回该进程当前是否存活。"""
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except (OSError, ValueError):
        return False
    return True


def read_state(slot: int) -> dict:
    """输入槽位号并读取状态文件；文件不可用时返回空字典。"""
    path = STATE_DIR / f"slot-{slot}.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def active_slot_roots() -> set[int]:
    """返回存活槽位拥有的监督进程和子进程根节点。"""
    result: set[int] = set()
    for slot in range(SLOT_COUNT):
        state = read_state(slot)
        if pid_alive(int(state.get("supervisor_pid", 0))):
            result.add(int(state["supervisor_pid"]))
            child_pid = int(state.get("child_pid", 0))
            if child_pid:
                result.add(child_pid)
    return result


def process_parent(pid: int) -> int:
    """输入进程号并返回父进程号；无法读取时返回零。"""
    try:
        for line in (Path("/proc") / str(pid) / "status").read_text().splitlines():
            if line.startswith("PPid:"):
                return int(line.split()[1])
    except (FileNotFoundError, PermissionError, ProcessLookupError, OSError, ValueError):
        pass
    return 0


def is_owned_process(pid: int, roots: set[int]) -> bool:
    """输入进程号和槽位根节点，返回该进程是否属于任一槽位。"""
    seen = set()
    while pid and pid not in seen:
        if pid in roots:
            return True
        seen.add(pid)
        pid = process_parent(pid)
    return False


def game_processes() -> list[dict]:
    """返回存活的 erArk 游戏进程及兼容计数所需信息。"""
    result = []
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit():
            continue
        pid = int(entry.name)
        try:
            args = [part.decode(errors="replace") for part in (entry / "cmdline").read_bytes().split(b"\0") if part]
            text = " ".join(args)
            cwd = os.readlink(entry / "cwd")
        except (FileNotFoundError, PermissionError, ProcessLookupError, OSError):
            continue
        if not args or not Path(args[0]).name.startswith("python"):
            continue
        has_game_file = any(Path(argument).name == "game.py" for argument in args[1:])
        has_runpy_game = any("runpy.run_path" in argument and "game.py" in argument for argument in args[1:])
        if not has_game_file and not has_runpy_game:
            continue
        result.append({"pid": pid, "cwd": cwd, "command": text})
    return result


def legacy_games() -> list[dict]:
    """返回未受槽位分配器监督的游戏进程。"""
    roots = active_slot_roots()
    return [item for item in game_processes() if not is_owned_process(item["pid"], roots)]


def try_lock(slot: int):
    """输入槽位号并尝试加锁；忙碌时返回 None。"""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    lock_file = open(STATE_DIR / f"slot-{slot}.lock", "a+", encoding="utf-8")
    try:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock_file.close()
        return None
    return lock_file


def acquire_slot():
    """获取空闲槽位，并为未纳管的旧游戏进程保留容量。"""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    allocator_lock = open(STATE_DIR / "allocator.lock", "a+", encoding="utf-8")
    fcntl.flock(allocator_lock.fileno(), fcntl.LOCK_EX)
    free_slots = []
    try:
        for slot in range(SLOT_COUNT):
            lock_file = try_lock(slot)
            if lock_file is not None:
                free_slots.append((slot, lock_file))
        busy_count = SLOT_COUNT - len(free_slots)
        legacy_reserved = min(len(legacy_games()), SLOT_COUNT)
        if busy_count + legacy_reserved >= SLOT_COUNT or not free_slots:
            raise RuntimeError(
                f"no Tk capture slot available ({busy_count} supervised, "
                f"{legacy_reserved} reserved by legacy game processes)"
            )
        selected_slot, selected_lock = free_slots.pop(0)
        return selected_slot, selected_lock, legacy_reserved
    finally:
        for _slot, lock_file in free_slots:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            lock_file.close()
        fcntl.flock(allocator_lock.fileno(), fcntl.LOCK_UN)
        allocator_lock.close()


def start_xvfb(slot: int, geometry: str):
    """输入槽位和画面尺寸，启动隔离 Xvfb 并返回进程、显示号和日志句柄。"""
    read_fd, write_fd = os.pipe()
    log_path = STATE_DIR / f"slot-{slot}-xvfb.log"
    log_file = open(log_path, "w", encoding="utf-8")
    process = subprocess.Popen(
        ["Xvfb", "-displayfd", str(write_fd), "-screen", "0", geometry, "-nolisten", "tcp"],
        pass_fds=(write_fd,),
        stdout=log_file,
        stderr=subprocess.STDOUT,
        start_new_session=True,
    )
    os.close(write_fd)
    ready, _, _ = select.select([read_fd], [], [], 10)
    if not ready:
        process.terminate()
        process.wait(timeout=5)
        os.close(read_fd)
        log_file.close()
        raise RuntimeError(f"Xvfb did not report a display; see {log_path}")
    display_number = os.read(read_fd, 32).decode().strip()
    os.close(read_fd)
    if not display_number or process.poll() is not None:
        terminate_group(process)
        log_file.close()
        raise RuntimeError(f"Xvfb failed to start; see {log_path}")
    return process, f":{display_number}", log_file


def terminate_group(process: subprocess.Popen | None) -> None:
    """输入子进程并终止其进程组，不影响其他会话。"""
    if process is None or process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=10)
    except (ProcessLookupError, subprocess.TimeoutExpired):
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


def write_state(slot: int, state: dict) -> None:
    """输入槽位和状态，并原子写入所有权信息。"""
    path = STATE_DIR / f"slot-{slot}.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def run_command(args: argparse.Namespace) -> int:
    """输入运行参数，在命令完整生命周期内监督槽位和 X 显示。"""
    runtime = Path(args.runtime).resolve()
    if not runtime.is_dir():
        raise RuntimeError(f"runtime directory does not exist: {runtime}")
    command = list(args.command)
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        raise RuntimeError("missing command after --")

    slot, lock_file, legacy_reserved = acquire_slot()
    xvfb = None
    child = None
    xvfb_log = None
    state_path = STATE_DIR / f"slot-{slot}.json"
    stopping = False

    def request_stop(_signum, _frame):
        nonlocal stopping
        stopping = True
        if child is not None and child.poll() is None:
            try:
                os.killpg(child.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass

    previous_term = signal.signal(signal.SIGTERM, request_stop)
    previous_int = signal.signal(signal.SIGINT, request_stop)
    try:
        xvfb, display, xvfb_log = start_xvfb(slot, args.geometry)
        environment = os.environ.copy()
        environment["DISPLAY"] = display
        environment["ERARK_TK_CAPTURE_SLOT"] = str(slot)
        child = subprocess.Popen(
            command,
            cwd=runtime,
            env=environment,
            start_new_session=True,
        )
        state = {
            "slot": slot,
            "owner": args.owner,
            "runtime": str(runtime),
            "display": display,
            "geometry": args.geometry,
            "supervisor_pid": os.getpid(),
            "child_pid": child.pid,
            "xvfb_pid": xvfb.pid,
            "command": command,
            "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "legacy_slots_reserved_at_start": legacy_reserved,
        }
        write_state(slot, state)
        print(json.dumps(state, ensure_ascii=False), flush=True)
        return_code = child.wait()
        return 128 + signal.SIGTERM if stopping else return_code
    finally:
        terminate_group(child)
        terminate_group(xvfb)
        if xvfb_log is not None:
            xvfb_log.close()
        current = read_state(slot)
        if int(current.get("supervisor_pid", 0)) == os.getpid():
            state_path.unlink(missing_ok=True)
        signal.signal(signal.SIGTERM, previous_term)
        signal.signal(signal.SIGINT, previous_int)
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
        lock_file.close()


def slot_status() -> dict:
    """返回分配器、槽位和旧游戏进程状态。"""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    legacy = legacy_games()
    slots = []
    busy_count = 0
    for slot in range(SLOT_COUNT):
        lock_file = try_lock(slot)
        if lock_file is None:
            busy_count += 1
            state = read_state(slot)
            slots.append({"slot": slot, "status": "busy", "owner": state})
            continue
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
        lock_file.close()
        slots.append({"slot": slot, "status": "free"})
    return {
        "slot_count": SLOT_COUNT,
        "supervised_busy": busy_count,
        "legacy_reserved": min(len(legacy), SLOT_COUNT),
        "capacity_available": max(0, SLOT_COUNT - busy_count - len(legacy)),
        "legacy_games": legacy,
        "slots": slots,
    }


def stop_slot(slot: int, owner: str) -> int:
    """输入槽位和所有者，要求监督进程停止并清理子进程与 Xvfb。"""
    state = read_state(slot)
    supervisor_pid = int(state.get("supervisor_pid", 0))
    if not pid_alive(supervisor_pid):
        raise RuntimeError(f"slot {slot} has no live supervisor")
    if state.get("owner") != owner:
        raise RuntimeError(f"slot {slot} is owned by {state.get('owner')!r}, not {owner!r}")
    os.kill(supervisor_pid, signal.SIGTERM)
    return 0


def parse_args() -> argparse.Namespace:
    """解析命令行参数并返回命名空间。"""
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="action", required=True)

    run_parser = subparsers.add_parser("run", help="run a command under an acquired slot")
    run_parser.add_argument("--owner", required=True, help="thread and candidate label")
    run_parser.add_argument("--runtime", required=True, help="isolated runtime working directory")
    run_parser.add_argument("--geometry", default="2100x1100x24", help="Xvfb screen geometry")
    run_parser.add_argument("command", nargs=argparse.REMAINDER)

    subparsers.add_parser("status", help="print slot and legacy-process status as JSON")
    stop_parser = subparsers.add_parser("stop", help="stop a supervised slot")
    stop_parser.add_argument("slot", type=int, choices=range(SLOT_COUNT))
    stop_parser.add_argument("--owner", required=True, help="must match the recorded owner")
    return parser.parse_args()


def main() -> int:
    """分发所选操作并返回退出码。"""
    args = parse_args()
    try:
        if args.action == "run":
            return run_command(args)
        if args.action == "status":
            print(json.dumps(slot_status(), ensure_ascii=False, indent=2))
            return 0
        if args.action == "stop":
            return stop_slot(args.slot, args.owner)
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 75
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
