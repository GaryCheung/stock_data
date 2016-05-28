from bs4 import BeautifulSoup
import requests

url = 'http://quote.eastmoney.com/sz000543.html'
web_data = requests.get(url)
soup = BeautifulSoup(web_data.text,'lxml')

print(soup)

#amplitude = soup.select('#amplitude')

#print(amplitude)