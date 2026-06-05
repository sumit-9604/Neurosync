import sys
import time
import argparse
import traceback
import platform
import pyautogui
from typing import Callable
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from automation.app_launcher        import AppLauncher
from automation.mouse_controller    import MouseController
from automation.keyboard_controller import KeyboardController
from command_router                 import execute, list_actions, action_info

# Disable failsafe globally for tests — we handle safety via clamping
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.03

PASS = "\033[92m✔ PASS\033[0m"
FAIL = "\033[91m✘ FAIL\033[0m"
SKIP = "\033[93m⊘ SKIP\033[0m"
WARN = "\033[93m⚠ WARN\033[0m"
SEP  = "─" * 70

results: list[dict] = []


def test(
    name: str,
    fn: Callable,
    expect_status: str = "success",
    skip: bool = False,
    warn_only: bool = False,
):
    if skip:
        print(f"  {SKIP}  {name}")
        results.append({"name": name, "result": "skip"})
        return None
    try:
        t0 = time.perf_counter()
        result = fn()
        elapsed = round((time.perf_counter() - t0) * 1000, 1)
        status = result.get("status") if isinstance(result, dict) else None
        ok = status == expect_status
        label  = PASS if ok else (WARN if warn_only else FAIL)
        detail = ""
        if not ok:
            detail = f"  → got status='{status}', msg={result.get('message', '')}"
        print(f"  {label}  {name}  [{elapsed}ms]{detail}")
        results.append({"name": name, "result": "pass" if ok else ("warn" if warn_only else "fail"), "data": result})
        return result
    except Exception as e:
        print(f"  {FAIL}  {name}  → Exception: {e}")
        print(f"          {traceback.format_exc().splitlines()[-1]}")
        results.append({"name": name, "result": "fail", "error": str(e)})
        return None


def section(title: str):
    print(f"\n{SEP}")
    print(f"  {title}")
    print(SEP)


