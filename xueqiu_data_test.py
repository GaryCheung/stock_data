from bs4 import BeautifulSoup
import requests
import pymysql
from datetime import date,datetime
import time
import re
import pycurl
from io import BytesIO

stock_list = [
    'SZ000543'    #皖能电力
]

'''
headers = BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, 'https://www.xueqiu.com')
c.setopt(c.HEADER, 1)
c.setopt(c.NOBODY, 1) # header only, no body
c.setopt(c.HEADERFUNCTION, headers.write)
c.perform()
print('------------',headers.getvalue())
'''

present_time = time.time()
#print('-----------------',present_time)
present_time = round(present_time)
#print('-----------------',str(present_time))

headers = {
    'Cookie':'s=1wp21218b9; xq_a_token=b6eecee1abad844d30250c0af58bfa36b2851f1d; xq_r_token=8bd931f3143a3c125db60e290232340b0a371472; Hm_lvt_1db88642e346389874251b5a1eded6e3=1463114665; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1463114673; __utmt=1; __utma=1.384338427.1463114673.1463114673.1463114673.1; __utmb=1.1.10.1463114673; __utmc=1; __utmz=1.1463114673.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
}

headers_win = {
    'Cookie':'s=1dmc1f8ed6; xq_a_token=db8683446fe2a5e342276e182a2d645557dd9ad8; xq_r_token=2e982c242f4c05dbd9e1f356c30a24d1a5bf297b; __utmt=1; __utma=1.1346186107.1464352898.1464352898.1464352898.1; __utmb=1.2.10.1464352898; __utmc=1; __utmz=1.1464352898.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_1db88642e346389874251b5a1eded6e3=1464352887; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1464352905',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.277.400 QQBrowser/9.4.7658.400'
}

headers_chrome = {
    "Cookie":"s=2u40153rw1; xq_a_token=934f674c5167ef0a40bc92c387554e5b8d74a6f8; xq_r_token=ed5549c6fd48ab1fbe3f40b00a823b21dbd4f618; Hm_lvt_1db88642e346389874251b5a1eded6e3=1464574456; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1464574464; __utmt=1; __utma=1.166417680.1464574465.1464574465.1464574465.1; __utmb=1.1.10.1464574465; __utmc=1; __utmz=1.1464574465.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
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

def delete_current_data(config):
    connection = pymysql.connect(**config)
    try:
        with connection.cursor() as cursor:
            # 执行sql语句，插入记录
            sql = "DELETE FROM stock_data where date = '%s'" %(present_date)
            cursor.execute(sql)
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
        connection.commit()
    finally:
        connection.close()
    print('-----------------------delete success!----------------','\n')

def get_stock_amplitude(stock_list):
    url_base = 'https://xueqiu.com/S/'
    for i in range(1,len(stock_list)+1):
        url = url_base + stock_list[i-1]
        print('-------------------------',url)
        #login = requests.session()
        #login_data = {'email': 'sirius_ziham@hotmail.com', 'password': '19860112'}
        #login.post('https://www.xueqiu.com',login_data)
        web_data = requests.get(url,headers=headers_chrome)
        #header = web_data.request.headers
        #print(header)
        soup = BeautifulSoup(web_data.text,'lxml')
        print(soup)
        stock_quantity = soup.select('table.topTable > tr:nth-of-type(2) > td:nth-of-type(4)')
        stock_amplitude = soup.select('table.topTable > tr:nth-of-type(5) > td:nth-of-type(1) > span')
        stock_name = soup.select('strong.stockName')
        print(stock_quantity,stock_amplitude,stock_name)

# delete_current_data(config)
get_stock_amplitude(stock_list)
