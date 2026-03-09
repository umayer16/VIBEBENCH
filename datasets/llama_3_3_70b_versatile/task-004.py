import csv

def calculate_average():
    total = 0
    count = 0
    with open('data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)  # skip header
        for row in reader:
            if len(row) > 1:
                try:
                    total += float(row[1])
                    count += 1
                except ValueError:
                    pass
    if count > 0:
        average = total / count
        with open('result.txt', 'w') as result_file:
            result_file.write(str(average))
    else:
        with open('result.txt', 'w') as result_file:
            result_file.write('No valid numbers found')

calculate_average()