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

headers1 = {
    'Cookie':'s=1d4k164ccu; xq_a_token=db8683446fe2a5e342276e182a2d645557dd9ad8; xq_r_token=2e982c242f4c05dbd9e1f356c30a24d1a5bf297b; Hm_lvt_1db88642e346389874251b5a1eded6e3=1464341283; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1464341302; __utmt=1; __utma=1.1909343692.1464341303.1464341303.1464341303.1; __utmb=1.1.10.1464341303; __utmc=1; __utmz=1.1464341303.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'Referer':'https://xueqiu.com/k?q=%E7%9A%96%E8%83%BD%E7%94%B5%E5%8A%9B',
    'Host':'xueqiu.com'
}

headers_mac = {
    'Cookie':'s=1do91buzvf; xq_a_token=db8683446fe2a5e342276e182a2d645557dd9ad8; xq_r_token=2e982c242f4c05dbd9e1f356c30a24d1a5bf297b; __utmt=1; Hm_lvt_1db88642e346389874251b5a1eded6e3=1464354158; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1464354170; __utma=1.1202071191.1464354164.1464354164.1464354164.1; __utmb=1.2.10.1464354164; __utmc=1; __utmz=1.1464354164.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}

headers_firefox = {
    'Cookie':'s=1acl1b37ul; __utma=1.491234239.1459080101.1463114086.1464352387.3; __utmz=1.1459080101.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_1db88642e346389874251b5a1eded6e3=1463114067,1464352375; xq_a_token=db8683446fe2a5e342276e182a2d645557dd9ad8; xq_r_token=2e982c242f4c05dbd9e1f356c30a24d1a5bf297b; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1464352385; __utmb=1.1.10.1464352387; __utmc=1; __utmt=1',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Host':'xueqiu.com',
    'Connection':'keep-alive'
}

data_mac = {
    'P3P':'CP="IDC DSP COR ADM DEVi TAIi PSA PSD IVAi IVDi CONi HIS OUR IND CNT"'
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
        web_data = requests.get(url)
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
