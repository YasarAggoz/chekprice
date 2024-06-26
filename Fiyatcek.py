import requests
import os
from bs4 import BeautifulSoup
import twilio
from twilio.rest import Client
import json
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from pyrogram import Client 
from selenium.webdriver.chrome.options import Options

def data(url,scroll):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=100,50")
    #chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    scroll_amount = 1400
    for _ in range(scroll): 
       driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
       time.sleep(1)  


    page_source = driver.page_source


    soup = BeautifulSoup(page_source, 'html.parser')


    urunler = soup.find_all('div', class_='p-card-wrppr with-campaign-view')

    urun_bilgileri = []

    for urun in urunler:
   
        urun_fiyat = urun.find('div', class_='prc-box-dscntd')
        if urun_fiyat:  
            fiyat_text = urun_fiyat.text.strip()  

        
            try:
                fiyat_text = fiyat_text.replace('TL', '').replace(',', '').replace('.', '')
                fiyat = float(fiyat_text)
            except ValueError:
                print(f"Fiyat Dönüştürme Hatası: {fiyat_text}")
                continue 

    
        urun_isimleri = urun.find_all('span', class_='prdct-desc-cntnr-name hasRatings')
        urun_link_elements = urun.find_all('a') 
        for urun_link_element in urun_link_elements:
         link = urun_link_element['href'].strip()  

        if link.startswith('/'):  
            link = f"https://www.trendyol.com{link}" 
           
        for urun_ismi in urun_isimleri:
            isim = urun_ismi['title'].strip()
    
       
        
            urun_bilgileri.append([isim, fiyat,link])



    driver.quit()
    return urun_bilgileri






previous_products_samsung = {}
previous_products_xiaomi = {}
previous_products_apple = {}
previous_products_huawei = {}
previous_products_oppo = {}
previous_products_realme = {}
previous_products_poco = {}

api_id = '22569112'
api_hash = '46f5072df87ee8dae7ce4fd138d52df9'
bot_token = '6862866677:AAHS9zLBJF7iR3sRR_TJ5nDWsAQNfTEjLy8'
target_username = '+905543529640'
chatid= '1385445024'
group_id = -1002090703470

while True:
    samsung = data(url="https://www.trendyol.com/sr?wc=109460&wb=794&sst=PRICE_BY_ASC",scroll=32)
    xiaomi = data (url="https://www.trendyol.com/sr?wc=109460&wb=101939&sst=PRICE_BY_ASC",scroll=32)
    apple = data(url="https://www.trendyol.com/sr?wc=109460&wb=101470&sst=PRICE_BY_ASC",scroll=24)
    huawei = data(url="https://www.trendyol.com/sr?wc=109460&wb=103505&sst=PRICE_BY_ASC",scroll=5)
    oppo = data(url="https://www.trendyol.com/sr?wc=109460&wb=109251&sst=PRICE_BY_ASC",scroll=5)
    realme = data(url="https://www.trendyol.com/sr?wc=109460&wb=145557&sst=PRICE_BY_ASC",scroll=10)
    poco = data(url="https://www.trendyol.com/sr?wc=109460&wb=142700&sst=PRICE_BY_ASC",scroll=5)
   

    for product in samsung:
        product_name = product[0]
        product_price = product[1]
        
        if product_name in previous_products_samsung:
            previous_price = previous_products_samsung[product_name]
            
            if product_price < previous_price and (previous_price - product_price) / previous_price >= 0.02:
                  message=(f"{product_name} ürününün fiyatı değişti!\nEski Fiyat: {previous_price}\nYeni Fiyat: {product_price}\nÜrün Linki: {product[2]}")
                  with Client ("my_account",api_id,api_hash) as app:
                   app.send_message(target_username,message)
        else:
            previous_products_samsung[product_name] = product_price
    
          
    for product in apple:
        product_name = product[0]
        product_price = product[1]
        
        if product_name in previous_products_apple:
            previous_price = previous_products_apple[product_name]
            
            if product_price < previous_price and (previous_price - product_price) / previous_price >= 0.02:
                  message=(f"{product_name} ürününün fiyatı değişti!\nEski Fiyat: {previous_price}\nYeni Fiyat: {product_price}\nÜrün Linki: {product[2]}")
                  with Client ("my_account",api_id,api_hash) as app:
                   app.send_message(target_username,message)
        else:
            previous_products_apple[product_name] = product_price   
  
  
    
    for product in xiaomi:
        product_name = product[0]
        product_price = product[1]
        
        if product_name in previous_products_xiaomi:
            previous_price = previous_products_xiaomi[product_name]
            if product_price < previous_price and (previous_price - product_price) / previous_price >= 0.02:
                  message=(f"{product_name} ürününün fiyatı değişti!\nEski Fiyat: {previous_price}\nYeni Fiyat: {product_price}\nÜrün Linki: {product[2]}")
                  with Client ("my_account",api_id,api_hash) as app:
                   app.send_message(target_username,message)
        else:
            previous_products_xiaomi[product_name] = product_price  
   
    
    for product in huawei:
        product_name = product[0]
        product_price = product[1]
        
        if product_name in previous_products_huawei:
            previous_price = previous_products_huawei[product_name]
            if product_price < previous_price and (previous_price - product_price) / previous_price >= 0.02:
                  message=(f"{product_name} ürününün fiyatı değişti!\nEski Fiyat: {previous_price}\nYeni Fiyat: {product_price}\nÜrün Linki: {product[2]}")
                  with Client ("my_account",api_id,api_hash) as app:
                   app.send_message(target_username,message)
        else:
            previous_products_huawei[product_name] = product_price   
  
    
    for product in oppo:
        product_name = product[0]
        product_price = product[1]
        
        if product_name in previous_products_oppo:
            previous_price = previous_products_oppo[product_name]
            if product_price < previous_price and (previous_price - product_price) / previous_price >= 0.02:
                  message=(f"{product_name} ürününün fiyatı değişti!\nEski Fiyat: {previous_price}\nYeni Fiyat: {product_price}\nÜrün Linki: {product[2]}")
                  with Client ("my_account",api_id,api_hash) as app:
                   app.send_message(target_username,message)
        else:
            previous_products_oppo[product_name] = product_price   
  
    
    for product in realme:
        product_name = product[0]
        product_price = product[1]
        
        if product_name in previous_products_realme:
            previous_price = previous_products_realme[product_name]
            if product_price < previous_price and (previous_price - product_price) / previous_price >= 0.02:
                  message=(f"{product_name} ürününün fiyatı değişti!\nEski Fiyat: {previous_price}\nYeni Fiyat: {product_price}\nÜrün Linki: {product[2]}")
                  with Client ("my_account",api_id,api_hash) as app:
                   app.send_message(target_username,message)
        else:
            previous_products_realme[product_name] = product_price   
        
    
    for product in poco:
        product_name = product[0]
        product_price = product[1]
        
        if product_name in previous_products_poco:
            previous_price = previous_products_poco[product_name]
            if product_price < previous_price and (previous_price - product_price) / previous_price >= 0.02:
                  message=(f"{product_name} ürününün fiyatı değişti!\nEski Fiyat: {previous_price}\nYeni Fiyat: {product_price}\nÜrün Linki: {product[2]}")
                  with Client ("my_account",api_id,api_hash) as app:
                   app.send_message(target_username,message)
        else:
            previous_products_poco[product_name] = product_price   
    
                  
    

    
    time.sleep(100)
    
    