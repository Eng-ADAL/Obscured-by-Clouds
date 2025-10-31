# Main app local entry point for OBC

import extract as e
import transform as t
import load as l


def main():
    filepath = "data_raw/raw_data.txt"

    # Extract stage
    extracted_data = e.extract_txt(filepath)
    print("Extracted sample:")
    print(extracted_data[:3])

    # Transform stage
    transformed_data = t.transform_all(extracted_data)
    print("Transformed sample:")
    print(transformed_data[:3])

    # Load stage (placeholder)


if __name__ == "__main__":
    main()