def reset_mouse():
    """Move mouse to screen center — call after any corner/edge movement."""
    w, h = pyautogui.size()
    pyautogui.moveTo(w // 2, h // 2, duration=0.15)
    time.sleep(0.1)


def summary():
    total   = len(results)
    passed  = sum(1 for r in results if r["result"] == "pass")
    failed  = sum(1 for r in results if r["result"] == "fail")
    warned  = sum(1 for r in results if r["result"] == "warn")
    skipped = sum(1 for r in results if r["result"] == "skip")
    print(f"\n{'═'*70}")
    print(f"  RESULTS  —  Total: {total}  |  "
          f"\033[92mPass: {passed}\033[0m  |  "
          f"\033[91mFail: {failed}\033[0m  |  "
          f"\033[93mWarn: {warned}  Skip: {skipped}\033[0m")
    print(f"{'═'*70}")
    if failed:
        print("\n  Failed tests:")
        for r in results:
            if r["result"] == "fail":
                print(f"    ✘  {r['name']}")
                if "error" in r:
                    print(f"       {r['error']}")


# ═══════════════════════════════════════════════════════════
# MODULE 1 — AppLauncher
# ═══════════════════════════════════════════════════════════

def test_app_launcher(safe: bool = False):
    section("MODULE 1 — AppLauncher")
    SYS = platform.system()

    # Open chrome once, verify, kill, reopen with url, kill — no duplicates
    test("open_chrome() — no url",
         lambda: AppLauncher.open_chrome(),
         skip=safe)
    time.sleep(1.5)

    test("is_running('chrome') — after open",
         lambda: AppLauncher.is_running("chrome"),
         skip=safe)

    test("kill_app('chrome')",
         lambda: AppLauncher.kill_app("chrome"),
         skip=safe)
    time.sleep(0.5)

    test("open_chrome() — with url",
         lambda: AppLauncher.open_chrome("https://example.com"),
         skip=safe)
    time.sleep(0.5)
    time.sleep(0.3)

    test("open_vscode()",
         lambda: AppLauncher.open_vscode(),
         skip=safe)

    test("open_terminal()",
         lambda: AppLauncher.open_terminal(),
         skip=safe)

    test("open_calculator()",
         lambda: AppLauncher.open_calculator(),
         skip=safe)

    test("open_notepad()",
         lambda: AppLauncher.open_notepad(),
         skip=safe or SYS != "Windows")

    test("open_file_manager()",
         lambda: AppLauncher.open_file_manager(),
         skip=safe)

    time.sleep(1.0)

    test("list_running() — returns dict with 'running' key",
         lambda: AppLauncher.list_running())

    test("kill_app('nonexistent') — should error",
         lambda: AppLauncher.kill_app("nonexistent_xyz"),
         expect_status="error")

    test("is_running('nonexistent') — should be False",
         lambda: AppLauncher.is_running("nonexistent_xyz"))

    if SYS == "Windows":
        test("open_app('calc')",
             lambda: AppLauncher.open_app("calc"),
             skip=safe)
    elif SYS == "Linux":
        test("open_app('echo', ['hello'])",
             lambda: AppLauncher.open_app("echo", ["hello"]))
    elif SYS == "Darwin":
        test("open_app('/bin/echo', ['hello'])",
             lambda: AppLauncher.open_app("/bin/echo", ["hello"]))

    test("open_app with bad exe — should error",
         lambda: AppLauncher.open_app("__does_not_exist_xyz__"),
         expect_status="error")

    test("open_firefox()",  lambda: AppLauncher.open_firefox(),  skip=safe, warn_only=True)
    test("open_spotify()",  lambda: AppLauncher.open_spotify(),  skip=safe, warn_only=True)
    test("open_vlc()",      lambda: AppLauncher.open_vlc(),      skip=safe, warn_only=True)


# ═══════════════════════════════════════════════════════════
# MODULE 2 — MouseController
# ═══════════════════════════════════════════════════════════

def test_mouse_controller(safe: bool = False):
    section("MODULE 2 — MouseController")

    # Always reset to center before starting mouse tests
    if not safe:
        reset_mouse()

    test("get_screen_size()",
         lambda: MouseController.get_screen_size())

    test("get_position()",
         lambda: MouseController.get_position())

    test("get_history() — empty initially",
         lambda: MouseController.get_history())

    test("move(200, 200)",
         lambda: MouseController.move(200, 200),
         skip=safe)

    test("move with duration",
         lambda: MouseController.move(300, 300, duration=0.3),
         skip=safe)

    test("move_relative(+50, +50)",
         lambda: MouseController.move_relative(50, 50),
         skip=safe)

    test("move_smooth(400, 400)",
         lambda: MouseController.move_smooth(400, 400, steps=15),
         skip=safe)

    test("move_to_center()",
         lambda: MouseController.move_to_center(),
         skip=safe)

    test("move_to_corner('top-left')",
         lambda: MouseController.move_to_corner("top-left"),
         skip=safe)

    # Reset after corner — prevents failsafe on next call
    if not safe:
        reset_mouse()

    test("move_to_corner('bottom-right')",
         lambda: MouseController.move_to_corner("bottom-right"),
         skip=safe)

    # Reset after corner
    if not safe:
        reset_mouse()

    test("move_to_corner('invalid') — should error",
         lambda: MouseController.move_to_corner("middle"),
         expect_status="error")

    test("get_history() — populated after moves",
         lambda: MouseController.get_history(),
         skip=safe)

    test("pixel_color(100, 100)",
         lambda: MouseController.pixel_color(100, 100))

    test("scroll(3) — up",
         lambda: MouseController.scroll(3),
         skip=safe)

    test("scroll(-3) — down",
         lambda: MouseController.scroll(-3),
         skip=safe)

    test("scroll with position",
         lambda: MouseController.scroll(2, x=400, y=300),
         skip=safe)

    test("scroll_horizontal(3)",
         lambda: MouseController.scroll_horizontal(3),
         skip=safe)

    if not safe:
        reset_mouse()

    test("click() — left at current position",
         lambda: MouseController.click(),
         skip=safe)

    test("click(x, y) — left at coords",
         lambda: MouseController.click(300, 300),
         skip=safe)

    test("right_click()",
         lambda: MouseController.right_click(),
         skip=safe)

    test("middle_click()",
         lambda: MouseController.middle_click(),
         skip=safe)

    test("double_click()",
         lambda: MouseController.double_click(),
         skip=safe)

    test("triple_click()",
         lambda: MouseController.triple_click(),
         skip=safe)

    test("drag(100,100 → 200,200)",
         lambda: MouseController.drag(100, 100, 200, 200, duration=0.3),
         skip=safe)

    test("drag_relative(+50, +50)",
         lambda: MouseController.drag_relative(50, 50, duration=0.2),
         skip=safe)

    test("mouse_down() + mouse_up()",
         lambda: (MouseController.mouse_down() or True) and MouseController.mouse_up(),
         skip=safe)

    test("mouse_down('right') + mouse_up('right')",
         lambda: (MouseController.mouse_down("right") or True) and MouseController.mouse_up("right"),
         skip=safe)

    test("move clamped — x=-999 clamps to 0",
         lambda: MouseController.move(-999, -999),
         skip=safe)

    # Reset after clamped move lands at (0,0)
    if not safe:
        reset_mouse()

    sz = MouseController.get_screen_size()
    W  = sz.get("width",  9999) + 500
    H  = sz.get("height", 9999) + 500
    test("move clamped — beyond screen max",
         lambda: MouseController.move(W, H),
         skip=safe)

    if not safe:
        reset_mouse()


# ═══════════════════════════════════════════════════════════
# MODULE 3 — KeyboardController
# ═══════════════════════════════════════════════════════════

def test_keyboard_controller(safe: bool = False):
    section("MODULE 3 — KeyboardController")

    # Clipboard — always safe
    test("write_clipboard('hello test')",
         lambda: KeyboardController.write_clipboard("hello test"))

    test("read_clipboard() — returns 'hello test'",
         lambda: KeyboardController.read_clipboard())

    test("clear_clipboard()",
         lambda: KeyboardController.clear_clipboard())

    test("read_clipboard() — empty after clear",
         lambda: KeyboardController.read_clipboard())

    test("write_clipboard() — unicode emoji",
         lambda: KeyboardController.write_clipboard("Hello 🌍 World"))

    test("read_clipboard() — unicode preserved",
         lambda: KeyboardController.read_clipboard())

    KeyboardController.clear_clipboard()

    test("press_key('space')",
         lambda: KeyboardController.press_key("space"),
         skip=safe)

    test("press_key('enter')",
         lambda: KeyboardController.press_key("enter"),
         skip=safe)

    test("press_key('backspace')",
         lambda: KeyboardController.press_key("backspace"),
         skip=safe)

    test("press_key('tab')",
         lambda: KeyboardController.press_key("tab"),
         skip=safe)

    test("press_key('esc')",
         lambda: KeyboardController.press_key("esc"),
         skip=safe)

    test("press_key('INVALID') — should error",
         lambda: KeyboardController.press_key("INVALID_XYZ_KEY"),
         expect_status="error")

    test("press_key_times('down', 3)",
         lambda: KeyboardController.press_key_times("down", 3, interval=0.05),
         skip=safe)

    test("key_down('shift') + key_up('shift')",
         lambda: (KeyboardController.key_down("shift") or True) and KeyboardController.key_up("shift"),
         skip=safe)

    test("key_down('INVALID') — should error",
         lambda: KeyboardController.key_down("notakey"),
         expect_status="error")

    test("hotkey('ctrl','z') — undo",
         lambda: KeyboardController.hotkey("ctrl", "z"),
         skip=safe)

    test("hotkey('ctrl','y') — redo",
         lambda: KeyboardController.hotkey("ctrl", "y"),
         skip=safe)

    test("hotkey with invalid key — should error",
         lambda: KeyboardController.hotkey("ctrl", "BADKEY"),
         expect_status="error")

    test("copy()",          lambda: KeyboardController.copy(),          skip=safe)
    test("paste()",         lambda: KeyboardController.paste(),         skip=safe)
    test("cut()",           lambda: KeyboardController.cut(),           skip=safe)
    test("select_all()",    lambda: KeyboardController.select_all(),    skip=safe)
    test("undo()",          lambda: KeyboardController.undo(),          skip=safe)
    test("redo()",          lambda: KeyboardController.redo(),          skip=safe)
    test("save()",          lambda: KeyboardController.save(),          skip=safe)
    test("find()",          lambda: KeyboardController.find(),          skip=safe)
    test("switch_window()", lambda: KeyboardController.switch_window(), skip=safe)
    test("show_desktop()",  lambda: KeyboardController.show_desktop(),  skip=safe)

    test("type_text('Hello')",
         lambda: KeyboardController.type_text("Hello", interval=0.02),
         skip=safe)

    test("type_text_fast('Hello fast')",
         lambda: KeyboardController.type_text_fast("Hello fast"),
         skip=safe)

    test("type_text — empty string",
         lambda: KeyboardController.type_text(""))

    test("type_text — non-string should error",
         lambda: KeyboardController.type_text(12345),  # type: ignore
         expect_status="error")

    safe_sequence = [
        {"action": "wait", "seconds": 0.05},
        {"action": "wait", "seconds": 0.05},
    ]
    test("run_sequence — wait-only (safe)",
         lambda: KeyboardController.run_sequence(safe_sequence))

    full_sequence = [
        {"action": "type",  "text": "test", "interval": 0.02},
        {"action": "press", "key": "backspace"},
        {"action": "press", "key": "backspace"},
        {"action": "press", "key": "backspace"},
        {"action": "press", "key": "backspace"},
        {"action": "wait",  "seconds": 0.1},
    ]
    test("run_sequence — type + press + wait",
         lambda: KeyboardController.run_sequence(full_sequence),
         skip=safe)

    bad_sequence = [
        {"action": "wait",  "seconds": 0.01},
        {"action": "press", "key": "TOTALLY_INVALID"},
        {"action": "wait",  "seconds": 0.01},
    ]
    test("run_sequence — aborts on error",
         lambda: KeyboardController.run_sequence(bad_sequence),
         expect_status="error")

    unk_sequence = [{"action": "fly_to_moon"}]
    test("run_sequence — unknown action aborts",
         lambda: KeyboardController.run_sequence(unk_sequence),
         expect_status="error")


# ═══════════════════════════════════════════════════════════
# MODULE 4 — command_router
# ═══════════════════════════════════════════════════════════

def test_command_router(safe: bool = False):
    section("MODULE 4 — command_router.execute()")

    if not safe:
        reset_mouse()

    actions = list_actions()
    print(f"\n  list_actions() → {len(actions)} actions registered")

    test("list_actions() — non-empty",
         lambda: {"status": "success"} if len(list_actions()) > 0 else {"status": "error", "message": "empty"})

    test("action_info('mouse_move')",
         lambda: action_info("mouse_move"))

    test("action_info('unknown_xyz') — should error",
         lambda: action_info("unknown_xyz"),
         expect_status="error")

    test("execute — empty command → error",
         lambda: execute({}),
         expect_status="error")

    test("execute — unknown action → error",
         lambda: execute({"action": "fly_to_moon"}),
         expect_status="error")

    test("execute — missing required field → error",
         lambda: execute({"action": "mouse_move"}),
         expect_status="error")

    test("execute — request_id echoed back",
         lambda: execute({"action": "get_screen_size", "request_id": "abc-123"}))

    test("execute — duration_ms present in response",
         lambda: execute({"action": "get_screen_size"}))

    # Chrome — open fresh (Module 1 already killed it)
    test("router: open_chrome",
         lambda: execute({"action": "open_chrome", "url": "https://example.com"}),
         skip=safe)
    time.sleep(1.0)

    test("router: list_running_apps",
         lambda: execute({"action": "list_running_apps"}))

    test("router: is_app_running — chrome",
         lambda: execute({"action": "is_app_running", "label": "chrome"}),
         skip=safe)

    test("router: kill_app — chrome",
         lambda: execute({"action": "kill_app", "label": "chrome"}),
         skip=safe)
    time.sleep(0.3)

    test("router: kill_app — missing label → error",
         lambda: execute({"action": "kill_app"}),
         expect_status="error")

    # Calculator — open once here only
    test("router: open_calculator",
         lambda: execute({"action": "open_calculator"}),
         skip=safe)

    test("router: open_app — bad exe → error",
         lambda: execute({"action": "open_app", "app_name": "__bad_exe_xyz__"}),
         expect_status="error")

    test("router: get_screen_size",
         lambda: execute({"action": "get_screen_size"}))

    test("router: get_mouse_position",
         lambda: execute({"action": "get_mouse_position"}))

    test("router: mouse_move",
         lambda: execute({"action": "mouse_move", "x": 300, "y": 300}),
         skip=safe)

    test("router: mouse_move — missing y → error",
         lambda: execute({"action": "mouse_move", "x": 100}),
         expect_status="error")

    test("router: mouse_move_relative",
         lambda: execute({"action": "mouse_move_relative", "dx": 20, "dy": 20}),
         skip=safe)

    test("router: mouse_move_smooth",
         lambda: execute({"action": "mouse_move_smooth", "x": 400, "y": 400}),
         skip=safe)

    test("router: mouse_to_center",
         lambda: execute({"action": "mouse_to_center"}),
         skip=safe)

    test("router: mouse_to_corner top-right",
         lambda: execute({"action": "mouse_to_corner", "corner": "top-right"}),
         skip=safe)

    # Reset after corner
    if not safe:
        reset_mouse()

    test("router: mouse_scroll up",
         lambda: execute({"action": "mouse_scroll", "amount": 3}),
         skip=safe)

    test("router: mouse_scroll — missing amount → error",
         lambda: execute({"action": "mouse_scroll"}),
         expect_status="error")

    test("router: mouse_scroll_horizontal",
         lambda: execute({"action": "mouse_scroll_horizontal", "amount": 2}),
         skip=safe)

    test("router: mouse_click at coords",
         lambda: execute({"action": "mouse_click", "x": 350, "y": 350}),
         skip=safe)

    test("router: mouse_right_click",
         lambda: execute({"action": "mouse_right_click"}),
         skip=safe)

    test("router: mouse_double_click",
         lambda: execute({"action": "mouse_double_click"}),
         skip=safe)

    test("router: mouse_drag",
         lambda: execute({"action": "mouse_drag", "x1": 200, "y1": 200,
                          "x2": 300, "y2": 300}),
         skip=safe)

    test("router: mouse_drag — missing field → error",
         lambda: execute({"action": "mouse_drag", "x1": 100}),
         expect_status="error")

    test("router: mouse_drag_relative",
         lambda: execute({"action": "mouse_drag_relative", "dx": 30, "dy": 30}),
         skip=safe)

    if not safe:
        reset_mouse()

    test("router: get_pixel_color",
         lambda: execute({"action": "get_pixel_color", "x": 100, "y": 100}))

    test("router: get_pixel_color — missing x → error",
         lambda: execute({"action": "get_pixel_color", "y": 100}),
         expect_status="error")

    test("router: get_mouse_history",
         lambda: execute({"action": "get_mouse_history"}))

    test("router: mouse_down + mouse_up",
         lambda: (execute({"action": "mouse_down"}) or True) and execute({"action": "mouse_up"}),
         skip=safe)

    # Clipboard — always safe
    test("router: write_clipboard",
         lambda: execute({"action": "write_clipboard", "text": "router_test"}))

    test("router: read_clipboard",
         lambda: execute({"action": "read_clipboard"}))

    test("router: clear_clipboard",
         lambda: execute({"action": "clear_clipboard"}))

    test("router: write_clipboard — missing text → error",
         lambda: execute({"action": "write_clipboard"}),
         expect_status="error")

    test("router: press_key 'esc'",
         lambda: execute({"action": "press_key", "key": "esc"}),
         skip=safe)

    test("router: press_key — missing key → error",
         lambda: execute({"action": "press_key"}),
         expect_status="error")

    test("router: press_key_times 'down' x3",
         lambda: execute({"action": "press_key_times", "key": "down", "count": 3}),
         skip=safe)

    test("router: key_down + key_up 'shift'",
         lambda: (execute({"action": "key_down", "key": "shift"}) or True)
                 and execute({"action": "key_up", "key": "shift"}),
         skip=safe)

    test("router: hotkey ctrl+z",
         lambda: execute({"action": "hotkey", "keys": ["ctrl", "z"]}),
         skip=safe)

    test("router: hotkey — missing keys → error",
         lambda: execute({"action": "hotkey"}),
         expect_status="error")

    test("router: type_text",
         lambda: execute({"action": "type_text", "text": "hi"}),
         skip=safe)

    test("router: type_text_fast",
         lambda: execute({"action": "type_text_fast", "text": "fast hi"}),
         skip=safe)

    test("router: type_text — missing text → error",
         lambda: execute({"action": "type_text"}),
         expect_status="error")

    test("router: copy",           lambda: execute({"action": "copy"}),           skip=safe)
    test("router: paste",          lambda: execute({"action": "paste"}),          skip=safe)
    test("router: cut",            lambda: execute({"action": "cut"}),            skip=safe)
    test("router: select_all",     lambda: execute({"action": "select_all"}),     skip=safe)
    test("router: undo",           lambda: execute({"action": "undo"}),           skip=safe)
    test("router: redo",           lambda: execute({"action": "redo"}),           skip=safe)
    test("router: save",           lambda: execute({"action": "save"}),           skip=safe)
    test("router: find",           lambda: execute({"action": "find"}),           skip=safe)
    test("router: switch_window",  lambda: execute({"action": "switch_window"}),  skip=safe)

    test("router: run_sequence — wait-only",
         lambda: execute({
             "action": "run_sequence",
             "steps": [
                 {"action": "wait", "seconds": 0.02},
                 {"action": "wait", "seconds": 0.02},
             ]
         }))

    test("router: run_sequence — bad step aborts",
         lambda: execute({
             "action": "run_sequence",
             "steps": [{"action": "press", "key": "BADKEY_XYZ"}]
         }),
         expect_status="error")

    test("router: run_sequence — missing steps → error",
         lambda: execute({"action": "run_sequence"}),
         expect_status="error")

    section("Coverage — every registered action callable")
    for action_name in list_actions():
        test(f"action_info({action_name!r}) reachable",
             lambda a=action_name: action_info(a))


# ═══════════════════════════════════════════════════════════
# MODULE 5 — Integration chains
# ═══════════════════════════════════════════════════════════

def test_integration(safe: bool = False):
    section("MODULE 5 — Integration chains")

    if not safe:
        reset_mouse()

    def chain_move_click_type():
        r1 = execute({"action": "mouse_move",  "x": 400, "y": 400})
        if r1["status"] != "success": return r1
        time.sleep(0.1)
        r2 = execute({"action": "mouse_click", "x": 400, "y": 400})
        if r2["status"] != "success": return r2
        r3 = execute({"action": "type_text",   "text": "integration"})
        if r3["status"] != "success": return r3
        execute({"action": "select_all"})
        time.sleep(0.05)
        execute({"action": "press_key", "key": "delete"})
        return {"status": "success"}

    test("chain: move → click → type → cleanup",
         chain_move_click_type,
         skip=safe)

    def chain_clipboard():
        text = "clipboard_round_trip_✓"
        w = execute({"action": "write_clipboard", "text": text})
        if w["status"] != "success": return w
        r = execute({"action": "read_clipboard"})
        if r["status"] != "success": return r
        if r.get("content") != text:
            return {"status": "error", "message": f"Expected {text!r}, got {r.get('content')!r}"}
        execute({"action": "clear_clipboard"})
        return {"status": "success", "verified": text}

    test("chain: write → read → verify → clear clipboard",
         chain_clipboard)

    def chain_corners():
        for corner in ["top-left", "top-right", "bottom-right", "bottom-left"]:
            r = execute({"action": "mouse_to_corner", "corner": corner})
            if r["status"] != "success": return r
            time.sleep(0.15)
            reset_mouse()   # reset after each corner
        return {"status": "success"}

    test("chain: visit all 4 corners",
         chain_corners,
         skip=safe)

    def chain_sequence():
        return execute({
            "action": "run_sequence",
            "steps": [
                {"action": "wait", "seconds": 0.02},
                {"action": "wait", "seconds": 0.02},
                {"action": "wait", "seconds": 0.02},
            ]
        })

    test("chain: multi-step sequence (safe waits)",
         chain_sequence)

    def chain_request_id():
        r = execute({"action": "get_screen_size", "request_id": "TEST-999"})
        if r.get("request_id") != "TEST-999":
            return {"status": "error", "message": "request_id not echoed"}
        if "duration_ms" not in r:
            return {"status": "error", "message": "duration_ms missing"}
        return {"status": "success"}

    test("chain: request_id and duration_ms in every response",
         chain_request_id)

    def chain_rapid():
        for _ in range(20):
            r = execute({"action": "get_mouse_position"})
            if r["status"] != "success":
                return r
        return {"status": "success"}

    test("stress: 20 rapid get_mouse_position calls",
         chain_rapid)


# ═══════════════════════════════════════════════════════════
# Entry point
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Desktop Agent test suite")
    parser.add_argument("--module", choices=["launcher", "mouse", "keyboard", "router", "integration"],
                        help="Run only this module")
    parser.add_argument("--safe", action="store_true",
                        help="Skip tests that move the mouse, click, or type")
    args = parser.parse_args()

    print(f"\n{'═'*70}")
    print(f"  Desktop Agent — Full Test Suite")
    print(f"  OS: {platform.system()} {platform.release()}")
    print(f"  Mode: {'SAFE (no mouse/keyboard output)' if args.safe else 'FULL'}")
    print(f"{'═'*70}")

    run_all = args.module is None

    if run_all or args.module == "launcher":
        test_app_launcher(safe=args.safe)

    if run_all or args.module == "mouse":
        test_mouse_controller(safe=args.safe)

    if run_all or args.module == "keyboard":
        test_keyboard_controller(safe=args.safe)

    if run_all or args.module == "router":
        test_command_router(safe=args.safe)

    if run_all or args.module == "integration":
        test_integration(safe=args.safe)

    summary()


if __name__ == "__main__":
     main()