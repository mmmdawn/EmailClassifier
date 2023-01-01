import csv


def read_csv(csv_file):
    reader = csv.reader(csv_file)
    next(reader)  # Skip the header row
    for row in reader:
        yield row
