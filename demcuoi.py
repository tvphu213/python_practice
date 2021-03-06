from scripts.python.data_file_process import DataFileProcess
from scripts.python.get_conf import Config
import pandas as pd
import investpy
from datetime import date
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
from scripts.sql.connect_db import ProcessDB

today = date.today()
config = Config()
config.get_init()
config.get_sql_ini()


def main():
    csv_file = DataFileProcess(config)
    path = csv_file.get_file_path()
    csv_data = pd.read_csv(path)
    dt = get_stock_data(csv_data)
    plot_price(dt, 'Close')
    save_to_db(dt)


def get_stock_data(csv_data):
    present = today.strftime("%d/%m/%Y")
    dt = {}
    for code in csv_data['Code']:
        dt[code] = investpy.get_stock_historical_data(stock=code,
                                                      country='United States',
                                                      from_date='01/01/2020',
                                                      to_date=present)
    return dt


def plot_price(dt, category):
    stocks = []
    x_dates = []
    y_prices = []
    for key in dt.keys():
        stocks.append(key)
        x_dates.append(dt[key].index)
        y_prices.append(dt[key][category])
    visualize(stocks, x_dates, y_prices, category)


def visualize(stocks, x_dates, y_prices, catagory):
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    title = '_'.join(stocks)
    fig_size = plt.rcParams["figure.figsize"]  # loads current figure size
    fig_size[0] = 15  # sets the X size to 15
    fig_size[1] = 8
    # sets this numbers to the new size
    plt.rcParams["figure.figsize"] = fig_size

    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter('%m/%d/%Y'))  # display the date properly
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(
        interval=60))  # x axis tick every 60 days
    # sets y axis tick spacing to 100
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(100))
    for i in range(0, len(x_dates)):
        # plots the x and y
        plt.plot(x_dates[i], y_prices[i], label=stocks[i])
    plt.grid(True)  # turns on axis grid
    plt.ylim(0)  # sets the y axis min to zero
    # rotates the x axis ticks 90 degress and font size 10
    plt.xticks(rotation=90, fontsize=10)
    plt.title(title)  # prints the title on the top
    plt.ylabel('Stock Price For ' + catagory)  # labels y axis
    plt.xlabel('Date')  # labels x axis
    plt.legend()
    # plt.show()
    plt.savefig("output/"+title+dt_string+'.png')


def save_to_db(data):
    dtrow = []
    for key in data.keys():
        dt = data[key]
        prices = dt['Close']
        dates = dt.index
        for i in range(0, len(prices)):
            dtrow.append((key, prices[i], dates[i].strftime("%d/%m/%Y")))
    db = ProcessDB("data/database/stockdb.sqlite")
    cur, conn = db.connect()
    table_name = "StockData"

    # drop table
    drop_table_sql = ProcessDB.drop_table_sql(config.sql_drop, table_name)
    cur.execute(drop_table_sql)
    print("Da xoa bang {} (neu ton tai)".format(table_name))

    # create table
    create_table_sql = ProcessDB.create_table_sql(
        config.sql_create, table_name, {
            "id": "INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE", "Company": "TEXT", "Close_Prices": "REAL", "Date": "TEXT"}
    )
    cur.execute(create_table_sql)
    print("Da tao bang", table_name)

    # insert data
    insert_sql = ProcessDB.insert_sql(
        config.sql_insert, table_name, ["Company", "Close_Prices", "Date"])
    cur.executemany(insert_sql, dtrow)
    conn.commit()

    # print to check
    print(pd.read_sql_query("SELECT * FROM StockData", conn))

    db.close_cur(cur)


if __name__ == "__main__":
    main()
