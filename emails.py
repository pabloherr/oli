import requests
import re
import time
import json
import pandas as pd
from bs4 import BeautifulSoup as bs

url = 'https://catalogo.fiereparma.it/manifestazione/cibus-2024/'

old_exl = input('Do you want to use the old excel file? (y/n): ')
while old_exl != 'y' and old_exl != 'n':
    print('Invalid input')
    old_exl = input('Do you want to use the old excel file? (y/n): ')

def get_product_mail(url):
        response2 = requests.get(url)
        soup2 = bs(response2.content, 'lxml')
        products2 = soup2.find_all('p')
        for product2 in products2:
            product2_a = product2.find('a')
            product2_info = str(re.findall(r'"(.*?)"', str(product2_a)))
            if 'mailto' in product2_info:
                product2_info = product2_info.replace('[', '')
                product2_info = product2_info.replace(']', '')
                product2_info = product2_info[12:-1]
                return product2_info

with open('dic.txt', 'r') as f:
    dic_str = f.read()

url_dic = json.loads(dic_str)

nfc1 = {}
name = []
email = []
for key in url_dic:
    print(key)
    name.append(key)
    mail = get_product_mail(url_dic[key])
    count = 0
    ts = 30
    while mail == None:
        count += 1
        time.sleep(ts)
        mail = get_product_mail(url_dic[key])
        if count == 2:
            ts = 60
        if count == 3:
            ts = 120
        if count == 4:
            mail = 'Not found/case 1'
            nfc1[key] = url_dic[key]
            with open('nfc1.txt', 'w') as f:
                f.write(json.dumps(nfc1))
        
    if mail == '':
        mail = 'Not found/case 2'
    email.append(mail)
    print(mail)
    if old_exl == 'y':
        df_old = pd.read_excel('output.xlsx')
    df = pd.DataFrame({'Name': name, 
                    'Mail': email})
    if old_exl == 'y':
        df = pd.concat([df_old, df])
    df.to_excel('output.xlsx', index=False)