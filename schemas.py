"""Tool schemas for hermes-gui-plug — what the LLM sees."""

from __future__ import annotations

from typing import Any, Dict

GUI_SCREENSHOT_SCHEMA: Dict[str, Any] = {
    "name": "gui_screenshot",
    "description": (
        "Capture a screenshot of the user's desktop display. Saves a PNG under "
        "the Hermes cache and returns screenshot_path. Inspect the image with "
        "`vision_analyze` or share it with the user via MEDIA:<screenshot_path>. "
        "Requires a graphical session (local desktop or forwarded DISPLAY). "
        "Optional region captures a rectangular sub-area instead of the full screen."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "region": {
                "type": "array",
                "items": {"type": "integer"},
                "minItems": 4,
                "maxItems": 4,
                "description": (
                    "Optional [left, top, width, height] in screen pixels. "
                    "Omit for the full screen."
                ),
            },
        },
    },
}

GUI_MOVE_MOUSE_SCHEMA: Dict[str, Any] = {
    "name": "gui_move_mouse",
    "description": (
        "Move the mouse cursor to absolute screen coordinates (x, y). "
        "Coordinates originate at the top-left of the primary display. "
        "Use gui_screenshot first to locate UI elements visually."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "x": {
                "type": "integer",
                "description": "Horizontal pixel position from the left edge.",
            },
            "y": {
                "type": "integer",
                "description": "Vertical pixel position from the top edge.",
            },
            "duration": {
                "type": "number",
                "description": (
                    "Seconds to animate the move. 0 (default) jumps instantly."
                ),
            },
        },
        "required": ["x", "y"],
    },
}

GUI_CLICK_SCHEMA: Dict[str, Any] = {
    "name": "gui_click",
    "description": (
        "Click the mouse at screen coordinates or at the current cursor position. "
        "Supports left (default), right, and middle buttons, plus double-click."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "x": {
                "type": "integer",
                "description": (
                    "Horizontal pixel position. Omit to click at the current cursor."
                ),
            },
            "y": {
                "type": "integer",
                "description": (
                    "Vertical pixel position. Omit to click at the current cursor."
                ),
            },
            "button": {
                "type": "string",
                "enum": ["left", "right", "middle"],
                "description": "Mouse button to click. Default: left.",
            },
            "clicks": {
                "type": "integer",
                "minimum": 1,
                "description": "Number of clicks. Use 2 for double-click. Default: 1.",
            },
            "interval": {
                "type": "number",
                "description": "Seconds between clicks when clicks > 1. Default: 0.",
            },
        },
    },
}

GUI_KEY_SCHEMA: Dict[str, Any] = {
    "name": "gui_key",
    "description": (
        "Press one or more keyboard keys. A single key performs a simple press "
        "(e.g. enter, tab, escape, backspace). Multiple keys are held simultaneously "
        "as a chord (e.g. ['ctrl', 'c'] for copy, ['ctrl', 'shift', 'z'] for redo). "
        "Use 'ctrl' on Windows/Linux and 'command' on macOS for modifier-based shortcuts. "
        "Common names: enter, tab, escape, backspace, delete, space, "
        "up, down, left, right, home, end, pageup, pagedown, "
        "ctrl, shift, alt, command, f1–f12."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "keys": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 1,
                "description": (
                    "Key name(s) to press. One key = simple press; "
                    "multiple keys = chord (all held simultaneously)."
                ),
            },
            "presses": {
                "type": "integer",
                "minimum": 1,
                "description": "How many times to repeat. Default: 1.",
            },
            "interval": {
                "type": "number",
                "description": (
                    "Seconds between each repetition (presses > 1) "
                    "or between keys within a chord. Default: 0."
                ),
            },
        },
        "required": ["keys"],
    },
}

GUI_TYPE_SCHEMA: Dict[str, Any] = {
    "name": "gui_type",
    "description": (
        "Type text via the keyboard into whichever application currently has "
        "focus. Uses clipboard paste for reliable Unicode support. Click the "
        "target field with gui_click first so focus is correct."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "Text to type into the focused UI element.",
            },
            "interval": {
                "type": "number",
                "description": (
                    "Seconds between keystrokes when falling back to per-key "
                    "typing (ASCII only). Default: 0."
                ),
            },
        },
        "required": ["text"],
    },
}
