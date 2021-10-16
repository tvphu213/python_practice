from scripts.python.module1 import Module1
from scripts.python.data_file_process import DataFileProcess
from scripts.python.get_conf import Config
from scripts.sql.connect_db import ProcessDB
import argparse
import pandas as pd


config = Config()
config.get_init()
config.get_sql_ini()

# to do: tao menu, chia ham in list ra


def main():
    # Lay gia tri min max cua range
    list_intersection = []
    csv_file = DataFileProcess()
    try:
        range_list = get_range(csv_file)
    except ValueError:
        print(config.value_err)
        return
    except:
        print(config.common_err)
        return
    # In ra 3 danh sach nhu yeu cau
    for range in range_list:
        mod1_obj = Module1(range)
        list_intersection.append(mod1_obj.intersection_2_list)
        print_list_as_required(mod1_obj)
    csv_file.add_column_to_csv_file("intersection_list", list_intersection)
    csv_file.write_to_output_file(config.output_csv)


def print_list_as_required(mod1_obj):
    # In ra danh sach so le va so chia het cho 3
    print("Danh sach so le:\n", *mod1_obj.list_odd_numbers)
    print(config.seprate_line)
    print("Danh sach so chia het cho 3:\n", *mod1_obj.list_multiple_of_three)
    print(config.seprate_line)
    # In ra danh sach so giong nhau o 2 list
    print("Danh sach phan tu giong nhau o 2 list tren:",
          *mod1_obj.intersection_2_list)


def get_input_from_client():
    """
    Ham tra ve gia tri min max input tu nguoi dung
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-mi", "--min_threshold", type=int,
                        default=config.not_inputed)
    parser.add_argument("-mx", "--max_threshold", type=int,
                        default=config.not_inputed)
    opt = parser.parse_args()
    return opt.min_threshold, opt.max_threshold


def get_range(csv_file):
    min_threshold, max_threshold = get_input_from_client()
    # kiem tra dam bao gia tri min < max
    if min_threshold > max_threshold:
        raise ValueError
    # neu khong duoc nhap thi doc tu file input
    range_list = []
    if min_threshold == config.not_inputed & max_threshold == config.not_inputed:
        csv_file.read_csv_file(config.input_csv)
        range_list = csv_file.get_range_from_csv()
    return range_list


def test_db():
    db = ProcessDB("database.sqlite")
    cur, conn = db.connect()
    table_name = "Customer"

    # tao drop table sql
    drop_table_sql = ProcessDB.drop_table_sql(config.sql_drop, table_name)

    # tao create table sql
    create_table_sql = ProcessDB.create_table_sql(
        config.sql_create, table_name, {
            "id": "INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE", "name": "TEXT", "cust_address": "TEXT"}
    )

    # tao insert table sql
    insert_sql = ProcessDB.insert_sql(
        config.sql_insert, table_name, ["name", "cust_address"])

    # drop table
    cur.execute(drop_table_sql)
    print("Da xoa bang {} (neu ton tai)".format(table_name))

    # create table
    cur.execute(create_table_sql)
    print("Da tao bang", table_name)

    # insert data
    cur.executemany(
        insert_sql, [("Phu", "Cung Trang"), ("Lan", "Quy Nhon, Binh Dinh"),
                     ("Hong", "Binh Thanh, Ho Chi Minh"), ("Tuan", "Ben Cat, Binh Duong")]
    )
    print("Da them", cur.rowcount, "records vao bang.")
    conn.commit()  # cap nhat nhung thay doi len database

    # select
    select_sql = open(r"data\sql_file\select_sample.sql")
    select_sql_as_string = select_sql.read()
    for row in cur.execute(select_sql_as_string):
        print(row)

    #update
    update_sql = open(r"data\sql_file\update_sample.sql")
    update_sql_as_string = update_sql.read()
    for row in cur.execute(update_sql_as_string):
        print(row)
    conn.commit()  # cap nhat nhung thay doi len database
    
    #in dep voi thu vien pandas
    print(pd.read_sql_query("SELECT * FROM Customer",conn))

    db.close_cur(cur)


if __name__ == "__main__":
    # main()
    test_db()
