from scripts.python.data_file_process import DataFileProcess
from scripts.python.get_conf import Config
import pandas as pd
import investpy
from datetime import date
from datetime import datetime
import pandas as pd  
import numpy as np  
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
    csv_file.read_csv_file(path)
    stock_codes = csv_file.get_stockcode_from_csv()
    dt = get_stock_data(stock_codes)
    plot_close_price(dt)
    save_to_db(dt)


def get_stock_data(stock_codes):
    present = today.strftime("%d/%m/%Y")
    dt = {}
    for key in stock_codes.keys():
        df = investpy.get_stock_historical_data(stock=stock_codes[key],
                                                country='United States',
                                                from_date='01/01/2020',
                                                to_date=present)
        dt[stock_codes[key]] = df
    return dt


def plot_close_price(dt):
    stocks = []
    x_dates = []
    y_prices = []
    catagory = 'Close'
    for key in dt.keys():
        stocks.append(key)
        x_dates.append(dt[key].index)
        y_prices.append(dt[key][catagory])
    visualize(stocks, x_dates, y_prices, catagory)


def visualize(stocks, x_dates, y_prices, catagory):
    # fig, ax = plt.subplots()
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    title = '_'.join(stocks)
    # edit this to change which value is plotted (see allstock.columns cell for options)
    # makes matrix with only the stock info

    fig_size = plt.rcParams["figure.figsize"]  # loads current figure size
    fig_size[0] = 15  # sets the X size to 15
    fig_size[1] = 8
    # sets this numbers to the new size
    plt.rcParams["figure.figsize"] = fig_size

    plt.gca().xaxis.set_major_formatter(
        mdates.DateFormatter('%m/%d/%Y'))  # display the date properly
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(
        interval=60))  # x axis tick every 60 days
    # sets y axis tick spacing to 20
    plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(20))
    for i in range(0, len(x_dates)):
        plt.plot(x_dates[i], y_prices[i], label=stocks[i])  # plots the x and y
    plt.grid(True)  # turns on axis grid
    plt.ylim(0)  # sets the y axis min to zero
    # rotates the x axis ticks 90 degress and font size 10
    plt.xticks(rotation=90, fontsize=10)
    plt.title(title)  # prints the title on the top
    plt.ylabel('Stock Price For ' + catagory)  # labels y axis
    plt.xlabel('Date')  # labels x axis
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
    db = ProcessDB("stockdb.sqlite")
    cur, conn = db.connect()
    table_name = "StockData"

    # tao drop table sql
    drop_table_sql = ProcessDB.drop_table_sql(config.sql_drop, table_name)

    # drop table
    cur.execute(drop_table_sql)
    print("Da xoa bang {} (neu ton tai)".format(table_name))

    # create table
    cur.execute("CREATE TABLE StockData(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, Company TEXT, Close_Prices REAL, Date TEXT)")
    print("Da tao bang", table_name)

    cur.executemany(
        "INSERT INTO StockData (Company, Close_Prices, Date) VALUES (?,?,?);", dtrow)
    conn.commit()

    # in dep voi thu vien pandas
    print(pd.read_sql_query("SELECT * FROM StockData", conn))

    db.close_cur(cur)


if __name__ == "__main__":
    main()
