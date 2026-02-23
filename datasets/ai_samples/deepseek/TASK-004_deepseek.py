import csv
import os
import sys


def calculate_column_average(filename, column_index=1, has_header=False):
    """
    Calculate the average of a specific column in a CSV file.
    
    Args:
        filename: Path to the CSV file
        column_index: Index of the column to average (0-based)
        has_header: Whether the CSV file has a header row
        
    Returns:
        float: Average of the column values
        
    Raises:
        FileNotFoundError: If the CSV file doesn't exist
        ValueError: If the column contains non-numeric data or is empty
        Exception: For other CSV processing errors
    """
    values = []
    line_number = 0
    
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            # Try to detect the delimiter automatically
            sample = csvfile.read(1024)
            csvfile.seek(0)
            
            # Common delimiters
            delimiters = [',', ';', '\t', '|']
            dialect = None
            
            # Try to guess the delimiter
            for delimiter in delimiters:
                if delimiter in sample:
                    try:
                        dialect = csv.Sniffer().sniff(sample, delimiters=delimiters)
                        break
                    except:
                        pass
            
            # If delimiter detection failed, default to comma
            if dialect is None:
                csv_reader = csv.reader(csvfile)
            else:
                csv_reader = csv.reader(csvfile, dialect)
            
            # Skip header if specified
            if has_header:
                try:
                    header = next(csv_reader)
                    print(f"Header detected: {header}")
                except StopIteration:
                    raise ValueError("CSV file is empty")
            
            # Process each row
            for row in csv_reader:
                line_number += 1
                
                # Check if row has enough columns
                if len(row) <= column_index:
                    print(f"Warning: Row {line_number} has fewer than {column_index + 1} columns, skipping")
                    continue
                
                # Get the value and try to convert to float
                value_str = row[column_index].strip()
                
                # Skip empty values
                if not value_str:
                    print(f"Warning: Row {line_number}, column {column_index} is empty, skipping")
                    continue
                
                try:
                    value = float(value_str)
                    values.append(value)
                except ValueError:
                    print(f"Warning: Row {line_number}, column {column_index} contains non-numeric data: '{value_str}', skipping")
                    continue
    
    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file '{filename}' not found")
    except csv.Error as e:
        raise Exception(f"Error parsing CSV file: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error reading CSV file: {e}")
    
    # Check if we found any valid values
    if not values:
        raise ValueError(f"No valid numeric data found in column {column_index}")
    
    # Calculate average
    average = sum(values) / len(values)
    return average


def write_result_to_file(filename, content):
    """
    Write result to a text file.
    
    Args:
        filename: Output filename
        content: Content to write
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except IOError as e:
        print(f"Error writing to file '{filename}': {e}")
        return False


def create_sample_csv(filename='data.csv'):
    """
    Create a sample CSV file for testing purposes.
    
    Args:
        filename: Name of the CSV file to create
    """
    sample_data = [
        ["Name", "Age", "Score", "Grade"],
        ["Alice", "25", "85.5", "B"],
        ["Bob", "30", "92.0", "A"],
        ["Charlie", "22", "78.5", "C"],
        ["Diana", "28", "95.5", "A"],
        ["Eve", "35", "88.0", "B"],
        ["Frank", "29", "invalid", "C"],  # Invalid data for testing
        ["Grace", "31", "91.5", "A"],
        ["", "", "", ""],  # Empty row for testing
        ["Henry", "27", "89.5", "B+"],
    ]
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(sample_data)
        print(f"Sample CSV file '{filename}' created successfully")
        return True
    except Exception as e:
        print(f"Error creating sample CSV file: {e}")
        return False


if __name__ == "__main__":
    print("CSV Column Average Calculator")
    print("=" * 40)
    
    input_file = 'data.csv'
    output_file = 'result.txt'
    column_to_average = 1  # Second column (0-based index)
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"File '{input_file}' not found.")
        response = input("Would you like to create a sample CSV file for testing? (y/n): ")
        
        if response.lower() == 'y':
            if not create_sample_csv(input_file):
                sys.exit(1)
        else:
            print("Exiting program.")
            sys.exit(0)
    
    # Try to calculate the average
    try:
        print(f"\nProcessing file: {input_file}")
        print(f"Calculating average of column index {column_to_average} (second column)")
        print("-" * 40)
        
        # Calculate average (assuming CSV has a header row)
        average = calculate_column_average(input_file, column_index=column_to_average, has_header=True)
        
        # Format the result
        result_text = f"Average of column {column_to_average} in '{input_file}': {average:.2f}\n"
        result_text += f"Calculated on: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        result_text += f"Based on numeric values found in the column\n"
        
        print(f"\nResult: {average:.2f}")
        
        # Write to output file
        if write_result_to_file(output_file, result_text):
            print(f"\nResult successfully written to '{output_file}'")
            
            # Display the content that was written
            print("\nFile contents:")
            print("-" * 20)
            print(result_text.rstrip())
        else:
            print(f"\nFailed to write result to '{output_file}'")
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Additional demonstration with different scenarios
    print("\n" + "=" * 40)
    print("Additional Examples:")
    print("-" * 40)
    
    # Example 1: Different column
    try:
        print("\nExample 1: Average of first column (Age) - should work:")
        avg_age = calculate_column_average(input_file, column_index=0, has_header=True)
        print(f"Average age: {avg_age:.2f}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 2: Column with mixed data
    try:
        print("\nExample 2: Average of third column (Score) - has invalid data:")
        avg_score = calculate_column_average(input_file, column_index=2, has_header=True)
        print(f"Average score: {avg_score:.2f} (invalid entries were skipped)")
    except Exception as e:
        print(f"Error: {e}")
    
    # Example 3: Non-existent file
    print("\nExample 3: Handling missing file:")
    try:
        avg = calculate_column_average('nonexistent.csv', column_index=0)
    except FileNotFoundError as e:
        print(f"Correctly caught: {e}")