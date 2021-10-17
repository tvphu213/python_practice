**I. Thực hành Python**

Người dùng chạy chương trình với 2 tham số min, max. Nếu không được nhập thì đọc tham số từ file input.csv

In ra:

 - List số lẻ
 
 - List số chia hết cho 3
 
 - List phần tử giống nhau ở 2 list trên
 
Từ nội dung file input, thêm 1 cột danh sách phần tử giống nhau của 2 list và xuất ra file output.csv
-> Chạy hàm main() trong main để test


**II. Thực hành Sqlite với Python**

Viết class xử lý các vấn đề liên quan database (Drop, Creat, Insert, Select, Update) -file connect_db.py

 - Tạo script sql bằng hàm
 
 - Tạo script sql bằng cách đọc file sql
 
 - Ứng dụng thư viện pandas để in kết quả câu lệnh select
 
-> Chạy hàm test_db() trong main để test

 Nội dung cover:
*  kiến thức cấu trúc dữ liệu (list, dictionary..)
*  OOP
*  module
*  xử lý file
*  except
*  Sqlite

**II. Thực hành Crawling data sử dụng Scrapy hoặc BeautifulSoup**
+ Với BeautifulSoup
 Chạy file scripts\data_crawl\beautifullsoup_scrawl.py để test crawling data sử dụng BeautifulSoup và in ra dạng bảng đẹp

+ Với scrapy
Sau khi cài scrapy, chạy câu lệnh sau để tạo các file cần thiết (bên dưới - tutorial là tên project)
>> scrapy startproject tutorial

folder tutorial sẽ được tạo với những file sau
tutorial/
    scrapy.cfg            # deploy configuration file

    tutorial/             # project's Python module, you'll import your code from here
        __init__.py

        items.py          # project items definition file

        middlewares.py    # project middlewares file

        pipelines.py      # project pipelines file

        settings.py       # project settings file

        spiders/          # a directory where you'll later put your spiders
            __init__.py
Tạo spider đặt trong thư mục tutorial\tutorial\spiders\
Giả sử ta có file tutorial\tutorial\spiders\quotes_spider.py
Di chuyển ra thư mục project tutorial\ và chạy lệnh sau để chạy spider với tên được định nghĩa trong file quotes_spider là "quotes", và lưu kết quả vào file quotes.json
>> scrapy crawl quotes -O quotes.json
-O là Override file nếu đã tồn tại file cùng tên
