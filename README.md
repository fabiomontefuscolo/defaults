# defaults

Personal dotfiles for Hyprland on Manjaro (Wayland, Intel Iris Xe, dual monitors).

## Install

```shell
curl -sL https://github.com/fabiomontefuscolo/defaults/archive/refs/heads/main.tar.gz \
    | tar --strip-components=1 --exclude=defaults-main/README.md -C $HOME -zxvf -
```

## Stack

| Role | Tool |
|---|---|
| Window manager | Hyprland |
| Status bar | Waybar |
| Launcher | Rofi |
| Notifications | Dunst |
| Wallpaper | swaybg |
| Terminal | kitty |
| Editor | Neovim / Zed |
| Browser | Brave |

---

## Keyboard shortcuts

> `Super` = Windows/Meta key

### Apps

| Shortcut | Action |
|---|---|
| `Super + Space` | App launcher (Rofi) |
| `Super + Return` | Terminal (kitty) |
| `Super + Q` | Close window |
| `Super + E` | File manager |
| `Super + V` | Toggle floating |
| `Super + F` | Maximize window |
| `Super + Shift + F` | True fullscreen |

### Focus & tiling

| Shortcut | Action |
|---|---|
| `Super + ←/→/↑/↓` | Move focus |
| `Super + Shift + ←/→/↑/↓` | Swap window in tiling layout |
| `Super + P` | Toggle pseudotile (dwindle) |
| `Super + J` | Toggle split direction (dwindle) |

### Workspaces

| Shortcut | Action |
|---|---|
| `Super + 1–0` | Switch to workspace 1–10 |
| `Super + Shift + 1–0` | Move window to workspace 1–10 |
| `Super + S` | Toggle scratchpad |
| `Super + Shift + S` | Send window to scratchpad |
| `Super + Scroll` | Cycle workspaces |

### Screenshots

| Shortcut | Action |
|---|---|
| `Print` | Full screen → `~/Pictures/Screenshots/` |
| `Shift + Print` | Region select |
| `Super + Print` | Active window |

### Media & system

| Shortcut | Action |
|---|---|
| `XF86AudioRaiseVolume / LowerVolume` | Volume ±5% |
| `XF86AudioMute` | Toggle mute |
| `XF86MonBrightnessUp / Down` | Brightness ±5% |
| `XF86AudioPlay / Pause / Next / Prev` | Media control (playerctl) |

### kitty — terminal panes & tabs

| Shortcut | Action |
|---|---|
| `Ctrl+Shift+Enter` | New pane |
| `Ctrl+Shift+X` | Close pane |
| `Ctrl+Shift+H/J/K/L` | Navigate panes |
| `Alt + ←/→/↑/↓` | Resize pane |
| `Ctrl+Shift+Space` | Cycle layouts |
| `Ctrl+Shift+T` | New tab |
| `Ctrl+Shift+W` | Close tab |
| `Ctrl+Tab` | Next tab |
| `Ctrl+Shift+Tab` | Previous tab |
| `Ctrl+Alt+1–5` | Jump to tab |
| `Ctrl+Shift+B` | **Broadcast input to all panes** |
| `Ctrl+Shift+C / V` | Copy / Paste |
| `Ctrl+= / Ctrl+-` | Font size up / down |

---

## Where to change things

### Monitors
**File:** `.config/hypr/hyprland.conf` — top of file, `### MONITORS ###` section

```
monitor = eDP-1, disable                  # laptop screen (disabled — broken lid)
monitor = ,      2560x1440, 1920x0, 1    # any other connected monitor (Dell)
```

Run `hyprctl monitors` to get your monitor names.

---

### Keyboard shortcuts
**File:** `.config/hypr/hyprland.conf` — `### KEYBINDINGS ###` section

- Change `$mainMod = SUPER` to use a different modifier key.
- All app launcher, focus, workspace, and media bindings are in this section.

---

### Default apps
**File:** `.config/hypr/hyprland.conf` — `### MY PROGRAMS ###` section

```
$terminal    = kitty
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

| Setting | Where |
|---|---|
| Window gaps | `general { gaps_in, gaps_out }` |
| Border width & colour | `general { border_size, col.active_border }` |
| Corner rounding | `decoration { rounding }` |
| Blur | `decoration > blur { size, passes }` |
| Shadows | `decoration > shadow { range, color }` |
| Window opacity | `decoration { active_opacity, inactive_opacity }` |
| Animations | `animations { }` block — adjust speed values |

---

### Terminal appearance & shortcuts
**File:** `.config/kitty/kitty.conf`

- Font: `font_family` and `font_size`
- Colours: the `Colors` section (Catppuccin Mocha by default)
- Opacity: `background_opacity` (0.0–1.0)
- Layouts available: `enabled_layouts`
- All keybindings are at the bottom under `Keyboard shortcuts`

---

### Status bar layout & modules
**File:** `.config/waybar/config.jsonc`

- `modules-left`, `modules-center`, `modules-right` — rearrange or add/remove modules.
- Common extras to add: `"cpu"`, `"memory"`, `"temperature"`.
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
hyprland waybar rofi dunst swaybg kitty
xdg-desktop-portal-hyprland polkit-gnome
network-manager-applet blueman pavucontrol
grim slurp playerctl brightnessctl
```

Optional for better icons/fonts:
```
ttf-jetbrains-mono-nerd papirus-icon-theme
```
