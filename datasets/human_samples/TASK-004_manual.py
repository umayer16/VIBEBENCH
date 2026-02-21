import csv
import os

def process_csv_average(input_file, output_file):
    # HUMAN TOUCH: Check for file existence first
    if not os.path.exists(input_file):
        return "File not found"

    try:
        with open(input_file, mode='r') as f:
            reader = csv.reader(f)
            next(reader) # Skip header
            # Extract 2nd column and calculate mean
            values = [float(row[1]) for row in reader if len(row) > 1]
            
        if not values: return "No data"
        
        avg = sum(values) / len(values)
        with open(output_file, 'w') as f:
            f.write(f"Average: {avg}")
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    process_csv_average('data.csv', 'result.txt')