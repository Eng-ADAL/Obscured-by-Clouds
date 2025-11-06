# OBS extract.py
# extracts text files

import time
from datetime import datetime

def extract_txt(filepath):
    """
    Extracts raw *.txt files

    Example data:
    Customer Name, Drink, Price, Branch, Payment Type, Card Number, Date/Time
    Dave  “Latte  2  £3.50”  Epsom  Card  0123456  12/08/2024
    """

    rows = []
    count_total_rows = 0
    count_malformed_rows = 0
    count_empty_rows = 0
    # Open file and fix BOM encoding ("utf-8-sig")
    with open(filepath, "r", encoding="utf-8-sig") as f:
        start_extract = time.perf_counter() # Strarts extract starts counter
        for line in f:
            line = line.strip()
            # Skip empty lines
            if not line or all(not cell.strip() for cell in line):
                 count_empty_rows += 1
                 continue

            parts = line.split(" ")
            if len(parts) != 7 :
                count_malformed_rows += 1
            # further improvement add log for malformed and empty lines
                continue # malformed row skip

            try:
                customer_name   = parts[0].strip()
                drink           = parts[1].strip()
                price           = parts[2].strip()
                branch          = parts[3].strip()
                payment_type    = parts[4].strip()
                card_number     = parts[5].strip()
                datetime_str    = parts[6].strip()

            except Exception:
                count_malformed_rows += 1

            row = {
                    "Customer Name" : customer_name,
                    "Drink"         : drink,
                    "Price"         : price,
                    "Branch"        : branch,
                    "Payment Type"  : payment_type,
                    "Card Number"   : card_number,
                    "Date/Time"     : datetime_str,
                  }
            rows.append(row)
            count_total_rows += 1

    end_extract = time.perf_counter() # End extract starts counter
    extract_total_time = end_extract - start_extract
    extract_end_time = datetime.utcnow()

    summary = {
            "total_rows" : count_total_rows,
            "malformed_rows" : count_malformed_rows,
            "empty_rows" : count_empty_rows,
            "source_file": filepath,
            "e_total_time" : extract_total_time,
            "e_datetime" : extract_end_time
            }

    return {
            "data" : rows,
            "stats" : summary
            }


