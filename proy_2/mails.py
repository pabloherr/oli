import requests
import re
import time
import json
import pandas as pd
from bs4 import BeautifulSoup as bs


def get_product_mail(url):
    response2 = requests.get(url)
    soup2 = bs(response2.content, 'lxml')
    products2 = soup2.find_all('a')
    products2 = [product2['href'] for product2 in products2 if 'mailto' in product2['href']]
    products2 = [product2.replace('mailto:', '') for product2 in products2]
    #eliminar las ' de los mails
    products2 = [product2.replace("'", '') for product2 in products2]
    products2 = list(set(products2))
    return products2

#leer el archivo json y usar la guncion en cada uno de los links
with open('products.json', 'r') as file:
    url_dic = json.load(file)

for key in url_dic:
    mail = get_product_mail(url_dic[key]) 
    mail = str(mail)[1:-1]
    url_dic[key] = mail


df = pd.DataFrame(list(url_dic.items()), columns = ['Name', 'Email'])
df.to_excel('output.xlsx', index = False)
