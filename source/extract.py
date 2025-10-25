# OBS extract.py
# extracts text files

def extract_txt(lines)
    """
    Extracts raw *.txt files
    Example data:

    Customer Name, Drink, Price, Branch, Payment Type, Card Number, Date/Time
    Dave  “Latte  2  £3.50”  Epsom  Card  0123456  12/08/2024
    """
    with open(/data_raw/*.txt)
    row = []
    count_total_rows = 0
    count_malformed_rows = 0

    reader = readline(lines)

        for line in reader:
            # Skip empty lines
            if not line or all(not cell.strip() for cell in line):
                continue

            if len(line) != 7 :
            # malformed row skip
            # further improvement add log for malformed and empty lines

            try:
                count_total_rows += 1
                customer_name = line[0].strip()
                drink = line[1].strip()
                price = line[2].strip()
                branch = line[3].strip()
                payment_type = line[4].strip()
                card_number = line[5].strip()
                datetime_str = line[6].strip()
            except Exception as e:
                count_malformed_rows += 1
                continue


