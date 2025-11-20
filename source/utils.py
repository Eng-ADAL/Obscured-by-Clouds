# OBC utilities utils.py
# utility codes stored here

import os
import datetime
import time

import sys
import termios
import tty
import select

import ui

from rich.console import Console
from rich.panel   import Panel

def clr_s():
    os.system('cls' if os.name == 'nt' else 'clear')

def wait(s):
    time.sleep(s)

def current_t():
    return datetime.utcnow().isoformat()

# Flush stdin (input)
def flush_stdin():
    if sys.platform.startswith("win"):
        return
    try:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    except Exception:
        pass

# Arcade mode key press and no need enter go!
def get_keypress():
    """Capture a single keypress (no Enter, no echo)."""
    if sys.platform.startswith("win"):
        print("For best ap performance please use docker")
    else:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1).lower()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


# Show documentation floating window else show in less
def show_docs():
    doc_path = "documentation.txt"
    if not os.path.exists(doc_path):
        print("Documentation not found")
        return
    try:
        if sys.platform.startswith("win"):
            with open(doc_path, encoding="utf-8") as f:
                print(f.read())
        else:
            # safer subprocess call
            subprocess.run(["less", doc_path])
    except Exception as e:
        print(f"Error showing documentation: {e}")

