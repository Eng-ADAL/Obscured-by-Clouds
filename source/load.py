import csv
import time
from datetime import datetime

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
