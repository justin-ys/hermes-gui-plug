# hermes-gui-plug

Hermes Agent plugin for cross-platform desktop GUI automation via [PyAutoGUI](https://pyautogui.readthedocs.io/).

## Tools

| Tool | Description |
|------|-------------|
| `gui_screenshot` | Capture the desktop (full screen or optional region) |
| `gui_move_mouse` | Move the cursor to `(x, y)` |
| `gui_click` | Click at coordinates or the current cursor position |
| `gui_type` | Type text into the focused application |

All tools register under the `gui` toolset.

## Install

### From Git (recommended)

```bash
hermes plugins install justin-ys/hermes-gui-plug --enable
```

Or clone manually:

```bash
git clone https://github.com/<owner>/hermes-gui-plug.git ~/.hermes/plugins/hermes-gui-plug
hermes plugins enable hermes-gui-plug
```

### Dependencies

Install PyAutoGUI into the **Hermes virtualenv** (not system Python):

```bash
source ~/.hermes/hermes-agent/.venv/bin/activate   # adjust path to your checkout
pip install -r ~/.hermes/plugins/hermes-gui-plug/requirements.txt
```

**Linux** may also need system packages for screenshot capture:

```bash
# Debian/Ubuntu
sudo apt install scrot python3-tk python3-dev

# Fedora
sudo dnf install scrot python3-tkinter
```

**macOS** and **Windows** generally work after `pip install`.

## Troubleshooting

**Plugin enabled but `gui` toolset missing from `hermes tools`?**

1. Check load status:
   ```bash
   hermes plugins list
   ```
   If `hermes-gui-plug` shows an error (e.g. `No module named 'hermes_gui_plug'`), update the plugin to the latest version — older layouts failed to import under Hermes's plugin loader.

2. Restart Hermes after enabling — plugin toolsets are discovered at process start.

3. In `hermes tools`, look for **🔌 Gui** near the bottom of the checklist (plugin toolsets append after built-ins).

4. Enable the `gui` toolset for your platform (CLI, gateway, etc.) — registering the plugin does not auto-enable the toolset.

## Enable

Plugins are opt-in. Add to `~/.hermes/config.yaml`:

```yaml
plugins:
  enabled:
    - hermes-gui-plug
```

Or run:

```bash
hermes plugins enable hermes-gui-plug
```

Enable the `gui` toolset if needed:

```bash
hermes tools   # toggle the gui toolset on your platform
```

## Usage pattern

Typical agent workflow:

1. `gui_screenshot` — see what's on screen
2. `vision_analyze` on the returned `screenshot_path` — locate UI elements
3. `gui_move_mouse` / `gui_click` — interact
4. `gui_type` — enter text (click the target field first)

Share screenshots with users via `MEDIA:<screenshot_path>` in agent responses.

## Requirements

- A **graphical desktop session** (local machine or SSH with `DISPLAY` / `WAYLAND_DISPLAY` forwarded)
- PyAutoGUI + pyperclip in the Hermes venv
- On Linux: `DISPLAY` or `WAYLAND_DISPLAY` must be set

Headless servers, Docker without X11, and SSH sessions without display forwarding will fail the runtime check — tools stay registered but are unavailable until a display is present.

## Safety

PyAutoGUI **failsafe** is enabled: moving the mouse to a screen corner aborts automation. The agent can control your real desktop — only enable this plugin in environments you trust.

## License

MIT — see [LICENSE](LICENSE).
