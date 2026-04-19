# defaults

Personal dotfiles for Hyprland on Manjaro (Wayland, Intel Iris Xe, dual monitors).

## Install

```shell
curl -sL https://github.com/fabiomontefuscolo/defaults/archive/refs/heads/main.tar.gz \
    | tar --strip-components=1 --exclude=defaults-main/README.md -C $HOME -zxvf -
```

## Stack

| Role           | Tool         |
|---             |---           |
| Window manager | Hyprland     |
| Status bar     | Waybar       |
| Launcher       | Rofi         |
| Notifications  | Dunst        |
| Wallpaper      | swaybg       |
| Terminal       | Terminator   |
| Editor         | Neovim / Zed |
| Browser        | Brave        |

---

## Keyboard shortcuts

> `Super` = Windows/Meta key

### Apps

| Shortcut            | Action                |
|---                  |---                    |
| `Super + Space`     | App launcher (Rofi)   |
| `Super + Return`    | Terminal (Terminator) |
| `Super + Q`         | Close window          |
| `Super + E`         | File manager          |
| `Super + V`         | Toggle floating       |
| `Super + F`         | Maximize window       |
| `Super + Shift + F` | True fullscreen       |

### Rectangle-style window snapping (`Super + Alt + …`)

Mirrors the [Rectangle](https://rectangleapp.com) macOS app — `Super + Alt` = `Cmd + Option`.

| Shortcut               | Action                  |
|---                     |---                      |
| `Super + Alt + ←`      | Left half               |
| `Super + Alt + →`      | Right half              |
| `Super + Alt + ↑`      | Top half                |
| `Super + Alt + ↓`      | Bottom half             |
| `Super + Alt + Return` | Maximize (same monitor) |
| `Super + Alt + C`      | Center                  |
| `Super + Alt + U`      | Top-left quarter        |
| `Super + Alt + I`      | Top-right quarter       |
| `Super + Alt + J`      | Bottom-left quarter     |
| `Super + Alt + K`      | Bottom-right quarter    |

Snapping works per-monitor and is HiDPI-aware. Snapped windows become floating; use `Super + V` to return them to tiling.

### Focus & tiling

| Shortcut                  | Action                           |
|---                        |---                               |
| `Super + ←/→/↑/↓`         | Move focus                       |
| `Super + Shift + ←/→/↑/↓` | Swap window in tiling layout     |
| `Super + P`               | Toggle pseudotile (dwindle)      |
| `Super + J`               | Toggle split direction (dwindle) |

### Workspaces

| Shortcut              | Action                        |
|---                    |---                            |
| `Super + 1–0`         | Switch to workspace 1–10      |
| `Super + Shift + 1–0` | Move window to workspace 1–10 |
| `Super + S`           | Toggle scratchpad             |
| `Super + Shift + S`   | Send window to scratchpad     |
| `Super + Scroll`      | Cycle workspaces              |

### Screenshots

| Shortcut        | Action                                  |
|---              |---                                      |
| `Print`         | Full screen → `~/Pictures/Screenshots/` |
| `Shift + Print` | Region select                           |
| `Super + Print` | Active window                           |

### Media & system

| Shortcut                              | Action                    |
|---                                    |---                        |
| `XF86AudioRaiseVolume / LowerVolume`  | Volume ±5%                |
| `XF86AudioMute`                       | Toggle mute               |
| `XF86MonBrightnessUp / Down`          | Brightness ±5%            |
| `XF86AudioPlay / Pause / Next / Prev` | Media control (playerctl) |

---

## Where to change things

### Monitors
**File:** `.config/hypr/hyprland.conf` — top of file, `### MONITORS ###` section

```
monitor = eDP-1, 1920x1080, 0x0, 1       # internal display
monitor = ,      2560x1440, 1920x0, 1    # any other connected monitor
```

Run `hyprctl monitors` to get your monitor names. Change `eDP-1` if yours differs (e.g. `eDP-2`).  
Change `1920x0` to adjust the position of the external monitor relative to the internal one.

---

### Keyboard shortcuts
**File:** `.config/hypr/hyprland.conf` — `### KEYBINDINGS ###` section

- Change `$mainMod = SUPER` to use a different modifier key.
- All app launcher, focus, workspace, and media bindings are in this section.
- Rectangle snap bindings use `$mainMod ALT` — change `ALT` to `CTRL` if you prefer `Super + Ctrl`.

---

### Window snap behaviour
**File:** `.config/hypr/hypr-snap.sh`

This script handles all Rectangle-style snapping. Edit `snap_window` calls in the `case` block to change snap sizes.  
For example, to snap left to 60% width instead of 50%:

```bash
left) snap_window 0 0 $((W * 6 / 10)) $H ;;
```

---

### Default apps
**File:** `.config/hypr/hyprland.conf` — `### MY PROGRAMS ###` section

```
$terminal    = terminator
$fileManager = nautilus
$menu        = rofi -show drun -show-icons
```

---

### Autostart
**File:** `.config/hypr/hyprland.conf` — `### AUTOSTART ###` section

Add or remove `exec-once =` lines. Things started here: waybar, dunst, swaybg, polkit agent, nm-applet, blueman.

---

### Wallpaper
**File:** `.config/hypr/hyprland.conf` — `### AUTOSTART ###` section

```
exec-once = swaybg -m fill -c 1e1e2e
```

Replace `-c 1e1e2e` (solid colour) with `-i /path/to/image.jpg` to use a wallpaper image.  
Supported modes: `fill`, `fit`, `stretch`, `center`, `tile`.

---

### Look & feel (gaps, borders, blur, rounding)
**File:** `.config/hypr/hyprland.conf` — `### LOOK AND FEEL ###` section

| Setting               | Where                                             |
|---                    |---                                                |
| Window gaps           | `general { gaps_in, gaps_out }`                   |
| Border width & colour | `general { border_size, col.active_border }`      |
| Corner rounding       | `decoration { rounding }`                         |
| Blur                  | `decoration > blur { size, passes }`              |
| Shadows               | `decoration > shadow { range, color }`            |
| Window opacity        | `decoration { active_opacity, inactive_opacity }` |
| Animations            | `animations { }` block — adjust speed values      |

---

### Status bar layout & modules
**File:** `.config/waybar/config.jsonc`

- `modules-left`, `modules-center`, `modules-right` — rearrange or add/remove modules.
- Common extras to add: `"cpu"`, `"memory"`, `"temperature"`, `"custom/power"`.
- `persistent-workspaces` — change which workspace numbers are always shown.

### Status bar colours & fonts
**File:** `.config/waybar/style.css`

- Font: change `font-family` in the `*` block.
- Bar background: `window#waybar { background: ... }` — adjust the `rgba` alpha for more/less transparency.
- Accent colour (active workspace, etc.): search for `#89b4fa` (Catppuccin blue) and replace.

---

### Launcher appearance
**File:** `.config/rofi/config.rasi`

- Font: `font` in the `configuration { }` block.
- Number of results shown: `lines` in `listview { }`.
- Position offset (vertical): `y-offset` in `window { }` — negative moves it up, positive moves down.
- Icon theme: `icon-theme` in `configuration { }` (requires matching theme installed, e.g. `papirus-icon-theme`).
- Colours: the `*` block at the top defines `bg`, `fg`, `accent`, `selected-bg` — change those to retheme the whole launcher.

---

### Notifications
Dunst is started automatically. Its config lives at `~/.config/dunst/dunstrc` (not in this repo).  
Run `man dunst` or see [dunst docs](https://dunst-project.org/documentation/) to customise notification style, timeouts, and position.

---

## Dependencies

```
hyprland waybar rofi dunst swaybg
xdg-desktop-portal-hyprland polkit-gnome
network-manager-applet blueman pavucontrol
jq grim slurp playerctl brightnessctl
```

Optional for better icons/fonts:
```
ttf-jetbrains-mono-nerd papirus-icon-theme
```
