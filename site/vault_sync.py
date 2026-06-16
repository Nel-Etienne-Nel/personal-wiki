#!/usr/bin/env python3
"""
Watches the Obsidian vault for changes and auto-pushes to GitHub.
Run once: python3 vault_sync.py
Keep running in the background — it will push whenever you save a note.
"""

import subprocess
import time
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

VAULT = Path("/Users/etienne/Documents/EtienneOBS")
DEBOUNCE_SECONDS = 30   # wait 30s after last change before pushing
IGNORED = {".obsidian", "site", ".git", "__pycache__", ".DS_Store"}


def git(args: list[str]) -> tuple[int, str]:
    result = subprocess.run(
        ["git", "-C", str(VAULT)] + args,
        capture_output=True, text=True
    )
    return result.returncode, result.stdout.strip() + result.stderr.strip()


class VaultHandler(FileSystemEventHandler):
    def __init__(self):
        self._pending = False
        self._last_change = 0.0

    def on_any_event(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        # Skip ignored folders and non-markdown files
        if any(part in IGNORED for part in path.parts):
            return
        if path.suffix not in {".md", ".canvas"}:
            return
        self._pending = True
        self._last_change = time.time()

    def flush_if_ready(self):
        if not self._pending:
            return
        if time.time() - self._last_change < DEBOUNCE_SECONDS:
            return

        self._pending = False
        print(f"\n[sync] Changes detected — committing and pushing...")

        code, out = git(["add", "."])
        if code != 0:
            print(f"[sync] git add failed: {out}")
            return

        timestamp = time.strftime("%Y-%m-%d %H:%M")
        code, out = git(["commit", "-m", f"vault: {timestamp}"])
        if code != 0 and "nothing to commit" in out:
            print("[sync] Nothing new to commit.")
            return
        if code != 0:
            print(f"[sync] git commit failed: {out}")
            return

        code, out = git(["push"])
        if code == 0:
            print(f"[sync] ✓ Pushed to GitHub at {timestamp}")
        else:
            print(f"[sync] Push failed: {out}")


def main():
    print(f"[sync] Watching vault at {VAULT}")
    print(f"[sync] Will push {DEBOUNCE_SECONDS}s after last change. Ctrl+C to stop.\n")

    handler = VaultHandler()
    observer = Observer()
    observer.schedule(handler, str(VAULT), recursive=True)
    observer.start()

    try:
        while True:
            handler.flush_if_ready()
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
        print("\n[sync] Stopped.")

    observer.join()


if __name__ == "__main__":
    main()
