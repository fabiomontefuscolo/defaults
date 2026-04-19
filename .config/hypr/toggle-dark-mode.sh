#!/usr/bin/env bash
# Toggle between dark and light mode for GTK and Qt apps

CURRENT=$(gsettings get org.gnome.desktop.interface color-scheme)

if [ "$CURRENT" = "'prefer-dark'" ]; then
    gsettings set org.gnome.desktop.interface color-scheme 'default'
    gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita'
else
    gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
    gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita-dark'
fi
