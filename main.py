import requests
import re
import time
from bs4 import BeautifulSoup as bs
import urllib.parse 

url = 'https://catalogo.fiereparma.it/manifestazione/cibus-2024/'
descriptions = []


response = requests.get(url)
soup = bs(response.content, 'lxml')
#products = soup.find_all('div', class_='product')
#print (str(soup.encode("utf-8")))
products = soup.find_all('h4')

for product in products:
    poduct_a = product.find('a')
    product_url = str(re.findall(r'"(.*?)"', str(poduct_a)))
    product_url = product_url.replace('[', '')
    product_url = product_url.replace(']', '')
    product_name = str(re.findall(r'>(.*?)<', str(poduct_a)))
    product_name = product_name.replace('[', '')
    product_name = product_name.replace(']', '')
    print(product_name)
    if not product_name == '' or not product_url == '':
        product_url = product_url[1:-1]
        time.sleep(10)
        response2 = requests.get(product_url)
        soup2 = bs(response2.content, 'lxml')
        
        products2 = soup2.find_all('p')
        for product2 in products2:
            product2_a = product2.find('a')
            product2_info = str(re.findall(r'"(.*?)"', str(product2_a)))
            if 'mailto' in product2_info:
                product2_info = product2_info.replace('[', '')
                product2_info = product2_info.replace(']', '')
                product2_info = product2_info[12:-1]
                print(product2_info)
        
