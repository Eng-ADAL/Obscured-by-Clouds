import os
import sys
import time
import select
import random
import termios
import tty

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
╭───┬──────────────────
│ 1   Extract and Transform Print
├───┼─────────────────────────────
│ 2   Extract and Load to CSV file
├───┼────────────────────────────────────
│ 3   Extract Transform and Load to CSV file
╰───┴─────────────────────────────────────────────
"""

main_menu_s1 = """
╭───┬──────────────────
│ 1   ███████████████████████████
├───┼─────────────────────────────
│ 2   Extract and Load to CSV file
├───┼────────────────────────────────────
│ 3   Extract Transform and Load to CSV file
╰───┴─────────────────────────────────────────────
"""

main_menu_s10 = """
╭───┬──────────────────
│ 1   ████# FIRST 10 ROWS #█████
├───┼─────────────────────────────
│ 2   Extract and Load to CSV file
├───┼────────────────────────────────────
│ 3   Extract Transform and Load to CSV file
╰───┴─────────────────────────────────────────────
"""


main_menu_s2 = """
╭───┬──────────────────
│ 1   Extract and Transform Print
├───┼─────────────────────────────
│ 2   ████████████████████████████
├───┼────────────────────────────────────
│ 3   Extract Transform and Load to CSV file
╰───┴─────────────────────────────────────────────
"""

main_menu_s3 = """
╭───┬──────────────────
│ 1   Extract and Transform Print
├───┼─────────────────────────────
│ 2   Extract and Load to CSV file
├───┼────────────────────────────────────
│ 3   ██████████████████████████████████████
╰───┴─────────────────────────────────────────────
"""



warning_symb = """
⠀  ⠀⠀⠀⠀⠀⠀⠀⢀⣤⡶⠿⠿⢶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
  ⠀⠀⠀⠀⠀⠀⠀⢠⡿⠃⠀⠀⠀⠀⠙⢷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀ ⠀⠀⠀⠀⠀⠀⣠⡿⢡⠀⠀⠀⠀⠀⢀⡈⢿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀ ⠀⠀⠀⠀⣰⡟⢠⣿⠀⠀⠀⠀⠀⢸⣷⡈⢻⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀ ⠀⠀⠀⣰⡟⢠⣿⣿⡆⠀⠀⠀⠀⣸⣿⣷⡄⠹⣆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⡿⠁⣰⣿⣿⣿⡇⠀⠀⠀⠀⣿⣿⣿⣿⡄⠹⣷⡀⠀⠀⠀⠀⠀
⠀⠀⠀⢠⡿⠁⣰⣿⣿⣿⣿⣿⠀⠀⠀⢠⣿⣿⣿⣿⣿⣆⠘⣷⡀⠀⠀⠀⠀
⠀⠀⢠⡿⠁⣼⣿⣿⣿⣿⣿⣿⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣆⠘⢿⡄⠀⠀⠀
⠀⣠⡟⢀⣼⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⣧⠈⢿⡄⠀⠀
⢰⡿⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⡟⠛⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠈⣿⡄⠀
⢼⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠆⢸⡇⠀
⠘⣷⣄⠙⠛⠻⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠛⠋⣠⡿⠃⠀
⠀⠈⠉⠛⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠛⠉⠀⠀

  ╭─────────────────────╮
  │ !! Invalid Input !! │
  ╰─────────────────────╯
"""


return_main = """
╭──────────────────────────────────╮
│ Press Enter For return main menu │
╰──────────────────────────────────╯
"
"""

exit_q = """
╭──────────────╮
│ Exit: 0 or q │
╰──────────────╯
"""
# Exit app button
def exit_app():
    align_r = "bottom"
    aligned = Align.right(exit_q, vertical=align_r)
    console.print(aligned, style="bold red")


# warning sign
def warning(center_vertically: bool = False, heigh:int | None = None) -> None:
    align_v = "middle" if center_vertically else "top"
    aligned = Align.center(warning_symb, vertical=align_v)
    console.print(aligned, style="bold red")

# return main menu
def r_main(center_vertically: bool = False, heigh:int | None = None) -> None:
    align_v = "middle" if center_vertically else "top"
    aligned = Align.center(return_main, vertical=align_v)
    console.print(aligned, style="bold green")




# Print main menu
def main_m(center_vertically: bool = False, heigh:int | None = None) -> None:
    align_v = "middle" if center_vertically else "top"
    aligned = Align.center(main_menu, vertical=align_v)
    console.print(aligned, style="bold green")

# Print main selected 1
def main_1(center_vertically: bool = False, heigh:int | None = None) -> None:
    align_v = "middle" if center_vertically else "top"
    aligned = Align.center(main_menu_s1, vertical=align_v)
    console.print(aligned, style="bold green")

# Print main selected 10
def main_10(center_vertically: bool = False, heigh:int | None = None) -> None:
    align_v = "middle" if center_vertically else "top"
    aligned = Align.center(main_menu_s10, vertical=align_v)
    console.print(aligned, style="bold cyan")

# Print main selected 2
def main_2(center_vertically: bool = False, heigh:int | None = None) -> None:
    align_v = "middle" if center_vertically else "top"
    aligned = Align.center(main_menu_s2, vertical=align_v)
    console.print(aligned, style="bold green")

# Print main selected 3
def main_3(center_vertically: bool = False, heigh:int | None = None) -> None:
    align_v = "middle" if center_vertically else "top"
    aligned = Align.center(main_menu_s3, vertical=align_v)
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
    random.seed(42)
    style = random.choice(colors)
    console.clear()
    console.print(Align.center(banner_art, vertical="middle"), style=style)
    console.print("\nPress any key to start or 'D' for Documentation", justify="center")


# Banner disco mode
def banner_fade_random():
    """
    Display banner with fade animation and detect a keypress instantly.
    Returns:
        str | None: Lowercase character pressed, or None if no key.
    """
    sys.stdout.write("\033[?25l") # blank cursor!
    sys.stdout.flush()
    style = random.choice(colors)
    for s in ["dim", "", "bold"]:  # fade effect
        console.clear()
        console.print(
            Align.center(banner_art, vertical="middle"),
            style=f"{s} {style}".strip()
        )
        console.print("\nPress Enter to start or 'D' for Documentation", justify="center")

        # short loop to check for keypress during fade delay
        start = time.time()
        while time.time() - start < 0.40:
            dr, _, _ = select.select([sys.stdin], [], [], 0)
            if dr:
                return sys.stdin.read(1).lower()  # immediate key detection
    # Restore cursor after loop
    sys.stdout.write("\033[?25h") # bring back cursor!
    sys.stdout.flush()
    return None

# Windows OS greeting
def if_win_banner():
    console.clear()
    banner()
    console.print("\nFor Documentation reach out documentation.txt \nOr: github.com/Eng-ADAL/Obscured-by-Clouds\n\nPress enter to run app", justify="center")
    input()

# Welcoming/Greeting screen (Opening)
def unix_banner_loop2():
    """Display animated greeting screen with instant keypress handling."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    u.flush_stdin()

    try:
        tty.setcbreak(fd)  # enable immediate key detection
        while True:
            key = banner_fade_random()  # animate and check key
            if key:
                console.clear()
                if key == "d":
                    os.system("less documentation.txt")
                # regardless of key, prepare to launch main app
                header()
                console.print("Launching app...", style="bold green", justify="center")
                u.wait(1.5)
                break
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # restore terminal

