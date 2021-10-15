from scripts.python.module1 import Module1
from scripts.python.data_file_process import DataFileProcess
from scripts.python.get_conf import Config
from scripts.sql.connect_db import ProcessDB
import argparse

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
    print("Danh sach phan tu giong nhau o 2 list tren:", *mod1_obj.intersection_2_list)


def get_input_from_client():
    """
    Ham tra ve gia tri min max input tu nguoi dung
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-mi", "--min_threshold", type=int, default=config.not_inputed)
    parser.add_argument("-mx", "--max_threshold", type=int, default=config.not_inputed)
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
    db = ProcessDB("testdb.sqlite")
    cur, conn = db.connect()
    drop_table_sql = ProcessDB.drop_table_sql(config.sql_drop, "Student")
    create_table_sql = ProcessDB.create_table_sql(
        config.sql_create, "Student", {"name": "TEXT", "class": "TEXT"}
    )
    insert_sql = ProcessDB.insert_sql(config.sql_insert, "Student", ["name", "class"])
    cur.execute(drop_table_sql)
    cur.execute(create_table_sql)
    cur.executemany(
        insert_sql, [("Phu", "AI"), ("Lan", "SQL"), ("Hong", "SQL"), ("Tuan", "Python")]
    )
    print("Chung ta da inserted", cur.rowcount, "records vao bang.")
    conn.commit()  # cap nhat nhung thay doi len sql database
    sql_file = open("data\sql_file\sample.sql")
    sql_as_string = sql_file.read()
    cur.executescript(sql_as_string)
    for row in cur.execute(sql_as_string):
        print(row)
    db.close_cur(cur)


if __name__ == "__main__":
    # main()
    test_db()
