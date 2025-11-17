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
    date

# Flush stdin (input)
def flush_stdin():
    termios.tcflush(sys.stdin, termios.TCIFLUSH)

# Arcade mode key press and no need enter go!
def get_keypress():
    """Capture a single keypress (no Enter, no echo)."""
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
    doc_cmd = "less documentation.txt"
    if sys.platform.startswith("win"):
        ui.header()
        ui.warning()
        wait(2.5)
    else:
        os.system(f"clear && {doc_cmd}")


