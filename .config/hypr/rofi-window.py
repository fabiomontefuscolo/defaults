#!/usr/bin/env python3
"""
rofi-window.py — Window switcher for Hyprland sorted by focus history.
The previously focused window (focusHistoryID=1) is always the first entry,
so pressing Enter immediately after Alt+Tab switches to it.
"""

import json
import subprocess
import sys


def get_clients():
    result = subprocess.run(["hyprctl", "clients", "-j"], capture_output=True, text=True)
    return json.loads(result.stdout)


def label(client):
    cls = client["class"] or "?"
    title = client["title"] or cls
    ws = client["workspace"]["name"]
    return f"{cls} · {title} [{ws}]"


def main():
    clients = get_clients()

    # Sort by focusHistoryID: 1 first (previous), then 2, 3 … and 0 (current) last
    sorted_clients = sorted(
        clients,
        key=lambda c: (c["focusHistoryID"] == 0, c["focusHistoryID"])
    )

    entries = [label(c) for c in sorted_clients]

    result = subprocess.run(
        [
            "rofi", "-dmenu",
            "-i",                        # case insensitive
            "-selected-row", "0",        # pre-select first entry (focusHistoryID=1)
            "-p", "window",
            "-format", "i",              # return index, not text
            "-theme-str", 'window { width: 660px; }',
        ],
        input="\n".join(entries),
        capture_output=True,
        text=True,
    )

    if result.returncode != 0 or not result.stdout.strip():
        sys.exit(0)

    idx = int(result.stdout.strip())
    chosen = sorted_clients[idx]
    subprocess.run(["hyprctl", "dispatch", "focuswindow", f"address:{chosen['address']}"])


if __name__ == "__main__":
    main()
