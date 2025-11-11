# Main app local entry point for OBC

import sys
import os
import extract as e
import transform as t
import load as l
import utils as u
import ui

from rich.console import Console
from rich.panel import Panel

console = Console()

def extract_transform_to_terminal(limit=None):
    filepath = "data_raw/raw_data.txt"

    # Extract stage
    extract_results = e.extract_txt(filepath)
    extracted_data = extract_results["data"]
    e_stats = extract_results["stats"]

    # Transform stage
    transform_results = t.transform_all(extracted_data)
    transformed_data = transform_results["data"][:limit]
    t_stats = transform_results["stats"]

    console.print(
        Panel(
            f"Source          : [bold]{e_stats['source_file']}[/bold]\n"
            f"Total rows      : [green]{e_stats['total_rows']}[/green]\n"
            f"Malformed rows  : [red]{e_stats['malformed_rows']}[/red]\n"
            f"Extraction Time : [yellow]{e_stats['e_total_time']}[/yellow]\n"
            f"Transform Time  : [green]{t_stats['t_total_time']}[/green]\n"
            f"Transform End   : [cyan]{t_stats['t_datetime']}[/cyan]",
            title="ETL Stats",
            border_style="bright_magenta",
        )
    )

    elines = []
    for i, eline in enumerate(extracted_data[:3], start = 1):
        # Only include non-PII fields
        safe_line = {
            k: v for k, v in eline.items() if k not in ["Customer Name", "Card Number"]
        }
        formatted = f"{i}.{safe_line}"
        elines.append(formatted)
    print("\n\n")
    extract_table = "\n".join(elines)

    info = ("\n\n          (Only first 3 lines for sanity check | PII dropped):")

    console.print(
            Panel(
        f"{extract_table}{info}",
#        f"{formatted}{info}",
        title="Extract Sample",
        border_style="yellow"
        )
        )

    # Field Names (CSV Headers)
    header = f"{'No.':<4}{'Drink':<11}{'Price':<7}{'Branch':<10}{'Payment':<9}{'Bank':<5}{'Date/Time':<10}{'TxID':<6}{'CustHash'}"
    lines = [header, "." * (len(header)+2)]
    for i, row in enumerate(transformed_data, start=1):
        txid_short = row['Transaction ID'][:4] + ".."
        hash_short = row['Customer Hash'][:5] + ".."
        dt_short = row['Date/Time'][:10]

        line = (
            f"{i:<4}"
            f"{row['Drink']:<11}"
            f"{row['Price']:<7}"
            f"{row['Branch']:<11}"
            f"{row['Payment Type']:<7}"
            f"{row['Bank Prefix']:<6}"
            f"{dt_short:<12}"
            f"{txid_short:<7}"
            f"{hash_short}"
        )
        lines.append(line)

    transform_table = "\n".join(lines)
    console.print(Panel(transform_table, title="Transformed Data", border_style="cyan"))

def el_to_csv():
    """
    Extract Load to CSV file
    """
    raw_path = "data_raw/raw_data.txt"
    file_path = "data_ext/el_csv_data.csv"
    extract_results = e.extract_txt(raw_path)
    data_to_save = extract_results["data"]
    l.load_to_csv(data_to_save, file_path)
    print(f"EL complete. Data saved to {file_path}")


def etl_to_csv():
    """
    Extract Transform and Load to CSV file
    """
    raw_path = "data_raw/raw_data.txt"
    file_path = "data_ext/etl_csv_data.csv"
    extract_results = e.extract_txt(raw_path)
    transform_results = t.transform_all(extract_results["data"])
    data_to_save = transform_results["data"]
    l.load_to_csv(data_to_save, file_path)
    print(f"ETL complete. Data saved to {file_path}")


def main():
    u.clr_s()
#    add sys if else if not unix print
    if sys.platform.startswith("win"):
        ui.if_win_banner()
    else:
         ui.unix_banner_loop2()

    while True:
        u.clr_s()
        ui.header()
        ui.display_menu(ui.main_menu)
        ui.exit_app()
        choice = input("Please select: ")

        # [ 1 ] Extract Transform Print to Terminal
        if choice == "1":
            u.clr_s()
            ui.header()
            ui.display_menu(ui.main_menu_s1)
            u.wait(2)
            u.clr_s()
            ui.header()
            extract_transform_to_terminal()
            input("\n Press Enter For return main menu")
            continue

        # [ 10 ] Extract Transform Print to Terminal (only first 10 row)
        if choice == "10":
            u.clr_s()
            ui.header()
            ui.display_menu(ui.main_menu_s10)
            u.wait(2)
            u.clr_s()
            ui.header()
            extract_transform_to_terminal(10)
            ui.r_main() # Press Enter For return main menu"
            input()
            continue

        # [ 2 ] Extract Transform Load CSV
        elif choice == "2":
            u.clr_s()
            ui.header()
            ui.display_menu(ui.main_menu_s2)
            u.wait(2)
            u.clr_s()
            ui.header()
            extract_transform_to_terminal(3)
            el_to_csv()
            input("\n Press Enter For return main menu")
            continue

        # [ 3 ] Extract Transform Load CSV
        elif choice == "3":
            u.clr_s()
            ui.header()
            ui.display_menu(ui.main_menu_s3)
            u.wait(2)
            u.clr_s()
            ui.header()
            extract_transform_to_terminal(3)
            etl_to_csv()
            input("\n Press Enter For return main menu")
            continue

        # [ 4 ] Extract Transform Load to Data Base
        elif choice == "4":
            """
            Place holder for load database
            """
            u.clr_s()
            ui.header()
            ui.display_menu(ui.main_menu_s4)
            u.wait(2)
            u.clr_s()
            ui.header()
            # Add Load database function
            extract_transform_to_terminal(3)
            ui.r_main() # Press Enter For return main menu"
            input()
            continue

        # [ 5 ] Extract Transform Load to Data Base
        elif choice == "5":
            """
            Place holder for load database
            """
            u.clr_s()
            ui.header()
            ui.display_menu(ui.main_menu_s5)
            u.wait(2)
            u.clr_s()
            ui.header()
            # Add AWS send raw function
#            extract_transform_to_terminal(3)
            ui.display_menu(ui.coming_s)
            ui.r_main() # Press Enter For return main menu"
            input()
            continue

        # [ 6 ] Extract Transform Load to Data Base
        elif choice == "6":
            """
            Place holder for load database
            """
            u.clr_s()
            ui.header()
            ui.display_menu(ui.main_menu_s6)
            u.wait(2)
            u.clr_s()
            ui.header()
            # Add AWS EL then send function
#            extract_transform_to_terminal(3)
            ui.display_menu(ui.coming_s)
            ui.r_main() # Press Enter For return main menu"
            input()
            continue




        elif choice in ["0", "q"]:
            u.clr_s()
            ui.banner()
            exit()

        # Documentation page in main menu
        elif choice in ["d", "D"]:
            u.clr_s()
            if sys.platform.startswith("win"):
                ui.header()
                ui.warning()
                print("Please input [0-3]")
                u.wait(3)
                continue
            else:
                os.system("less documentation.txt")

        else:
            u.clr_s()
            ui.header()
            ui.warning()
            print("Please input [0-3]")
            u.wait(3)
            continue

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        u.clr_s()
        ui.banner()
        print("\n\n\nKeyboard interrupt\n\nThank you for using L&S products\n")
        exit()
    try:
        main()
    except Exception as e:
        print(f"Error {e}")
        exit()
