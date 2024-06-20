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

url = 'https://sitevinitech.com.ar/catalogo-de-expositores/'

driver = webdriver.Firefox()
driver.get(url)

def get_product_mail(url):
        response2 = requests.get(url)
        soup2 = bs(response2.content, 'lxml')
        products2 = soup2.find_all('p')
        #eliminar todo lo que no sea <a .../a>
        products2 = [product2.find('a') for product2 in products2 if product2.find('a') is not None]
        #separar el los links y los nombres en un diccionario
        products2 = {product2.text: product2['href'] for product2 in products2}
        
        
        return products2
driver.quit()

print(get_product_mail(url))
#escribir en un archivo json con un enter entre cada uno
with open('products.json', 'w') as file:
    json.dump(get_product_mail(url), file, indent=1)
