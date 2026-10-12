"""python3 test_disk_cleaner.py  (no GUI, no root; touches only temp dirs under $HOME)"""
import importlib.machinery, importlib.util, os, shutil, stat, tempfile

here = os.path.dirname(os.path.abspath(__file__))
loader = importlib.machinery.SourceFileLoader("dc", os.path.join(here, "disk-cleaner"))
dc = importlib.util.module_from_spec(importlib.util.spec_from_loader("dc", loader))
loader.exec_module(dc)
H = dc.HOME


def refused(target, kind="rm"):
    try:
        dc.check_safe(target, kind)
    except dc.Refused:
        return True
    return False


# --- safety guard: dangerous deletions are refused
for bad in ["/", "/etc", "/usr/bin/ls", H, os.path.join(H, ".ssh"), os.path.join(H, ".config"), dc.CACHE,
            os.path.join(H, ".cache", ".."), os.path.join(H, "Documents")]:
    assert refused(bad), bad
    assert refused(bad, "clear"), bad
assert not refused(os.path.join(H, ".cache", "somecache"), "clear")
assert refused(os.path.join(H, ".cache/x") + "\n/etc")  # one bad path poisons the whole row

# --- commands: only allow-listed ones run
for ok in ["sudo pacman -Sc", "sudo journalctl --vacuum-size=200M", "paru -Rns $(pacman -Qdtq)", "yay -Rns foo-bin",
           "sudo pacman -Rns libfoo++", "sudo apt-get autoremove --purge", "sudo apt-get remove libc6:amd64",
           "sudo dnf clean all", "sudo dnf remove python3-foo"]:
    assert dc.ALLOWED_CMD.fullmatch(ok), ok
for bad in ["sudo rm -rf /", "sudo pacman -Sc --noconfirm", "sudo pacman -Rns foo; rm -rf ~", "sudo pacman -Rdd glibc",
            "sudo pacman -Rns -dd x", "sudo pacman -Rns $(rm -rf ~)", "sudo apt-get remove x y", "rm -rf /"]:
    assert refused(bad, "cmd"), bad

# --- explaining failures
i = dc.issue("pacman package cache", "error: failed to init transaction (unable to lock database)")
assert "Another package manager" in i.cause, i
i = dc.issue("x", "[Errno 13] Permission denied: '/etc/hostname'", "/etc/hostname")
assert "owned by 'root'" in i.cause, i
i = dc.issue("x", "sudo: a password is required")
assert "sudo" in i.cause
r = dc.run_job(dc.Row("evil", "/etc/hostname", 1, "rm", ""))
assert r and "safety guard" in r[0].cause, r

# --- deletion: dir contents emptied (dir kept); unreadable (mode 311) and read-only trees removed
t = tempfile.mkdtemp(dir=H)
try:
    os.makedirs(f"{t}/c/ro/sub"); os.makedirs(f"{t}/pkg/a/b")
    open(f"{t}/c/f", "w").close(); open(f"{t}/c/ro/sub/x", "w").close(); open(f"{t}/pkg/a/b/f", "w").close()
    os.chmod(f"{t}/c/ro/sub", 0o555); os.chmod(f"{t}/c/ro", 0o555)
    os.chmod(f"{t}/pkg/a/b", 0o555); os.chmod(f"{t}/pkg", 0o311)
    assert dc.run_job(dc.Row("c", f"{t}/c", 1, "clear", "")) == []
    assert os.path.isdir(f"{t}/c") and not os.listdir(f"{t}/c")
    assert dc.run_job(dc.Row("pkg", f"{t}/pkg", 1, "rm", "")) == [] and not os.path.exists(f"{t}/pkg")
finally:
    shutil.rmtree(t, ignore_errors=True)

# --- terminal command failure surfaces its stderr (fake terminal runs the command directly)
fake = tempfile.mkdtemp()
try:
    with open(f"{fake}/xterm", "w") as f:
        f.write('#!/bin/sh\nshift\nexec "$@" </dev/null\n')
    os.chmod(f"{fake}/xterm", 0o755)
    os.environ.update(PATH=f"{fake}:{os.environ['PATH']}", TERMINAL="xterm")
    dc.run_in_terminal("true")
    try:
        dc.run_in_terminal("echo 'error: unable to lock database' >&2; exit 1")
        raise SystemExit("expected CmdError")
    except dc.CmdError as e:
        assert "unable to lock database" in str(e) and e.rc == 1
        assert "Another package manager" in dc.issue("c", str(e)).cause
finally:
    shutil.rmtree(fake, ignore_errors=True)
# --- donut layout never indexes past the palette, whatever the number of rows (was an IndexError at 8 rows)
pal = dc.PALETTE["dark"]
for n in range(0, 25):
    rows = [(False, f"r{k}", 1000 - k, "", "", "") for k in range(n)]
    sl = dc.pie_slices(rows, pal)
    assert len(sl) <= len(pal) + 1 and sum(x["size"] for x in sl) == sum(r[2] for r in rows), n
    assert all(len(x["rows"]) == 1 for x in sl[:len(pal)]), n

txt = dc.issues_text([i])
assert "What happened" in txt and "Likely cause" in txt and "What to do" in txt
print("all tests passed")
