# OBS transform.py
# Transform extracted files
# 🜂

"""
Sample data:

{'Customer Name': 'Carol', 'Drink': 'Macchiato', 'Price': '£4.50', 'Branch': 'Guildford', 'Payment Type': 'Cash', 'Card Number': '9528512', 'Date/Time': '05/12/2024'}
"""


#import pandas #revisit transform_all function
import uuid
import hashlib
from datetime import datetime
import re
from decimal import Decimal
import time


def transaction_uuid(transaction_id):
    return str(uuid.uuid4())


def hash_pii_fields(customer_name):
    """
    Hashing Customer Name
    """
    return hashlib.sha256(customer_name.strip().encode()).hexdigest()


def drop_card(card_number):
    """
    Keep the first 4 digits of the card number to identify the bank.
    """
    return card_number[:4] if card_number else None

def to_iso8601(datetime_str):
    """
    Convert string datatime to iso8601 format
    DD/MM/YYYY to YYYY-MM-DDTHH:MM:SS

    Example:
    05/12/2024 ➜ 2024-12-05T00:00:00
    """
    dt = datetime.strptime(datetime_str, "%d/%m/%Y")
    return dt.strftime("%Y-%m-%dT%H:%M:%S")

def decimal_price(price):
    """
    remove currency sign (£) and transform it integer
    """
    p_price = re.sub(r'[£$€?]', '', price)
    dec_price = Decimal(p_price)
    return dec_price


def transform_all(rows):
    """
    Apply transformations to each extracted row.
    """
    start_transform = time.perf_counter() # Starts transfrom time counter
    transformed = []

    for r in rows:
        customer_hash = hash_pii_fields(r["Customer Name"])
        card_prefix = drop_card(r["Card Number"])
        iso_date = to_iso8601(r["Date/Time"])
        transaction_id = str(uuid.uuid4())
        price = decimal_price(r["Price"])
        row = {
            "Transaction ID": transaction_id,
            "Customer Hash": customer_hash,
            "Drink": r["Drink"],
            "Price": price,
            "Branch": r["Branch"],
            "Payment Type": r["Payment Type"],
            "Bank Prefix": card_prefix,
            "Date/Time": iso_date,
        }

        transformed.append(row)

    end_transform = time.perf_counter()                 # End transform time
    transform_time = end_transform - start_transform    # Total Transfrom time
    transform_end_time = datetime.utcnow()

    summary = {
            "t_total_time" : transform_time,
            "t_datetime" : transform_end_time
             }

    return {
            "data" : transformed,
            "stats" : summary
            }
