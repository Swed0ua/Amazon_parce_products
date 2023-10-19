import sys
import requests
from bs4 import BeautifulSoup
import time
import json
import os
import codecs
import xlsxwriter
import quickstart


file_path = os.path.abspath(__file__)
file_name = file_path.split('\\')[-1]
dir_path = file_path.replace(f'\\{file_name}', '')

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'uk,en-US;q=0.9,en;q=0.8,ru;q=0.7',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}

site_domen = 'https://www.amazon.com'
domen_temp = 'https://www.amazon.com/dp/'
max_size = sys.maxsize

def get_config ():
    with codecs.open(f'{dir_path}\\SETT\\config.json', 'r', encoding='utf-8-sig') as f:
        data_config = json.load(f)
    return data_config

def get_data_product():
    with codecs.open(f'{dir_path}\\DATA\\products.json', 'r', encoding='utf-8-sig') as f:
        data_products = json.load(f)
    return data_products

def set_data_product (item):
    data = get_data_product()
    data[item['id']] = item
    with codecs.open(f'{dir_path}\\DATA\\products.json', 'w', encoding='utf-8-sig') as f:
        json.dump(data, f,ensure_ascii=False, indent=4)
    exec

def writer ():
   exec

def program ():
    config_data = get_config()
    config_links = quickstart.get_values()
    view = config_data['view']

    for product_id in config_links:
        _link = f'{domen_temp}{product_id[0]}'
        print(_link)
        req = requests.get(_link, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        product_data = {}
        
        #Назва продукту 
        product_title = soup.find(id='productTitle').text.strip()
        
        #Категорія та підкатегорія
        product_category_area = soup.find(id='wayfinding-breadcrumbs_feature_div')
        product_category_list = product_category_area.find_all('li')
        product_subcategory = product_category_list[-1].find('a').text.strip()
        product_category = product_category_list[0].find('a').text.strip()

        #Наявність товару
        try:
            is_stock = soup.find(id='exports_desktop_outOfStock_buybox_message_feature_div').find('span').text.strip()
            if (is_stock == 'Temporarily out of stock.'):
                exec
            else:
                is_stock = 'true'    
        except:
            is_stock = 'true'
        
        #Ціна товару
        try:
            product_price = soup.find(id='price_inside_buybox').text.strip()
        except Exception as er:
            try:
                product_price = soup.find(id='kindle-price').text.strip()
            except Exception:
                product_price = ''

        # Запис результату в JSON файл
        product_link_tm = _link.split('?')[0]
        product_data['title'] = product_title
        product_data['category'] = product_category
        product_data['subcategory'] = product_subcategory
        product_data['link'] = f'{product_link_tm}'
        product_data['price'] = product_price
        product_data['stock'] = is_stock,
        product_data['id'] = product_id[0]
        set_data_product(product_data)

        print(product_title)
    writer()
    quickstart.main(config_links)

program()