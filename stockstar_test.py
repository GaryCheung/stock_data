from bs4 import BeautifulSoup
import requests
from datetime import datetime
import pymysql
import re
import time

config = {
    'host':'127.0.0.1',
    'port':3306,
    'user':'root',
    'password':'19860112',
    'db':'stock',
    'charset':'utf8'
}

stock_list = [
'600349',#富通昭和
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


def get_stock_data(stock_list, source):
    url_base = 'http://stock.quote.stockstar.com//'
    for i in range(1,len(stock_list)+1):
        url = url_base + stock_list[i-1] + '.shtml'
        print(len(stock_list),'------------',i,'---------------',stock_list[i-1],'-------------------URL',url)
        web_data = requests.get(url)
        soup = BeautifulSoup(web_data.text,'lxml')
        quantity = soup.select('#stock_quoteinfo_cj')
        amplitude = soup.select('#stock_quoteinfo_zf')
        name = soup.select('div.name > h2:nth-of-type(1)')
        # print(quantity,'--------------',amplitude,'-------------',name)
        for quantities,amplitudes,names in zip(quantity, amplitude, name):
            quantities = quantities.get_text()
            quantities = quantities.encode('latin-1').decode('gbk')
            quantities = re.findall(r'(\w*[0-9]+\.*[0-9]+)\w*',quantities)
            print(amplitudes.get_text())
            if float(amplitudes.get_text()) == 0:
                url = 'http://q.ssajax.cn/webhandler/quote_stocks.ashx?debug=1&q=cn|s&i=' + stock_list[i-1] + '&n=h_stock'
                print(url)
                web_data_tmp = requests.get(url)
                soup_tmp = BeautifulSoup(web_data_tmp.text,'lxml')
                soup_tmp = str(soup_tmp)
                amplitudes_tmp = re.findall(r'(\"swing\"\:[0-9]+\.[0-9]+)',soup_tmp)
                amplitudes = re.findall(r'([0-9]+\.[0-9]+)',str(amplitudes_tmp))
                print('------------------',amplitudes_tmp)
                if amplitudes == []:
                    amplitudes = str(0.00)
                    print(type(amplitudes))
            names = names.get_text().encode('latin-1').decode('gbk')
            print('quantities',type(quantities),quantities,'-------------','amplitudes',type(amplitudes),amplitudes,'-----------------',type(names),names)
            connection = pymysql.connect(**config)
            try:
                with connection.cursor() as cursor:
                    # 执行sql语句，插入记录
                    sql = 'INSERT INTO stock_data (date, quantity, amplitude, stock_name, source) VALUES (%s, %s, %s, %s, %s)'
                    cursor.execute(sql, (present_date, quantities, amplitudes, names, source))
                    # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                connection.commit()
            finally:
                connection.close()
    time.sleep(1)

source = 'stockstar'
delete_current_data(config,source)
get_stock_data(stock_list,source)