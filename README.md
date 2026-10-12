# disk-cleaner

GTK3 GUI (PyGObject) to find and delete disposable files on an Arch machine:
`~/.cache/*`, paru build dirs (`clone/*/{src,pkg}` only), trash, npm/cargo caches,
pacman cache (`pacman -Sc`), journal (vacuum to 200M), and files over 500MB in `$HOME`.
Nothing is pre-selected; deletion is permanent after a confirmation dialog. Root actions use `pkexec`.

```sh
./install.sh            # ~/.local/bin + desktop entry
disk-cleaner            # GUI
disk-cleaner --list     # print candidates, no GUI
```
