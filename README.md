# disk-cleaner

Desktop app (GTK3 + PyGObject + cairo) to find and delete disposable files on Linux: Arch (pacman, paru/yay),
Debian/Ubuntu (apt) and Fedora (dnf). A donut chart shows what takes the space (top 7 + "Other"; click a slice or a
row to select, selected slices pop out), next to a sortable list and a `/` usage bar. Nothing is pre-selected.

| Candidate | How it is removed |
|---|---|
| `$XDG_CACHE_HOME/*` (`~/.cache`), npm/cargo caches, trash (`files/`+`info/`) | contents emptied, directory kept |
| paru clones: untracked files only (`src/`, `pkg/`, sources, built packages) | deleted; PKGBUILD + `.git` kept |
| files over 500MB in `$HOME` | deleted (permanent) after a confirmation dialog, with a ⚠ note |
| package cache, unneeded packages, packages owning a big file, systemd journal | **never unlinked directly**: run in a terminal as `sudo pacman -Sc` / `paru -Rns …` / `sudo apt-get autoremove --purge` / `sudo dnf remove …` / `sudo journalctl --vacuum-size=…`, so the package manager/sudo ask for confirmation |

## Safety
- Only an allow-list of commands can run (`ALLOWED_CMD`); no `--noconfirm`, no `-dd`, no free-form shell.
- Direct deletion is limited to paths inside `$HOME`; `$HOME` itself, `~/.ssh`, `~/.gnupg`, `~/.config`, `~/.local`,
  `~/Documents` and friends, the cache/data roots and mount points are refused (symlinks are resolved first).
- Big files owned by a package, critical packages (base/essential/kernel), and the packages this program runs on are
  never offered; files under `~/.ssh`, `~/.gnupg`, `~/.config`, `~/.local` are not offered either.
- The confirmation dialog lists what is deleted now vs. run in a terminal, plus ⚠ warnings; Cancel is the default.

## Problems
Nothing is printed on the CLI. Failed deletions/commands and unreadable paths are analysed and shown in the GUI
(what happened / likely cause / what to do), e.g. root-owned files, unwritable parent dirs, stale pacman locks, sudo failures.
The "⚠ Problems (N)" button re-opens them.

## Install
```sh
./install.sh            # ~/.local/{bin,share} + icon + desktop entry; PREFIX=/usr/local sudo ./install.sh for system-wide
disk-cleaner            # GUI (or launch "Disk Cleaner" from the app menu)
disk-cleaner --list     # print candidates, no GUI
python3 test_disk_cleaner.py
```
Dependencies: `python-gobject gtk3 python-cairo` (Arch) · `python3-gi python3-gi-cairo gir1.2-gtk-3.0` (Debian/Ubuntu) ·
`python3-gobject gtk3 python3-cairo` (Fedora). A terminal emulator (`$TERMINAL`, terminator, xfce4-terminal,
gnome-terminal, konsole, alacritty, kitty, foot, xterm) is needed for package-manager actions.
