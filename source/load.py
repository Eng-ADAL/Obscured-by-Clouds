import csv
import time
from datetime import datetime
import psycopg2
from psycopg2.extras import execute_values


def load_to_csv(data_to_save,file_path):
    """
    Load data to csv file
    """
    start_load = time.perf_counter()
    if not data_to_save:
        raise ValueError("No data to save as CSV file")

    if not file_path:
        raise ValueError("File path not defined")

    header = list(data_to_save[0].keys()) # extract field names

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames = header)
        writer.writeheader()
        data = writer.writerows(data_to_save)

    end_load = time.perf_counter()
    load_total_time = end_load - start_load
    load_end_time = datetime.utcnow()

    summary = {
            "l_total_time" : load_total_time,
            "l_datetime" : load_end_time
            }

    return {
            "data": data,
            "stats" : summary
           }

# Load to Local Postgres
def to_local_database(data):
    """
    Load transformed data into Postgres fact table & dimensions
    db_config: dict with keys: host, port, dbname, user, password
    """
    if not data:
        raise ValueError("No data to load into database")
    # Later create and save on env file
    conn = psycopg2.connect(
        host= "postgres",
        port= "5432",
        dbname= "obc_db",
        user= "postgres",
        password= "postgres"
    )
    cur = conn.cursor()

    start_load = time.perf_counter()

    # Example: insert into dim_customer first
    # On conflict log error
    customers = [(row["Customer Hash"],) for row in data]
    execute_values(
        cur,
        """
        INSERT INTO dim_customer (customer_hash)
        VALUES %s
        ON CONFLICT (customer_hash) DO NOTHING
        """,
        customers
    )

    # Insert into dim_drink
    drinks = [(row["Drink"], None) for row in data]
    execute_values(
        cur,
        """
        INSERT INTO dim_drink (drink_name, category)
        VALUES %s
        ON CONFLICT (drink_name) DO NOTHING
        """,
        drinks
    )

    # Insert into dim_branch
    branches = [(row["Branch"],) for row in data]
    execute_values(
        cur,
        """
        INSERT INTO dim_branch (branch_name)
        VALUES %s
        ON CONFLICT (branch_name) DO NOTHING
        """,
        branches
    )

    # Insert into dim_payment
    payments = [(row["Payment Type"], row["Bank Prefix"]) for row in data]
    execute_values(
        cur,
        """
        INSERT INTO dim_payment (payment_type, bank_prefix)
        VALUES %s
        ON CONFLICT (payment_type, bank_prefix) DO NOTHING
        """,
        payments
    )

    # Insert into dim_datetime
    datetimes = [(row["Date/Time"], datetime.fromisoformat(row["Date/Time"]).year,
                  datetime.fromisoformat(row["Date/Time"]).month,
                  datetime.fromisoformat(row["Date/Time"]).day,
                  datetime.fromisoformat(row["Date/Time"]).strftime("%A")) for row in data]

    execute_values(
        cur,
        """
        INSERT INTO dim_datetime (iso_date, year, month, day, weekday)
        VALUES %s
        ON CONFLICT (iso_date) DO NOTHING
        """,
        datetimes
    )

    # Insert into fact_transactions
    # Map foreign keys
    cur.execute("SELECT customer_id, customer_hash FROM dim_customer")
    customer_map = {customer_hash: customer_id for customer_id, customer_hash in cur.fetchall()}

    cur.execute("SELECT drink_id, drink_name FROM dim_drink")
    drink_map = {drink_name: drink_id for drink_id, drink_name in cur.fetchall()}

    cur.execute("SELECT branch_id, branch_name FROM dim_branch")
    branch_map = {branch_name: branch_id for branch_id, branch_name in cur.fetchall()}

    cur.execute("SELECT payment_id, payment_type, bank_prefix FROM dim_payment")
    payment_map = {(row[1], row[2]): row[0] for row in cur.fetchall()}

    cur.execute("SELECT datetime_id, iso_date FROM dim_datetime")
    datetime_map = {row[1].isoformat(): row[0] for row in cur.fetchall()}

    facts = []
    for row in data:
        facts.append((
            row["Transaction ID"],
            customer_map[row["Customer Hash"]],
            drink_map[row["Drink"]],
            branch_map[row["Branch"]],
            payment_map[(row["Payment Type"], row["Bank Prefix"])],
            datetime_map[row["Date/Time"]],
            row["Price"]
        ))

    execute_values(
        cur,
        """
        INSERT INTO fact_transactions (transaction_id, customer_id, drink_id, branch_id, payment_id, datetime_id, price)
        VALUES %s
        ON CONFLICT (transaction_id) DO NOTHING
        """,
        facts
    )

    conn.commit()
    end_load = time.perf_counter()
    conn.close()

    load_total_time = end_load - start_load
    load_end_time = datetime.utcnow()

    return {
        "rows_loaded": len(data),
        "l_total_time": load_total_time,
        "l_datetime": load_end_time
    }

