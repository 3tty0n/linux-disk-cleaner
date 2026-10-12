#!/bin/sh
set -e
cd "$(dirname "$0")"
install -Dm755 disk-cleaner "$HOME/.local/bin/disk-cleaner"
install -Dm644 disk-cleaner.desktop "$HOME/.local/share/applications/disk-cleaner.desktop"
