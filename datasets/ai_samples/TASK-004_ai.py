import pandas as pd

def process_csv_average(input_file, output_file):
    try:
        # AI frequently defaults to pandas for any CSV work
        df = pd.read_csv(input_file)
        avg = df.iloc[:, 1].mean()
        
        with open(output_file, 'w') as f:
            f.write(f"Average: {avg}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # This will fail unless data.csv exists, perfect for testing your 'executor.py' error handling
    process_csv_average('data.csv', 'result.txt')