from bs4 import BeautifulSoup
import requests
import pymysql
from datetime import date,datetime
import time
import re

stock_list = [
    'SZ000543'    #皖能电力
]

headers = {
    'Cookie':'s=30e012lulu; xq_a_token=4c857c2073766ab3b6e6c26c583bfc2be49b59dd; xqat=4c857c2073766ab3b6e6c26c583bfc2be49b59dd; xq_r_token=982d1df16ab28e980d963c239a1550963c2004c2; xq_is_login=1; u=3123842048; xq_token_expire=Mon%20May%2023%202016%2020%3A34%3A05%20GMT%2B0800%20(CST); bid=b605182f86b7f2f48872188e1be4686d_ink9v8vs; snbim_minify=true; Hm_lvt_1db88642e346389874251b5a1eded6e3=1462179811,1462503687,1462775091,1462861925; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1463110841; __utmt=1; __utma=1.1403218528.1461846852.1463024491.1463110842.17; __utmb=1.1.10.1463110842; __utmc=1; __utmz=1.1461846852.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
}

config = {
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'password':'19860112',
    'db':'stock',
    'charset':'utf8'
}

ISOTIMEFORMAT='%Y-%m-%d %X'
present_date = time.strftime(ISOTIMEFORMAT,time.localtime())

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
        web_data = requests.get(url,headers=headers)
        soup = BeautifulSoup(web_data.text,'lxml')
        print(soup)
        stock_quantity = soup.select('table.topTable > tr:nth-of-type(2) > td:nth-of-type(4)')
        stock_amplitude = soup.select('table.topTable > tr:nth-of-type(5) > td:nth-of-type(1) > span')
        stock_name = soup.select('strong.stockName')
        print(stock_quantity,stock_amplitude,stock_name)

# delete_current_data(config)
get_stock_amplitude(stock_list)
