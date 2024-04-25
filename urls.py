import requests
import re
import time
import pandas as pd
import json
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://catalogo.fiereparma.it/manifestazione/cibus-2024/'

driver = webdriver.Firefox()
driver.get(url)

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
            
response = requests.get(url)
soup = bs(response.content, 'lxml')
products = soup.find_all('h4')
url_dic = {}
a = 2
for i in range(1, 100):#1, 100
    elements = driver.find_elements(By.TAG_NAME, 'h4')
    b = 1
    for element in elements:
        if b > 2:
            element_html = element.get_attribute('outerHTML')
            product_url = str(re.findall(r'"(.*?)"', str(element_html)))
            product_url = product_url.replace('[', '')
            product_url = product_url.replace(']', '')
            product_url = product_url[57:-1]
            product_name = str(re.findall(r'>(.*?)<', str(element_html)))
            product_name = product_name.replace('[', '')
            product_name = product_name.replace(']', '')
            product_name = product_name[5:-5]
            
            url_dic[product_name] = product_url
        b += 1
    if a == 2:
        path = f'/html/body/div[4]/section[2]/div[1]/div/form/div/button[{a}]'
    else:
        path = f'/html/body/div[3]/section[2]/div[1]/div/form/div/button[{a}]'
    if a > 12:
        path = f'/html/body/div[3]/section[2]/div[1]/div/form/div/button[8]'
    if a > 97:
        path = f'/html/body/div[3]/section[2]/div[1]/div/form/div/button[{a-89}]'
    if a == 2:
        a +=1
    a += 1
    next_buttom = WebDriverWait(driver,20).until(
        EC.element_to_be_clickable((By.XPATH, path)))
    next_buttom.click()
driver.quit()

dic_str = json.dumps(url_dic, indent=4)

# Escribir la cadena en el archivo
with open('dic.txt', 'w') as f:
    f.write(dic_str)
