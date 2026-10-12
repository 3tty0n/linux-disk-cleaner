#!/bin/sh
# per-user install; PREFIX=/usr/local sudo ./install.sh for system-wide
set -e
cd "$(dirname "$0")"
P="${PREFIX:-$HOME/.local}"
install -Dm755 disk-cleaner "$P/bin/disk-cleaner"
install -Dm644 disk-cleaner.svg "$P/share/icons/hicolor/scalable/apps/disk-cleaner.svg"
install -Dm644 disk-cleaner.desktop "$P/share/applications/disk-cleaner.desktop"
gtk-update-icon-cache -qtf "$P/share/icons/hicolor" 2>/dev/null || true
update-desktop-database -q "$P/share/applications" 2>/dev/null || true
echo "installed to $P (needs python3 + PyGObject + GTK3 + pycairo, see README)"
