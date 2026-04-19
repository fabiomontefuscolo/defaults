#!/usr/bin/env bash
# hypr-snap.sh — Rectangle-style window snapping for Hyprland
# Usage: hypr-snap.sh <left|right|top|bottom|topleft|topright|bottomleft|bottomright|max|center>
#
# Mirrors Rectangle (macOS) shortcuts bound to Super+Alt+<key>.
# Windows are made floating and snapped to precise positions on their current monitor.

set -euo pipefail

DIR="${1:-}"
if [[ -z "$DIR" ]]; then
    echo "Usage: hypr-snap.sh <left|right|top|bottom|topleft|topright|bottomleft|bottomright|max|center>"
    exit 1
fi

# Max/center don't need float + pixel math — use native dispatchers
case "$DIR" in
    max)
        hyprctl dispatch fullscreen 1
        exit 0
        ;;
    center)
        hyprctl dispatch centerwindow
        exit 0
        ;;
esac

# Get active window info
WIN=$(hyprctl activewindow -j)
ADDR=$(echo "$WIN" | jq -r '.address')
MON_NAME=$(echo "$WIN" | jq -r '.monitor')

# Get the monitor the window is currently on
MON=$(hyprctl monitors -j | jq ".[] | select(.name == \"$MON_NAME\")")

# Physical pixels and scale → compute logical (workspace) dimensions
PW=$(echo "$MON" | jq '.width')
PH=$(echo "$MON" | jq '.height')
MX=$(echo "$MON" | jq '.x')
MY=$(echo "$MON" | jq '.y')
SC=$(echo "$MON" | jq '.scale')

# Logical size (what hyprctl positioning uses)
W=$(awk "BEGIN { printf \"%d\", $PW / $SC }")
H=$(awk "BEGIN { printf \"%d\", $PH / $SC }")

HW=$((W / 2))
HH=$((H / 2))

# Make the window floating so we can position it freely
hyprctl dispatch setfloating "address:$ADDR"

snap_window() {
    local x=$1 y=$2 w=$3 h=$4
    hyprctl dispatch resizewindowpixel "exact $w $h,address:$ADDR"
    hyprctl dispatch movewindowpixel   "exact $((MX + x)) $((MY + y)),address:$ADDR"
}

case "$DIR" in
    left)        snap_window 0   0   $HW $H  ;;
    right)       snap_window $HW 0   $HW $H  ;;
    top)         snap_window 0   0   $W  $HH ;;
    bottom)      snap_window 0   $HH $W  $HH ;;
    topleft)     snap_window 0   0   $HW $HH ;;
    topright)    snap_window $HW 0   $HW $HH ;;
    bottomleft)  snap_window 0   $HH $HW $HH ;;
    bottomright) snap_window $HW $HH $HW $HH ;;
    *)
        echo "Unknown direction: $DIR"
        exit 1
        ;;
esac
