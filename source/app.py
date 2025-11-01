# Main app local entry point for OBC

import extract as e
import transform as t
import load as l

from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
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

    print("\n\nExtracted sample (first 3 lines for sanity check):\n")
    print("-" * 72)
    for eline in enumerate(extracted_data[:3]):
        print(eline)

    print("-" * 72)
    print("\n\n")

    # Transform stage
    transformed_data = t.transform_all(extracted_data)

    # Header
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
    console.print(Panel(transform_table, title="Transform Sample", border_style="cyan"))
    # Load stage (placeholder)


if __name__ == "__main__":
    main()



