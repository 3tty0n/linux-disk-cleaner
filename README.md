# disk-cleaner

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Install](#install)
- [License](#license)

## Overview

GTK3 desktop app that finds disposable files and deletes them.

- Donut chart, sortable list and `/` usage bar; nothing is pre-selected
- Arch (pacman, paru/yay) is tested; apt and dnf are not run on real machines
- Failures are explained in the GUI; nothing is printed on the CLI

### What it finds

- `~/.cache/*`, npm/cargo caches, trash: contents emptied, dir kept
- paru clones: untracked files only (`PKGBUILD` and `.git` kept)
- Files over 500 MB in `$HOME`: deleted permanently, with a warning
- Package cache, unneeded packages, journal: run via the package manager

Package-manager items open a terminal and run `sudo pacman -Sc`,
`paru -Rns`, `apt-get` or `dnf`, so the tool itself asks for confirmation.

### Safety

- Only allow-listed commands run; no `--noconfirm`
- Critical packages and this app's own dependencies are never removed
- Direct deletion stays inside `$HOME`; `.ssh`, `.gnupg`, `.config` refused
- The confirm dialog lists every action; Cancel is the default

### Files

- `disk-cleaner`: the app (scan, safety guard, deletion, GUI)
- `test_disk_cleaner.py`: tests, no GUI and no root
- `disk-cleaner.svg`, `disk-cleaner.desktop`, `install.sh`

## Prerequisites

- Linux desktop, `sudo`, and pacman, apt or dnf
- Python 3.10+
- A terminal emulator (`$TERMINAL`, terminator, gnome-terminal, ...)
- `du`, `find`, `git`
- GTK3 and cairo bindings for Python:
  - Arch: `python-gobject gtk3 python-cairo`
  - Debian/Ubuntu: `python3-gi python3-gi-cairo gir1.2-gtk-3.0`
  - Fedora: `python3-gobject gtk3 python3-cairo`

## Setup

```sh
git clone https://github.com/3tty0n/linux-disk-cleaner.git
cd linux-disk-cleaner
python3 test_disk_cleaner.py   # run the tests
./disk-cleaner --list          # dry run: list candidates, delete nothing
./disk-cleaner                 # run the GUI from the checkout
```

## Install

```sh
./install.sh                   # per user, into ~/.local
PREFIX=/usr/local sudo ./install.sh   # system-wide
```

Start it from the app menu or with `disk-cleaner`.

Uninstall:

```sh
rm ~/.local/bin/disk-cleaner
rm ~/.local/share/applications/disk-cleaner.desktop
rm ~/.local/share/icons/hicolor/scalable/apps/disk-cleaner.svg
```

## License

[MIT](LICENSE) (c) 2026 YUSUKE IZAWA
