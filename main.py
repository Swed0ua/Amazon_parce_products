import sys
import requests
from bs4 import BeautifulSoup
import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import codecs


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
    data[item['link']] = item
    with codecs.open(f'{dir_path}\\DATA\\products.json', 'w', encoding='utf-8-sig') as f:
        json.dump(data, f,ensure_ascii=False, indent=4)
    exec

def browser_init(view):
    ua = dict(DesiredCapabilities.CHROME)
    options = webdriver.ChromeOptions()
    if view == False:
        options.add_argument('headless')
        options.add_argument('window-size=1920x935')
    browser = webdriver.Chrome(chrome_options=options, service=Service(ChromeDriverManager().install()))
    return browser


def program ():
    config_data = get_config()
    config_links = config_data['links']
    view = config_data['view']
    browser = browser_init(view)

    for _link in config_links:
        req = requests.get('')
        browser.get(f'{_link}')
        for index in range (1, max_size):
            html = browser.page_source
            soup = BeautifulSoup(html, 'lxml')
            try:
                pages_count = int(soup.find_all(class_='s-pagination-item')[-2].text)
            except Exception:
                pages_count = 0
            print(pages_count)
            try:
                next_page = soup.find_all(class_='s-pagination-item')[-1].get('href')
            except:
                next_page = False
            product_list = soup.find_all(class_='s-result-item')
            if view == False:    
                time.sleep(15)
            else :
                time.sleep(2)
            for product in product_list:
                try:
                    product_data = {}
                    product_link = product.find('a', class_='a-link-normal').get('href')
                    browser.get(f'{site_domen}{product_link}')
                    html = browser.page_source
                    soup = BeautifulSoup(html, 'lxml')
                    print(product_link)
                    try:
                        product_price = soup.find(class_='price_inside_buybox').text
                    except Exception as er:
                        product_price = ''
                    product_title = soup.find(id='productTitle').text.strip()
                    #product_img = soup.find(class_='a-dynamic-image').get('src')
                    product_category_area = soup.find(id='wayfinding-breadcrumbs_feature_div')
                    product_category_list = product_category_area.find_all('li')
                    product_subcategory = product_category_list[-1].find('a').text.strip()
                    product_category = product_category_list[0].find('a').text.strip()
                    try:
                        is_stock = soup.find(id='exports_desktop_outOfStock_buybox_message_feature_div').find('span').text.strip()
                        if is_stock == ('Temporarily out of stock.'):
                            exec
                        else:
                            is_stock = 'true'    
                    except:
                        is_stock = 'true'
                    """ print(product_subcategory)
                    print(product_category) """
                    product_link_tm = product_link.split('?')[0]
                    product_data['title'] = product_title
                    product_data['category'] = product_category
                    product_data['subcategory'] = product_subcategory
                    product_data['link'] = f'{site_domen}{product_link_tm}'
                    product_data['price'] = product_price
                    product_data['stock'] = is_stock
                    print(product_data)
                    set_data_product(product_data)
                except Exception as e:
                    print(e)
                    print('No product element')
                print('----------------------------')
            if next_page == False or next_page == None:
                print('links item finish')
                break
            browser.get(f'{site_domen}{next_page}')
         

   
program()