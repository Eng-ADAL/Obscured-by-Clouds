# OBS extract.py
# extracts text files

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
        for line in f:
            line = line.strip()
            # Skip empty lines
            if not line or all(not cell.strip() for cell in line):
                 count_empty_rows += 1
                 continue

            parts = line.split(" ") #split by coma
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

    summary = {
            "total_rows" : count_total_rows,
            "malformed_rows" : count_malformed_rows,
            "empty_rows" : count_empty_rows,
            "source_file": filepath,
#            "extraction_time" : good idea for metadata
            }
    return {
            "data" : rows,
            "stats" : summary
            }


