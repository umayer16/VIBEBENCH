import csv
import os


def calculate_average_second_column(csv_filename='data.csv', output_filename='result.txt'):
    """
    Reads 'data.csv', computes the average of values in the second column (index 1),
    and writes the result to 'result.txt'.
    
    Handles missing file and basic data issues gracefully.
    """
    if not os.path.exists(csv_filename):
        error_msg = f"Error: File '{csv_filename}' not found.\n"
        print(error_msg)
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(error_msg)
        except Exception as e:
            print(f"Also failed to write error to '{output_filename}': {e}")
        return

    total = 0.0
    count = 0

    try:
        with open(csv_filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            
            # Optional: skip header row if it exists
            # header = next(reader, None)   # uncomment if your file has headers
            
            for row in reader:
                if len(row) < 2:
                    continue  # skip malformed rows
                    
                try:
                    value = float(row[1])  # second column (0-based index 1)
                    total += value
                    count += 1
                except (ValueError, TypeError):
                    # skip non-numeric values silently (or log if desired)
                    continue

        if count == 0:
            result = "No valid numeric values found in the second column.\n"
        else:
            average = total / count
            result = f"Average of second column: {average:.4f}\n"
            result += f"(based on {count} valid numeric values)\n"

        print(result.strip())

        # Write result to output file
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(result)

    except Exception as e:
        error_msg = f"Error processing file: {type(e).__name__}: {e}\n"
        print(error_msg)
        try:
            with open(output_filename, 'w', encoding='utf-8') as f:
                f.write(error_msg)
        except Exception as write_err:
            print(f"Failed to write error message: {write_err}")


if __name__ == "__main__":
    print("Processing 'data.csv'...\n")
    calculate_average_second_column()
    print("\nDone. Check 'result.txt' for the output.")