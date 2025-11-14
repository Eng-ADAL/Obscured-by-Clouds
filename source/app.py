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

def extract_transform_to_terminal(limit=None, transform=True):
    filepath = "data_raw/raw_data.txt"

    # Extract stage
    extract_results = e.extract_txt(filepath)
    extracted_data = extract_results["data"]
    e_stats = extract_results["stats"]

    # Transform stage
    if transform:
        transform_results = t.transform_all(extracted_data)
        transformed_data = transform_results["data"][:limit]
        t_stats = transform_results["stats"]
    else:
        transform_results = None
        transformed_data = extracted_data[:limit]
        t_stats = None

    console.print(
        Panel(
            f"Source          : [bold]{e_stats['source_file']}[/bold]\n"
            f"Total rows      : [green]{e_stats['total_rows']}[/green]\n"
            f"Malformed rows  : [red]{e_stats['malformed_rows']}[/red]\n"
            f"Extraction Time : [yellow]{e_stats['e_total_time']}[/yellow]\n"
            + (f"\nTransform Time  : [green]{t_stats['t_total_time']}[/green]\n"
               f"Transform End   : [cyan]{t_stats['t_datetime']}[/cyan]" if transform else ""),
#            f"Transform Time  : [green]{t_stats['t_total_time']}[/green]\n"
#            f"Transform End   : [cyan]{t_stats['t_datetime']}[/cyan]",
            title="Stats",
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
        title="Extract Sample",
        border_style="yellow"
        )
        )

    if transform:
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

# Extract and load to CSV file
def el_to_csv():
    """
    Extract Load to CSV file
    """
    raw_path = "data_raw/raw_data.txt"
    file_path = "data_ext/el_csv_data.csv"
    extract_results = e.extract_txt(raw_path)
    data_to_save = extract_results["data"]
    l.load_to_csv(data_to_save, file_path)


# ETL to CSV function
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


# Do ETL to database
def load_to_db():
    raw_path = "data_raw/raw_data.txt"
    extract_results = e.extract_txt(raw_path)
    transform_results = t.transform_all(extract_results["data"])
    data_to_save = transform_results["data"]
    l.to_local_database(data_to_save)
    return l.to_local_database(data_to_save)

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
            ui.print_panel("[green] ETL to Terminal[/green]", style="cyan", title="L&S", center_vertically=True)
            extract_transform_to_terminal()
            ui.r_main() # Press Enter For return main menu"
            input()
            continue

        # [ 10 ] Extract Transform Print to Terminal (only first 10 row)
        if choice == "10":
            u.clr_s()
            ui.header()
            ui.display_menu(ui.main_menu_s10)
            u.wait(2)
            u.clr_s()
            ui.header()
            ui.print_panel("[green] ETL to Terminal First 10 [/green]", style="cyan", title="L&S", center_vertically=True)
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
            ui.print_panel("[green] EL to CSV[/green]", style="cyan", title="L&S", center_vertically=True)
            extract_transform_to_terminal(3,transform=False)
            el_to_csv()
            ui.print_panel("EL complete. Data saved to [green]data_ext/etl_csv_data.csv[/green]", style="green", title="Success", center_vertically=True)
            ui.r_main() # Press Enter For return main menu"
            input()
            continue

        # [ 3 ] Extract Transform Load CSV
        elif choice == "3":
            u.clr_s()
            ui.header()
            ui.display_menu(ui.main_menu_s3)
            u.wait(2)
            u.clr_s()
            ui.header()
            ui.print_panel("[green] ETL to CSV[/green]", style="cyan", title="L&S", center_vertically=True)
            extract_transform_to_terminal(3)
            etl_to_csv()
            ui.print_panel("ETL complete. Data saved to [green]data_ext/etl_csv_data.csv[/green]", style="green", title="Success", center_vertically=True)
            ui.r_main() # Press Enter For return main menu"
            input()
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
            ui.print_panel("[green] ETL to DB[/green]", style="cyan", title="L&S", center_vertically=True)
            # Add Load database function
            extract_transform_to_terminal(3)
            load_results = load_to_db()
            #Need to more clean for now it is OK
            summary = f"✅ Load complete: {load_results['rows_loaded']:,} rows in {load_results['l_total_time']:.2f}s  |  UTC: {load_results['l_datetime']}"
            ui.print_panel(summary, style="green", title="Load Stats")
            ui.print_panel("ETL complete. Data saved to Database \n\nCan reach Adminer at browser -> localhost:8181", style="green", title="Success", center_vertically=True)
            ui.r_main() # Press Enter For return main menu"
            input()
            continue

        # [ 5 ] Send Raw data to AWS S3 bucket
        elif choice == "5":
            """
            Place holder for send raw data to aws s3
            """
            u.clr_s()
            ui.header()
            ui.display_menu(ui.main_menu_s5)
            u.wait(2)
            u.clr_s()
            ui.header()
            ui.print_panel("[green]Raw to S3[/green]", style="cyan", title="L&S", center_vertically=True)
            # Add AWS send raw function
#            extract_transform_to_terminal(3)
            ui.display_menu(ui.coming_s)
            ui.r_main() # Press Enter For return main menu"
            input()
            continue

        # [ 6 ] Send Extracted CSV to AWS S3 bucket
        elif choice == "6":
            """
            Place holder for send extracted csv to aws s3
            """
            u.clr_s()
            ui.header()
            ui.display_menu(ui.main_menu_s6)
            u.wait(2)
            u.clr_s()
            ui.header()
            ui.print_panel("[green]Extracted to S3[/green]", style="cyan", title="L&S", center_vertically=True)
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
            def show_docs():
                doc_cmd = "less documentation.txt"

                if os.environ.get("TMUX"):
                    popup = f'tmux display-popup -E -w 73 -h 90% "bash -c \'clear; {doc_cmd}\'"'
                    os.system(popup)
                else:
                    os.system(f"clear && {doc_cmd}")

#            if sys.platform.startswith("win"):
#                ui.header()
#                ui.warning()
#                u.wait(3)
#                continue
#            else:
#                os.system("less documentation.txt")

        else:
            u.clr_s()
            ui.header()
            ui.warning()
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
