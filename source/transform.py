# OBS transform.py
# Transform extracted files
# 🜂

"""
Sample data:

{'Customer Name': 'Carol', 'Drink': 'Macchiato', 'Price': '£4.50', 'Branch': 'Guildford', 'Payment Type': 'Cash', 'Card Number': '9528512', 'Date/Time': '05/12/2024'}
"""



import uuid
from datetime import datetime


def hash_pii_fields(customer_name):
    """
    Hashing Customer Name
    """
    return hash(customer_name)


def drop_card(card_number):
    """
    Keep the first 4 digits of the card number to identify the bank.
    """
    return card_number[:4]
def to_iso8601(datetime_str):
    """
    Convert string datatime to iso8601 format
    DD/MM/YYYY to YYYY-MM-DDTHH:MM:SS

    Example:
    05/12/2024 ➜ 2024-12-05T00:00:00
    """
    dt = datetime.strptime(datetime_str, "%d/%m/%Y")
    return dt.strftime("%Y-%m-%dT%H:%M:%S")

