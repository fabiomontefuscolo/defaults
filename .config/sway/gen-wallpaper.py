#!/usr/bin/env python3
"""Generate a Sway cheat sheet wallpaper from the actual sway config.
Catppuccin Mocha theme. Re-run after changing shortcuts to update the wallpaper.
"""

import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ── Dimensions & paths ────────────────────────────────────────────────────────
W, H    = 2560, 1440
OUT     = Path.home() / "Pictures" / "sway-wallpaper.png"
CONFIG  = Path.home() / ".config" / "sway" / "config"

FONT_REG  = "/usr/share/fonts/TTF/HackNerdFont-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/TTF/HackNerdFont-Bold.ttf"

# ── Catppuccin Mocha ──────────────────────────────────────────────────────────
BG      = "#1e1e2e"
SURFACE = "#313244"
OVERLAY = "#45475a"
TEXT    = "#cdd6f4"
SUBTEXT = "#a6adc8"
BLUE    = "#89b4fa"
YELLOW  = "#f9e2af"
GREEN   = "#a6e3a1"
MAUVE   = "#cba6f7"
RED     = "#f38ba8"
PEACH   = "#fab387"

def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

# ── Parse sway config ─────────────────────────────────────────────────────────
def pretty_key(k):
    """Make key combos more readable."""
    k = k.replace("$mod", "Super")
    k = k.replace("--locked ", "")
    k = k.replace("Mod4", "Super")
    k = k.replace("Return", "Enter")
    k = k.replace("XF86Audio", "")
    k = k.replace("XF86Mon", "")
    k = k.replace("plus", "+5%")
    k = k.replace("minus", "−")
    k = k.replace("Minus", "−")
    k = k.replace("+", " + ")
    k = re.sub(r'\s+', ' ', k)
    return k.strip()

def parse_shortcuts(config_path):
    """Extract all bindsym lines from the sway config."""
    text = config_path.read_text()

    # Resolve variables like $mod, $term, $menu
    variables = {}
    for m in re.finditer(r'^set\s+(\$\w+)\s+(.+)$', text, re.MULTILINE):
        variables[m.group(1)] = m.group(2).strip()

    def resolve(s):
        for var, val in variables.items():
            s = s.replace(var, val)
        return s

    shortcuts = []
    for m in re.finditer(
        r'^\s*bindsym\s+((?:--\w+\s+)?[\w+$]+(?:\+[\w$]+)*)\s+(.+)$',
        text, re.MULTILINE
    ):
        keys = resolve(m.group(1)).strip()
        action = resolve(m.group(2)).strip()

        # Skip mode-internal bindsym (inside resize {})
        # Clean up action — take first meaningful word(s)
        action = re.sub(r'\s+', ' ', action)
        shortcuts.append((keys, action))

    return shortcuts

def categorize(shortcuts):
    """Group shortcuts into display sections."""
    sections = {
        "Apps":        (GREEN,  []),
        "Focus":       (BLUE,   []),
        "Move":        (MAUVE,  []),
        "Layout":      (YELLOW, []),
        "Workspaces":  (PEACH,  []),
        "Screenshots": (RED,    []),
        "Media":       (SUBTEXT,[]),
        "Other":       (OVERLAY,[]),
    }

    for keys, action in shortcuts:
        k = keys.lower()
        a = action.lower()

        if any(x in a for x in ["exec $term", "exec kitty"]):
            sections["Apps"][1].append((keys, "Terminal (kitty)"))
        elif any(x in a for x in ["exec $menu", "exec rofi"]):
            sections["Apps"][1].append((keys, "Launcher (rofi)"))
        elif "kill" in a:
            sections["Apps"][1].append((keys, "Close window"))
        elif "reload" in a:
            sections["Apps"][1].append((keys, "Reload config"))
        elif "exit" in a or "swaynag" in a:
            sections["Apps"][1].append((keys, "Exit sway"))
        elif "exec grim" in a and "slurp" in a:
            sections["Screenshots"][1].append((keys, "Region screenshot"))
        elif "exec grim" in a:
            sections["Screenshots"][1].append((keys, "Full screenshot"))
        elif "grim" in a:
            sections["Screenshots"][1].append((keys, "Screenshot"))
        elif any(x in a for x in ["volume", "sink", "audioraise", "audiolower", "audiomute", "micmute"]):
            label = "Volume +" if "raise" in k or "+5" in a else \
                    "Volume −" if "lower" in k or "-5" in a else \
                    "Mute mic" if "mic" in k else "Toggle mute"
            sections["Media"][1].append((keys, label))
        elif "brightness" in a or "brightness" in k:
            label = "Brightness +" if "up" in k else "Brightness −"
            sections["Media"][1].append((keys, label))
        elif "playerctl" in a:
            sections["Media"][1].append((keys, action.replace("exec playerctl ", "")))
        elif "focus" in a and "focus mode" not in a and "focus parent" not in a:
            sections["Focus"][1].append((keys, action))
        elif "focus parent" in a:
            sections["Focus"][1].append((keys, "Focus parent"))
        elif "focus mode_toggle" in a:
            sections["Other"][1].append((keys, "Toggle float focus"))
        elif "move" in a and "workspace" not in a and "scratchpad" not in a:
            sections["Move"][1].append((keys, action))
        elif "workspace" in a and "move" not in a:
            sections["Workspaces"][1].append((keys, action))
        elif "move container to workspace" in a:
            sections["Workspaces"][1].append((keys, action))
        elif any(x in a for x in ["split", "layout", "fullscreen", "floating", "scratchpad"]):
            sections["Layout"][1].append((keys, action))
        elif "mode" in a and "resize" in a:
            sections["Layout"][1].append((keys, "Enter resize mode"))
        else:
            sections["Other"][1].append((keys, action))

    # Clean up empty sections and deduplicate workspace binds
    result = []
    for name, (color, items) in sections.items():
        if not items:
            continue
        # Collapse workspace 1-10 into one line
        if name == "Workspaces":
            has_switch = any("workspace number" in a and "move" not in a for _, a in items)
            has_move   = any("move container to workspace" in a for _, a in items)
            items = []
            if has_switch:
                items.append(("Super + 1 … 0", "Switch to workspace"))
            if has_move:
                items.append(("Super + Shift + 1 … 0", "Move window to workspace"))
        result.append((name, color, items))

    return result

