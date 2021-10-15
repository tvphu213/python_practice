import csv
from enum import IntEnum
import sys
sys.path.append('../')


class DataFileProcess:

    def __init__(self):
        self.header = []
        self.row_data = []

    def read_csv_file(self, input_file):
        """
        Ham doc file csv
        """
        self.row_data = []
        with open(input_file, "r") as file:
            csvreader = csv.reader(file)
            self.header = next(csvreader)
            for row in csvreader:
                self.row_data.append(row)

    def write_to_output_file(self, output_file):
        with open(output_file, "w", newline="") as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(self.header)
            csvwriter.writerows(self.row_data)

    def add_column_to_csv_file(self, column_name, new_column_data):
        # new_rows_data = []
        self.header.append(column_name)
        i = 0
        for item in self.row_data:
            item.append(new_column_data[i])
            i += 1
        return self

    def get_range_from_csv(self):
        """
        Ham tra ve 2 cot min max tu file csv
        """
        ranges = []
        rows = self.row_data
        for row in rows:
            min = int(row[ColumnName.MIN])
            max = int(row[ColumnName.MAX])
            ranges.append([min, max])
        return ranges


class ColumnName(IntEnum):
    NO = 0
    MIN = 1
    MAX = 2
    INTERSECTION = 3
