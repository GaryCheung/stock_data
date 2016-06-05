from bs4 import BeautifulSoup
import requests
import pymysql
from datetime import date,datetime
import time
import re
import pycurl

stock_list = [
    'SZ000543',    #皖能电力
    'SZ002041',    #登海种业
    'SH600050',    #中国联通
    'SZ002215',    #诺普信
    'SH600789',    #鲁抗医药
    'SZ300027',    #华谊兄弟
    'SH600133',    #东湖高新
    'SZ300074',    #华平股份
    'SZ002178',    #延华智能
    'SZ300315',    #掌趣科技
    'SZ002565',    #上海绿新
    'SZ000705',    #浙江震元
    'SH600677',    #航天通信
    'SZ002658',    #雪迪龙
    'SZ000563',    #陕国投A
    'SZ002345',    #潮宏基
    'SZ002699',    #美盛文化
    'SH600251',    #冠农股份
    'SZ000587',    #金洲慈航, 金叶珠宝
    'SZ002553',    #南方轴承
    'SZ002240'     #威华股份
]

headers_all = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    "Host":"xueqiu.com"
}

config = {
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'password':'19860112',
    'db':'stock',
    'charset':'utf8'
}

present_date = datetime.now().date()

def delete_current_data(config,source):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # 执行sql语句，插入记录
            sql = "DELETE FROM stock_data where date = %s and source = %s"
            cursor.execute(sql,(present_date,source))
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        connection.commit()
    finally:
        connection.close()
    print('-----------------------delete success!----------------','\n')

def get_stock_amplitude(stock_list,source):
    url_base = 'https://xueqiu.com/S/'
    for i in range(1,len(stock_list)+1):
        url = url_base + stock_list[i-1]
        print('-------------------------',url)
        web_data = requests.get(url,headers=headers_all)
        soup = BeautifulSoup(web_data.text,'lxml')
        #print(soup)
        stock_quantity = soup.select('table.topTable > tr:nth-of-type(2) > td:nth-of-type(4)')
        stock_amplitude = soup.select('table.topTable > tr:nth-of-type(5) > td:nth-of-type(1) > span')
        stock_name = soup.select('strong.stockName')
        price_open = soup.select('table.topTable > tr:nth-of-type(1) > td:nth-of-type(1)')
        price_close = soup.select('div.currentInfo > strong')
        price_high = soup.select('table.topTable > tr:nth-of-type(1) > td:nth-of-type(2)')
        price_low = soup.select('table.topTable > tr:nth-of-type(2) > td:nth-of-type(2)')
        print(stock_quantity,stock_amplitude,stock_name, price_close, price_high, price_low, price_open)
        for quantity,amplitude,name,pclose,phigh,plow,popen in zip(stock_quantity,stock_amplitude,stock_name,price_close, price_high, price_low, price_open):
            quantities = re.findall(r'(\w*[0-9]+\.*[0-9]+)\w*',quantity.get_text())
            pclose = re.findall(r'(\w*[0-9]+\.*[0-9]+)\w*',pclose.get_text())
            phigh = re.findall(r'(\w*[0-9]+\.*[0-9]+)\w*',phigh.get_text())
            plow = re.findall(r'(\w*[0-9]+\.*[0-9]+)\w*',plow.get_text())
            popen = re.findall(r'(\w*[0-9]+\.*[0-9]+)\w*',popen.get_text())
            amplitudes = re.findall(r'(\w*[0-9]+\.*[0-9]+)\w*',amplitude.get_text())
            names = name.get_text()
            if quantities == []:
                quantities = 0
            if amplitudes == []:
                amplitudes = 0
            print(quantities,'-------------',amplitudes,'-----------------',names)
            connection = pymysql.connect(**config)
            try:
                with connection.cursor() as cursor:
                    # 执行sql语句，插入记录
                    sql = 'INSERT INTO stock_data (date, quantity, amplitude, stock_name, source, price_close, price_high, price_low, price_open) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
                    cursor.execute(sql, (present_date, quantities, amplitudes, names, source, pclose, phigh, plow, popen))
                    # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                connection.commit()
            finally:
                connection.close()
    time.sleep(1)

source = 'xueqiu'
delete_current_data(config,source)
get_stock_amplitude(stock_list,source)