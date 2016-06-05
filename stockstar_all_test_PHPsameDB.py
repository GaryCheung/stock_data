from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pymysql
import re
import time

config = {
    'host':'127.0.0.1',
    'port':8889,
    'user':'root',
    'password':'root',
    'db':'stock',
    'charset':'utf8',
    'unix_socket':'/Applications/MAMP/tmp/mysql/mysql.sock'
}

stock_list_all = [
   '000543'
]

present_date = datetime.now().date()

def delete_current_data(config,source):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # 执行sql语句，插入记录
            sql = "DELETE FROM stock_data where date = %s and source = %s"
            cursor.execute(sql,(present_date, source))
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        connection.commit()
    finally:
        connection.close()
    print('-----------------------delete success!----------------','\n')


def get_stock_data(stock_list, source, present_location):
    url_base = 'http://q.ssajax.cn/webhandler/quote_stocks.ashx?debug=1&q=cn|s&i='
    for i in range(1,len(stock_list)+1):
        url = url_base + stock_list[i-1] + '&n=h_stock'
        print(len(stock_list),'------------',i,'---------------',stock_list[i-1],'-------------------URL',url)
        web_data = requests.get(url)
        soup = BeautifulSoup(web_data.text,'lxml')
        soup = str(soup)
        # print(soup)
        amplitudes_tmp = re.findall(r'(\"swing\"\:[0-9]+\.[0-9]+)',soup)
        amplitudes = re.findall(r'([0-9]+\.[0-9]+)',str(amplitudes_tmp))
        quantities_tmp = re.findall(r'(\"volume\"\:[0-9]+\.[0-9]+)',soup)
        quantities = re.findall(r'([0-9]+\.[0-9]+)',str(quantities_tmp))
        names_tmp = re.findall(r'(\"stockname\"\:[\D]+\"\,)',soup)
        names = re.findall(r'([\u4e00-\u9fa5]+)',str(names_tmp))
        price_high_tmp = re.findall(r'(\"high\"\:[0-9]+\.[0-9]+)',soup)
        price_high = re.findall(r'([0-9]+\.[0-9]+)',str(price_high_tmp))
        price_low_tmp = re.findall(r'(\"low\"\:[0-9]+\.[0-9]+)',soup)
        price_low = re.findall(r'([0-9]+\.[0-9]+)',str(price_low_tmp))
        price_open_tmp = re.findall(r'(\"open\"\:[0-9]+\.[0-9]+)',soup)
        price_open = re.findall(r'([0-9]+\.[0-9]+)',str(price_open_tmp))
        price_close_tmp = re.findall(r'(\"close\"\:[0-9]+\.[0-9]+)',soup)
        price_close = re.findall(r'([0-9]+\.[0-9]+)',str(price_close_tmp))
        #print(quantities,'------------------',amplitudes)
        if amplitudes == []:
            amplitudes = str(0.00)
            print(type(amplitudes))
        # print(quantities_tmp,'----------',amplitudes_tmp,'---------',names_tmp)
        print(quantities,'-------',amplitudes,'-------',names,'-------',price_high,'-------',price_low,'-------',price_open,'-----',price_close)
        present_location = present_location + 1
        connection = pymysql.connect(**config)
        try:
            with connection.cursor() as cursor:
                # 执行sql语句，插入记录
                sql = 'INSERT INTO stock_data (date, quantity, amplitude, stock_name, source, price_high, price_low, price_open, price_close) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                cursor.execute(sql, (present_date, quantities, amplitudes, names, source, price_high, price_low, price_open, price_close))
                # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
            connection.commit()
        finally:
            connection.close()
    time.sleep(1)
    return present_location


source = 'stockstar'
delete_current_data(config,source)
urllen = len(stock_list_all)
print(urllen)
present_location = 0
i = 0
stock_list_slice = []
step = 50

#point = 1000
#print(stock_list_all[point])
#stock_list_all = stock_list_all[point:]

while (i*step <= urllen):
    stock_list_slice = stock_list_all[i*step:i*step+step]
    i = i+1
    print('NO.',i,'-------------------','len',len(stock_list_slice),stock_list_slice)
    present_location = get_stock_data(stock_list_slice, source, present_location)
    # print('============',present_location)

#get_stock_data(stock_list_all,source)

#get_stock_data(stock_list_sh,source)
#get_stock_data(stock_list_sz,source)
#get_stock_data(stock_list_cy,source)