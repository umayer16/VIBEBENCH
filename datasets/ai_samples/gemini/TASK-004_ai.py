import csv
import os

def calculate_column_average(input_filename, output_filename):
    """
    Reads a CSV, calculates the average of the second column, 
    and writes the result to a text file.
    """
    if not os.path.exists(input_filename):
        print(f"Error: The file '{input_filename}' was not found.")
        return

    total = 0.0
    count = 0

    try:
        with open(input_filename, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            
            # Skip header if necessary; assuming data starts from row 1
            # If your CSV has a header, uncomment the next line:
            # next(reader, None) 

            for row in reader:
                # Ensure the row has at least two columns
                if len(row) >= 2:
                    try:
                        # Attempt to convert second column (index 1) to float
                        value = float(row[1])
                        total += value
                        count += 1
                    except ValueError:
                        # Skip rows where the second column isn't a number
                        continue

        if count > 0:
            average = total / count
            with open(output_filename, mode='w', encoding='utf-8') as f:
                f.write(f"Average of second column: {average}\n")
            print(f"Successfully calculated average ({average}) and saved to {output_filename}")
        else:
            print("No valid numeric data found in the second column.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Sample Execution: Create a dummy data.csv for testing
    input_file = 'data.csv'
    output_file = 'result.txt'
    
    with open(input_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Item', 'Price']) # Header
        writer.writerow(['Apple', '1.50'])
        writer.writerow(['Banana', '0.75'])
        writer.writerow(['Cherry', '2.25'])

    # Run the function
    calculate_column_average(input_file, output_file)
    
    # Verify the result
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            print(f"Contents of {output_file}: {f.read().strip()}")