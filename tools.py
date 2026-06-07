"""Tool handlers for hermes-gui-plug — PyAutoGUI desktop automation."""

from __future__ import annotations

import json
import os
import platform
import uuid
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from hermes_constants import get_hermes_dir


def check_gui_requirements() -> bool:
    """Return True when PyAutoGUI can reach a graphical desktop session."""
    try:
        import pyautogui  # noqa: F401
    except ImportError:
        return False

    system = platform.system().lower()
    if system == "linux":
        if not os.environ.get("DISPLAY") and not os.environ.get("WAYLAND_DISPLAY"):
            return False
    return True


def _import_pyautogui():
    import pyautogui

    pyautogui.FAILSAFE = True
    return pyautogui


def _screenshots_dir() -> Path:
    directory = get_hermes_dir("cache/screenshots", "gui_screenshots")
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _ok(**fields: Any) -> str:
    return json.dumps({"success": True, **fields})


def _err(message: str, **fields: Any) -> str:
    return json.dumps({"success": False, "error": message, **fields})


def _parse_region(region: Any) -> Optional[Tuple[int, int, int, int]]:
    if region is None:
        return None
    if not isinstance(region, list) or len(region) != 4:
        raise ValueError("region must be [left, top, width, height]")
    left, top, width, height = (int(v) for v in region)
    if width <= 0 or height <= 0:
        raise ValueError("region width and height must be positive")
    return left, top, width, height


def _paste_text(text: str, interval: float) -> str:
    """Type *text*; return the method used ('clipboard' or 'typewrite')."""
    pyautogui = _import_pyautogui()
    try:
        import pyperclip

        pyperclip.copy(text)
        mod = "command" if platform.system() == "Darwin" else "ctrl"
        pyautogui.hotkey(mod, "v")
        return "clipboard"
    except Exception:
        if not text.isascii():
            raise RuntimeError(
                "Unicode text requires pyperclip and a system clipboard "
                "(install pyperclip in the Hermes venv)"
            )
        pyautogui.write(text, interval=interval)
        return "typewrite"


def gui_screenshot(args: Dict[str, Any], **kwargs: Any) -> str:
    del kwargs
    try:
        region = _parse_region(args.get("region"))
    except (TypeError, ValueError) as exc:
        return _err(str(exc))

    try:
        pyautogui = _import_pyautogui()
        screenshots_dir = _screenshots_dir()
        screenshot_path = screenshots_dir / f"gui_screenshot_{uuid.uuid4().hex}.png"

        if region is None:
            image = pyautogui.screenshot()
        else:
            image = pyautogui.screenshot(region=region)

        image.save(screenshot_path, format="PNG")
        size = pyautogui.size()
        return _ok(
            screenshot_path=str(screenshot_path),
            width=image.width,
            height=image.height,
            screen_width=size.width,
            screen_height=size.height,
            region=list(region) if region else None,
            hint=(
                f"Inspect with vision_analyze or share via "
                f"MEDIA:{screenshot_path}"
            ),
        )
    except Exception as exc:
        return _err(f"Screenshot failed: {exc}")


def gui_move_mouse(args: Dict[str, Any], **kwargs: Any) -> str:
    del kwargs
    try:
        x = int(args["x"])
        y = int(args["y"])
    except (KeyError, TypeError, ValueError):
        return _err("x and y are required integers")

    duration = float(args.get("duration") or 0)
    if duration < 0:
        return _err("duration must be non-negative")

    try:
        pyautogui = _import_pyautogui()
        pyautogui.moveTo(x, y, duration=duration)
        position = pyautogui.position()
        return _ok(x=position.x, y=position.y, duration=duration)
    except Exception as exc:
        return _err(f"Mouse move failed: {exc}")


def gui_click(args: Dict[str, Any], **kwargs: Any) -> str:
    del kwargs
    button = args.get("button") or "left"
    if button not in {"left", "right", "middle"}:
        return _err("button must be left, right, or middle")

    try:
        clicks = int(args.get("clicks") or 1)
    except (TypeError, ValueError):
        return _err("clicks must be a positive integer")
    if clicks < 1:
        return _err("clicks must be at least 1")

    interval = float(args.get("interval") or 0)
    if interval < 0:
        return _err("interval must be non-negative")

    has_x = "x" in args and args["x"] is not None
    has_y = "y" in args and args["y"] is not None
    if has_x != has_y:
        return _err("provide both x and y, or omit both to click in place")

    try:
        pyautogui = _import_pyautogui()
        click_kwargs: Dict[str, Any] = {
            "button": button,
            "clicks": clicks,
            "interval": interval,
        }
        if has_x and has_y:
            click_kwargs["x"] = int(args["x"])
            click_kwargs["y"] = int(args["y"])

        pyautogui.click(**click_kwargs)
        position = pyautogui.position()
        return _ok(
            x=position.x,
            y=position.y,
            button=button,
            clicks=clicks,
        )
    except Exception as exc:
        return _err(f"Click failed: {exc}")


def gui_type(args: Dict[str, Any], **kwargs: Any) -> str:
    del kwargs
    text = args.get("text")
    if text is None or text == "":
        return _err("text is required")

    interval = float(args.get("interval") or 0)
    if interval < 0:
        return _err("interval must be non-negative")

    try:
        method = _paste_text(str(text), interval)
        return _ok(characters=len(str(text)), method=method)
    except Exception as exc:
        return _err(f"Keyboard input failed: {exc}")
