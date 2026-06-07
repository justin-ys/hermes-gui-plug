"""Pip entry point — same register() as the directory-installed plugin."""

from __future__ import annotations

from schemas import (
    GUI_CLICK_SCHEMA,
    GUI_MOVE_MOUSE_SCHEMA,
    GUI_SCREENSHOT_SCHEMA,
    GUI_TYPE_SCHEMA,
)
from tools import (
    check_gui_requirements,
    gui_click,
    gui_move_mouse,
    gui_screenshot,
    gui_type,
)

_TOOLS = (
    ("gui_screenshot", GUI_SCREENSHOT_SCHEMA, gui_screenshot, "🖥️"),
    ("gui_move_mouse", GUI_MOVE_MOUSE_SCHEMA, gui_move_mouse, "🖱️"),
    ("gui_click", GUI_CLICK_SCHEMA, gui_click, "👆"),
    ("gui_type", GUI_TYPE_SCHEMA, gui_type, "⌨️"),
)


def register(ctx) -> None:
    for name, schema, handler, emoji in _TOOLS:
        ctx.register_tool(
            name=name,
            toolset="gui",
            schema=schema,
            handler=handler,
            check_fn=check_gui_requirements,
            emoji=emoji,
        )
