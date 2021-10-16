import sqlite3


class ProcessDB:
    def __init__(self, db_name):
        self.db_name = db_name

    def connect(self):
        conn = sqlite3.connect(self.db_name)
        print("Ket noi sql!")
        cur = conn.cursor()
        return cur, conn

    @staticmethod
    def close_cur(cur):
        print("Dong ket noi sql!")
        cur.close()

    @staticmethod
    def drop_table_sql(sql, table_name):
        sql = sql.format(table_name)
        return sql

    @staticmethod
    def create_table_sql(sql, table_name, column_specs):
        str = ProcessDB.columns_to_string(column_specs)
        sql = sql.format(table_name, str)
        return sql

    @staticmethod
    def insert_sql(sql, table_name, column_names):
        columns_placehold = []
        column_names_to_string = ", ".join(column_names)
        for i in range(0, len(column_names)):
            columns_placehold.append("?")

        columns_placehold = ", ".join(columns_placehold)
        sql = sql.format(table_name, column_names_to_string, columns_placehold)
        return sql

    @staticmethod
    def columns_to_string(column_specs):
        str = ""
        count = 0
        for column_name in column_specs.keys():
            count += 1
            str = str + column_name + " " + column_specs[column_name]
            if count < len(column_specs):
                str += ", "
        return str
