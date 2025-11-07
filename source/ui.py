from rich.console   import Console
from rich.panel     import Panel
from rich.align     import Align
from rich.layout    import Layout

console = Console()

header_art ="""
 ╬═════════════════════════════════════════════╗
 ║ │  Ｏｂｓｃｕｒｅｄ ｂｙ  Ｃｌｏｕｄｓ      ║│
 ║░│░λ░░░░░░░░░░░░░░░░░░░░░░░░░▒▒▒▒▒▒▒▒███████ ║││
 ╬═╪═══════════════════════════════════════════╬╡│

"""

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


def header(center_vertically: bool = False, height:int | None = None) -> None:
    align_v = "middle" if center_vertically else "top"
    aligned = Align.center(header_art, vertical=align_v)
    console.print(aligned,style="bold cyan")


def banner():
    aligned_banner = Align.center(banner_art, vertical="middle")
    console.print(aligned_banner, style="bold cyan")

