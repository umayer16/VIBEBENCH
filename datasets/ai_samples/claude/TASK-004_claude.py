import csv
import os


def read_csv_and_calculate_average(csv_filename="data.csv"):
    if not os.path.exists(csv_filename):
        raise FileNotFoundError(f"File '{csv_filename}' not found.")

    values = []
    skipped_rows = 0

    with open(csv_filename, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader, None)

        for line_num, row in enumerate(reader, start=2):
            if len(row) < 2:
                print(f"  [Warning] Row {line_num} skipped: not enough columns -> {row}")
                skipped_rows += 1
                continue
            try:
                values.append(float(row[1].strip()))
            except ValueError:
                print(f"  [Warning] Row {line_num} skipped: invalid value -> '{row[1]}'")
                skipped_rows += 1

    if not values:
        raise ValueError("No valid numeric data found in the second column.")

    average = sum(values) / len(values)
    return average, len(values), skipped_rows, header


def write_result(result_filename="result.txt", average=0, count=0, skipped=0, header=None):
    col_name = header[1].strip() if header and len(header) >= 2 else "Column 2"

    with open(result_filename, "w", encoding="utf-8") as f:
        f.write("===== CSV Average Calculator Result =====\n\n")
        f.write(f"Column Analyzed : {col_name}\n")
        f.write(f"Valid Rows      : {count}\n")
        f.write(f"Skipped Rows    : {skipped}\n")
        f.write(f"Average Value   : {average:.4f}\n")

    print(f"\n  Result written to '{result_filename}'")
    print(f"  Column   : {col_name}")
    print(f"  Rows used: {count} | Skipped: {skipped}")
    print(f"  Average  : {average:.4f}")


def create_sample_csv(filename="data.csv"):
    rows = [
        ["Name", "Score"],
        ["Alice", "88"],
        ["Bob", "92"],
        ["Charlie", "75"],
        ["Diana", "95"],
        ["Eve", "invalid"],
        ["Frank", "83"],
    ]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)
    print(f"  Sample '{filename}' created with {len(rows) - 1} data rows.")


if __name__ == "__main__":
    CSV_FILE = "data.csv"
    RESULT_FILE = "result.txt"

    print("Step 1: Creating sample CSV file...")
    create_sample_csv(CSV_FILE)

    print("\nStep 2: Reading CSV and calculating average...")
    try:
        average, count, skipped, header = read_csv_and_calculate_average(CSV_FILE)
        write_result(RESULT_FILE, average, count, skipped, header)
    except FileNotFoundError as e:
        print(f"  [Error] {e}")
    except ValueError as e:
        print(f"  [Error] {e}")
    except Exception as e:
        print(f"  [Unexpected Error] {e}")

    print("\nStep 3: Contents of 'result.txt':")
    print("-" * 42)
    if os.path.exists(RESULT_FILE):
        with open(RESULT_FILE, "r") as f:
            print(f.read())