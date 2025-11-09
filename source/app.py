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
    stats = extract_results["stats"]

    console.print(
        Panel(
            f"ETL Pipeline: Running...\n\n"
            f"Source: [bold]{stats['source_file']}[/bold]\n"
            f"Total rows: [green]{stats['total_rows']}[/green]\n"
            f"Malformed: [red]{stats['malformed_rows']}[/red]",
            title="Status",
            border_style="bright_magenta",
        )
    )

    elines = []
    for i, eline in enumerate(extracted_data[:3], start = 1):
        formatted = f"{i}.{eline}"
        elines.append(formatted)

    print("\n\n")
    extract_table = "\n".join(elines)

    info = ("\n\n          (Only first 3 lines for sanity check | PII dropped):")

    console.print(
            Panel(
        f"{extract_table}{info}",
        title="Extract Sample",
        border_style="yellow"
        )
        )

    # Transform stage
    transfrom_results = t.transform_all(extracted_data)
    transformed_data = transfrom_results["data"]

    if limit is not None:
        transformed_data = transformed_data[:limit]

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
        # Place holder for cli-gui
        u.clr_s()
        ui.header()
        ui.main_m()
        ui.exit_app()
        choice = input("Please select: ")

        if choice == "1":
            u.clr_s()
            ui.header()
            ui.main_1()
            u.wait(2)
            u.clr_s()
            ui.header()
            extract_transform_to_terminal()
            input("\n Press Enter For return main menu")
            continue

        if choice == "10":
            u.clr_s()
            ui.header()
            ui.main_10()
            u.wait(2)
            u.clr_s()
            ui.header()
            extract_transform_to_terminal(10)
            input("\n Press Enter For return main menu")
            continue


        elif choice == "2":
            u.clr_s()
            ui.header()
            ui.main_2()
            u.wait(2)
            u.clr_s()
            ui.header()
            el_to_csv()
            input("\n Press Enter For return main menu")
            continue

        elif choice == "3":
            u.clr_s()
            ui.header()
            ui.main_3()
            u.wait(2)
            u.clr_s()
            ui.header()
            etl_to_csv()
            input("\n Press Enter For return main menu")
            continue

        elif choice in ["0", "q"]:
            u.clr_s()
            ui.banner()
#            print("\n\n\n\nThank you for using L&S products!\n\n\n\n")
            exit()

        # Documentation page in main menu
        elif choice in ["d", "D"]:
            u.clr_s()
            if sys.platform.startswith("win"):
                ui.warning()
                print("Please input [0-3]")
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
