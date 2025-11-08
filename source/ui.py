import os
import sys
import time
import select
import random

from rich.console   import Console
from rich.panel     import Panel
from rich.align     import Align
from rich.layout    import Layout
from rich.text      import Text

import utils as u

console = Console()

header_art ="""
 ││╬═════════════════════════════════════════════╗
  │║ │  Ｏｂｓｃｕｒｅｄ  ｂｙ  Ｃｌｏｕｄｓ     ║│
   ║░│░λ░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒█████████████ ║││
   ╬═╪═══════════════════════════════════════════╬╡│

"""

banner_p = ("""

    ████████████████████████████████████████████████
    ██ ╔══════════════════════════════════════════██═╗░░░░░
    ██ ║ ╭────────────────────────────────────────██─║─╮ ░░
    ██ ║ │                                        ██ ║ │ ░░
    ██ ║ │    ██████╗     ██████╗      ██████╗    ██ ║ │ ░░
    ██ ║ │   ██╔═══██╗    ██╔══██╗    ██╔════╝    ██ ║ │ ░░
    ██ ║ │   ██║   ██║    ██████╔╝    ██║         ██ ║ │ ░░
    ██ ║ │   ██║   ██║    ██╔══██╗    ██║         ██ ║ │ ▒▒
    ██ ║ │   ╚██████╔╝    ██████╔╝    ╚██████╗    ██ ║ │ ▒▒
    ██ ║ │    ╚═════╝     ╚═════╝      ╚═════╝    ██ ║ │ ▒▒
    ██ ║ │                                        ██ ║ │ ▓▓
    ██ ║ │  Ｏｂｓｃｕｒｅｄ ｂｙ  Ｃｌｏｕｄｓ   ██ ║ │ ▓▓
    ████████████████████████████████████████████████ ║ │ ▓▓
     ░░ ╚╪═══════════════════════════════════════════╝ │ ▓▓
     ░░  ╰─────────────────────────────────────────────╯ ██
     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▓▓▓▓▓▓▓▓███
""")


banner_art = ("""

    ████████████████████████████████████████████████
    ██ ╔══════════════════════════════════════════██═╗░░░░░
    ██ ║ ╭────────────────────────────────────────██─║─╮ ░░
    ██ ║ │                                        ██ ║ │ ░░
    ██ ║ │    ██████╗     ██████╗      ██████╗    ██ ║ │ ░░
    ██ ║ │   ██╔═══██╗    ██╔══██╗    ██╔════╝    ██ ║ │ ░░
    ██ ║ │   ██║   ██║    ██████╔╝    ██║         ██ ║ │ ░░
    ██ ║ │   ██║   ██║    ██╔══██╗    ██║         ██ ║ │ ▒▒
    ██ ║ │   ╚██████╔╝    ██████╔╝    ╚██████╗    ██ ║ │ ▒▒
    ██ ║ │    ╚═════╝     ╚═════╝      ╚═════╝    ██ ║ │ ▒▒
    ██ ║ │                                        ██ ║ │ ▓▓
    ██ ║ │  Ｏｂｓｃｕｒｅｄ ｂｙ  Ｃｌｏｕｄｓ   ██ ║ │ ▓▓
    ████████████████████████████████████████████████ ║ │ ▓▓
     ░░ ╚╪═══════════════════════════════════════════╝ │ ▓▓
     ░░  ╰─────────────────────────────────────────────╯ ██
     ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▓▓▓▓▓▓▓▓███

               Local And Cloud Automation Tool

                  (OBC is a L&S procudct ©)
 """)

main_menu = """
╭───┬──
│ 1   Extract and Transform Print
├───┼───────────────────────────────
│ 2   Extract and Load to CSV file
├───┼─────────────────────────────────────
│ 3   Extract Transform and Load to CSV file
╰───┴─────────────────────────────────────────────
"""

exit_q = """
╭──────────────╮
│ Exit: 0 or q │
╰──────────────╯
"""

def exit_app():
    align_r = "bottom"
    aligned = Align.right(exit_q, vertical=align_r)
    console.print(aligned, style="bold red")

# Print main menu
def main_m(center_vertically: bool = False, heigh:int | None = None) -> None:
    align_v = "middle" if center_vertically else "top"
    aligned = Align.center(main_menu, vertical=align_v)
    console.print(aligned, style="bold green")

# Print header aligned center
def header(center_vertically: bool = False, height:int | None = None) -> None:
    align_v = "middle" if center_vertically else "top"
    aligned = Align.center(header_art, vertical=align_v)
    console.print(aligned,style="bold cyan")

# Print plain banner aligned center (colour cyan)
def banner():
    aligned_banner = Align.center(banner_art, vertical="middle")
    console.print(aligned_banner, style="bold cyan")

# Banner cyan
def banner_c():
    console.clear()
    console.print(Align.center(banner_p, vertical="middle"), style="bold cyan")
    console.print("\nPress any key to start or 'D' for Documentation", justify="center")

# Banner yellow
def banner_y():
    console.clear()
    console.print(Align.center(banner_p, vertical="middle"), style="yellow")
    console.print("\nPress any key to start or 'D' for Documentation", justify="center")


# Banner colour loop cyan and yellow
def unix_banner_loop():
    banners = [banner_c, banner_y]
    i = 0
    last_change = time.time()
    banners[i]()

    while True:
        if time.time() - last_change > 1.5:
            i = (i + 1) % 2
            banners[i]()
            last_change = time.time()

        dr, _, _ = select.select([sys.stdin], [], [], 0.1)
        if dr:
            key = sys.stdin.read(1).lower()
            if key == "d":
                console.clear()
                console.print(open("documentation.txt").read())
            else:
                console.clear()
                console.print("Launching app...", style="bold green")
            break


# random colour picker for banner
colors = ["bold cyan", "yellow", "magenta", "green", "bright_blue", "bright_red"]
def banner_random():
    style = random.choice(colors)
    console.clear()
    console.print(Align.center(banner_art, vertical="middle"), style=style)
    console.print("\nPress any key to start or 'D' for Documentation", justify="center")


# Banner disco mode
def banner_fade_random():
    style = random.choice(colors)
    for s in ["dim", "", "bold"]:  # fade illusion
        console.clear()
        console.print(Align.center(banner_art, vertical="middle"), style=f"{s} {style}".strip())
        console.print("\nPress any key to start or 'D' for Documentation", justify="center")
        time.sleep(0.25)  # quick fade illusion

# Windows OS greeting
def if_win_banner():
    console.clear()
    banner()
    console.print("\nFor Documentation reach out documentation.txt \nOr: github.com/Eng-ADAL/Obscured-by-Clouds\n\nPress enter to run app", justify="center")
    input()

# Welcoming/Greeting screen (Opening)
def unix_banner_loop2():
    last_change = time.time()
    banner_fade_random()  # initial display

    while True:
        if time.time() - last_change > 2.5:
            banner_fade_random()
            last_change = time.time()

        dr, _, _ = select.select([sys.stdin], [], [], 0.1)
        if dr:
            key = sys.stdin.read(1).lower()
            # less Documentation
            if key == "d":
                console.clear()
                os.system("less documentation.txt")
                header()
                console.print("Launching app...", style="bold green",justify="center")
                u.wait(1.5)
            else:
                console.clear()
                header()
                console.print("Launching app...", style="bold green",justify="center")
                u.wait(1.5)
            break

