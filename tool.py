from enum import IntEnum
from module1 import Module1
import argparse
import csv


DEFAULT_PARAM_FILE_NAME_TXT = "default_txt.txt"
DEFAULT_PARAM_FILE_NAME_CSV = "default_csv.csv"
SEPERATE_LINE = "------------------------------------------------------------------------------------------------------------------------------------------------------"
NO_SET_CLIENT_INPUT = -1
DEFAULT_ROW_DATA = 0


def main():
    # Lay gia tri min max cua range
    try:
        min_threshold, max_threshold = get_range()
    except ValueError:
        print("Min threshold lon hon gia tri maxthershold, vui long chay va nhap lai.")
        return
    except:
        print("Dung chuong trinh do co loi. Vui long lien he nha san xuat.")
        return
    # In ra 3 danh sach nhu yeu cau    
    print_list_as_required(min_threshold, max_threshold)


def print_list_as_required(min_threshold, max_threshold):
    # In ra danh sach so le va so chia het cho 3
    mod1_obj = Module1(min_threshold, max_threshold)
    print("Danh sach so le:\n", *mod1_obj.list_odd_numbers)
    print(SEPERATE_LINE)
    print("Danh sach so chia het cho 3:\n", *mod1_obj.list_multiple_of_three)
    print(SEPERATE_LINE)
    # In ra danh sach so giong nhau o 2 list
    print("Danh sach phan tu giong nhau o 2 list tren:")
    print(
        *Module1.intersect_2_list(
            mod1_obj.list_odd_numbers, mod1_obj.list_multiple_of_three
        )
    )


def get_input_from_client():
    """
    Ham tra ve gia tri min max input tu nguoi dung
    """
    #
    parser = argparse.ArgumentParser()
    parser.add_argument("-mi", "--min_threshold", type=int, default=NO_SET_CLIENT_INPUT)
    parser.add_argument("-mx", "--max_threshold", type=int, default=NO_SET_CLIENT_INPUT)
    opt = parser.parse_args()
    return opt.min_threshold, opt.max_threshold


def read_csv_file():
    """
    Ham doc file cau hinh default csv
    """
    rows = []
    with open(DEFAULT_PARAM_FILE_NAME_CSV, "r") as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
        for row in csvreader:
            rows.append(row)
    return {"header": header, "rows": rows}


def get_range_from_csv(csv):
    """
    Ham tra ve gia tri min max tu file cau hinh default
    """
    rows = csv["rows"]
    min = int(rows[DEFAULT_ROW_DATA][ColumnName.MIN])
    max = int(rows[DEFAULT_ROW_DATA][ColumnName.MAX])
    return min, max


def get_range():
    min_threshold, max_threshold = get_input_from_client()
    # kiem tra dam bao gia tri min < max
    if min_threshold > max_threshold:
        raise ValueError
    # neu khong duoc nhap thi doc tu file default
    if min_threshold == NO_SET_CLIENT_INPUT & max_threshold == NO_SET_CLIENT_INPUT:
        csv_file = read_csv_file()
        min_threshold, max_threshold = get_range_from_csv(csv_file)
    return min_threshold, max_threshold


class ColumnName(IntEnum):
    MIN = 0
    MAX = 1
    NAME = 2


if __name__ == "__main__":
    main()
