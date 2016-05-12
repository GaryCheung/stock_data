from bs4 import BeautifulSoup
import requests
import pymysql
from datetime import date,datetime
import time
import re

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
    'SZ002553'     #南方轴承
]

headers = {
    'Cookie':'s=30e012lulu; xq_a_token=4c857c2073766ab3b6e6c26c583bfc2be49b59dd; xqat=4c857c2073766ab3b6e6c26c583bfc2be49b59dd; xq_r_token=982d1df16ab28e980d963c239a1550963c2004c2; xq_is_login=1; u=3123842048; xq_token_expire=Mon%20May%2023%202016%2020%3A34%3A05%20GMT%2B0800%20(CST); bid=b605182f86b7f2f48872188e1be4686d_ink9v8vs; snbim_minify=true; Hm_lvt_1db88642e346389874251b5a1eded6e3=1462179811,1462503687,1462775091,1462861925; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1463024491; __utmt=1; __utma=1.1403218528.1461846852.1462929892.1463024491.16; __utmb=1.1.10.1463024491; __utmc=1; __utmz=1.1461846852.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
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
        web_data = requests.get(url,headers=headers)
        soup = BeautifulSoup(web_data.text,'lxml')
        stock_quantity = soup.select('table.topTable > tr:nth-of-type(2) > td:nth-of-type(4)')
        stock_amplitude = soup.select('table.topTable > tr:nth-of-type(5) > td:nth-of-type(1) > span')
        stock_name = soup.select('strong.stockName')
        print(stock_quantity,stock_amplitude,stock_name)
        for quantity,amplitude,name in zip(stock_quantity,stock_amplitude,stock_name):
            quantities = re.findall(r'(\w*[0-9]+\.*[0-9]+)\w*',quantity.get_text())
            amplitudes = re.findall(r'(\w*[0-9]+\.*[0-9]+)\w*',amplitude.get_text())
            names = name.get_text()
            print(quantities,'-------------',amplitudes,'-----------------',names)
            connection = pymysql.connect(**config)
            try:
                with connection.cursor() as cursor:
                    # 执行sql语句，插入记录
                    sql = 'INSERT INTO stock_data (date, quantity, amplitude, stock_name) VALUES (%s, %s, %s, %s)'
                    cursor.execute(sql, (present_date, quantities, amplitudes, names))
                    # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                connection.commit()
            finally:
                connection.close()
    time.sleep(1)

delete_current_data(config)
get_stock_amplitude(stock_list)
