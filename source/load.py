import csv

def load_to_csv(data_to_save,file_path):
    """
    Saves extract and transformed data to csv file
    """
    if not data_to_save:
        raise ValueError("No data to save as CSV file")

    if not file_path:
        raise ValueError("File path not defined")

    header = list(data_to_save[0].keys()) # extract field names

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames = header)
        writer.writeheader()
        data = writer.writerows(data_to_save)
        return data