# ── Draw ──────────────────────────────────────────────────────────────────────
def main():
    shortcuts = parse_shortcuts(CONFIG)
    sections  = categorize(shortcuts)

    img  = Image.new("RGB", (W, H), hex2rgb(BG))
    draw = ImageDraw.Draw(img)

    f_title   = ImageFont.truetype(FONT_BOLD, 52)
    f_section = ImageFont.truetype(FONT_BOLD, 24)
    f_key     = ImageFont.truetype(FONT_BOLD, 19)
    f_desc    = ImageFont.truetype(FONT_REG,  19)

    PAD      = 60
    COL_GAP  = 50
    NCOLS    = 3
    ROW_H    = 32
    SEC_GAP  = 28

    # Title
    title = "Sway Keyboard Shortcuts"
    tw = draw.textlength(title, font=f_title)
    draw.text(((W - tw) / 2, PAD), title, font=f_title, fill=hex2rgb(TEXT))

    div_y = PAD + 52 + 18
    draw.line([(PAD, div_y), (W - PAD, div_y)], fill=hex2rgb(OVERLAY), width=2)

    col_w   = (W - 2 * PAD - (NCOLS - 1) * COL_GAP) // NCOLS
    start_y = div_y + 28

    # Distribute sections across columns roughly evenly
    def section_height(sec):
        return 24 + 10 + 10 + len(sec[2]) * (ROW_H + 6) + SEC_GAP

    total_h = sum(section_height(s) for s in sections)
    target  = total_h / NCOLS

    cols = [[], [], []]
    ci, running = 0, 0
    for sec in sections:
        cols[ci].append(sec)
        running += section_height(sec)
        if running >= target and ci < NCOLS - 1:
            ci += 1
            running = 0

    for ci, col_sections in enumerate(cols):
        x = PAD + ci * (col_w + COL_GAP)
        y = start_y

        for sec_name, color, items in col_sections:
            draw.text((x, y), sec_name, font=f_section, fill=hex2rgb(color))
            y += 24 + 10
            draw.line([(x, y), (x + col_w, y)], fill=hex2rgb(SURFACE), width=1)
            y += 10

            for keys, desc in items:
                display_key = pretty_key(keys)
                key_w = int(draw.textlength(display_key, font=f_key)) + 16
                draw.rounded_rectangle(
                    [x, y, x + key_w, y + ROW_H - 2],
                    radius=4, fill=hex2rgb(SURFACE)
                )
                draw.text((x + 8, y + 5), display_key, font=f_key, fill=hex2rgb(YELLOW))
                draw.text((x + key_w + 10, y + 5), desc, font=f_desc, fill=hex2rgb(SUBTEXT))
                y += ROW_H + 6

            y += SEC_GAP

    footer = "Super = Windows/Meta key   ·   generated from ~/.config/sway/config"
    fw = draw.textlength(footer, font=f_desc)
    draw.text(((W - fw) / 2, H - PAD), footer, font=f_desc, fill=hex2rgb(OVERLAY))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT)
    print(f"Saved → {OUT}")

if __name__ == "__main__":
    main()
