import csv
from enum import IntEnum
import argparse
import sys
from typing import Text
sys.path.append('../')


class DataFileProcess:

    def __init__(self, ini):
        self.ini = ini
        self.file_path = ""
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
        return self

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

    def get_stockcode_from_csv(self):
        """
        Ham tra ve lib {ten cong ty :stock code} 
        """
        data = {}
        rows = self.row_data
        for row in rows:
            name = row[ColumnStock.NAME]
            code = row[ColumnStock.CODE]
            data[name] = code
        return data

    def get_file_path_from_client(self):
        """
        Ham lay dia chi file csv tu nguoi dung
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("-path", "--file_path", type=Text,
                            default=self.ini.not_inputed)
        opt = parser.parse_args()
        return opt.file_path

    def get_file_path(self):
        path = self.get_file_path_from_client()
        # neu khong duoc nhap thi doc tu file init
        if path == self.ini.not_inputed:
            path = self.ini.stock_csv
        return path


class ColumnName(IntEnum):
    NO = 0
    MIN = 1
    MAX = 2
    INTERSECTION = 3


class ColumnStock(IntEnum):
    NO = 0
    NAME = 1
    CODE = 2
