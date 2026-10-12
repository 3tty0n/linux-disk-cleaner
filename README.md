# disk-cleaner

GTK3 GUI (PyGObject + cairo, no other deps) to find and delete disposable files on an Arch machine.
A donut chart shows what takes the space (top 7 + "Other"; click a slice or a row to select, selected slices pop out),
next to a sortable list and a `/` usage bar. Nothing is pre-selected.

| Candidate | How it is removed |
|---|---|
| `~/.cache/*`, npm/cargo caches, trash (`files/`+`info/`) | contents emptied, directory kept |
| paru clones: untracked files only (`src/`, `pkg/`, sources, built packages) | deleted; PKGBUILD + `.git` kept |
| files over 500MB in `$HOME` | deleted (permanent, after a confirmation dialog) |
| pacman cache, orphan packages, packages owning a big file, systemd journal | **never unlinked directly**: run in a terminal as `sudo pacman -Sc` / `paru -Rns …` / `sudo journalctl --vacuum-size=…`, so pacman/paru/sudo ask for confirmation |

Terminal: `$TERMINAL`, else the first of terminator, xfce4-terminal, alacritty, kitty, xterm.

```sh
./install.sh            # ~/.local/bin + desktop entry
disk-cleaner            # GUI
disk-cleaner --list     # print candidates, no GUI
```
