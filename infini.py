import atexit
import asyncio
import time
import json
import psutil
from bs4 import BeautifulSoup
from pyrogram import Client as TelegramClient, errors
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
api_id = '22569112'
api_hash = '46f5072df87ee8dae7ce4fd138d52df9'
bot_token = '6862866677:AAHS9zLBJF7iR3sRR_TJ5nDWsAQNfTEjLy8'
group_id = -1002090703470

app = TelegramClient("my_bot", api_id, api_hash, bot_token=bot_token)
driver = None

def initialize_driver():
    global driver
    chrome_options = Options()
    chrome_options.add_argument("--window-size=800,600")
    chrome_options.add_argument("--window-position=0,0")
    driver = webdriver.Chrome(options=chrome_options)

def quit_driver():
    global driver
    if driver:
        driver.quit()
        driver = None
    
    for process in psutil.process_iter():
        if process.name() == "chrome" or process.name() == "chromedriver":
            process.kill()

atexit.register(quit_driver)

async def data(url, scroll):
    global driver
    initialize_driver()
    driver.get(url)
    scroll_amount = 1200
    time.sleep(3)
    for _ in range(scroll):
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        if (_ + 1) % 10 == 0:  # Check every 20 scrolls
                    # Scroll up 2000 pixels
                    driver.execute_script(f"window.scrollBy(0, {-2000});")
                    time.sleep(1) 
            
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "p-card-wrppr")))
        except Exception as e:
            print(f"Error while waiting for page to load: {e}")
        time.sleep(1.5)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    urunler = soup.find_all('div', class_='p-card-wrppr with-campaign-view')

    urun_bilgileri = []
    for urun in urunler:
        urun_fiyat = urun.find('div', class_='prc-box-dscntd')
        if urun_fiyat:
            fiyat_text = urun_fiyat.text.strip()
            try:
                fiyat_text = fiyat_text.replace('TL', '').replace('.', '').replace(',', '.')
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

            match = re.search(r'-p-(\d+)', link)
            urun_id = match.group(1) if match else None

        for urun_ismi in urun_isimleri:
            isim = urun_ismi['title'].strip()

            urun_bilgileri.append({
                "name": isim,
                "price": fiyat,
                "link": link,
                "id": urun_id
            })
    quit_driver()
    return urun_bilgileri

def save_previous_prices(previous_prices):
    with open('previous_prices.json', 'w') as file:
        json.dump(previous_prices, file)

def load_previous_prices():
    try:
        with open('previous_prices.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

previous_prices = load_previous_prices()

async def send_message_to_group(group_id, message):
    while True:
        try:
            await app.send_message(group_id, message)
            await asyncio.sleep(2)
            break
        except errors.FloodWait as e: 
            print(f"FloodWait hatası aldı: {e.x} saniye bekleniyor.")
            await asyncio.sleep(e.x)

async def main():
    while True:
        brands = {
            'karisik': ("https://www.trendyol.com/sr?wb=794,101939,101470,145557&wc=109460&attr=290|165569_19006_7205_7206_285902_286467_4183_11046&sst=BEST_SELLER", 100)
        }

        previous_prices = load_previous_prices()  

        for brand, (url, scroll) in brands.items():
            new_products = await data(url=url, scroll=scroll)
            brand_prices = previous_prices.get(brand, {})  

            for product in new_products:
                product_name = product["name"]
                product_price = product["price"]
                product_id = product["id"]

                if product_id in brand_prices:
                    previous_price = brand_prices[product_id]["price"]
                    if product_price < previous_price and (previous_price - product_price) / previous_price >= 0.02:
                        message = (
                            f"{product_name} ürününün fiyatı değişti!\nEski Fiyat: {previous_price}\nYeni Fiyat: {product_price}\nÜrün Linki: {product['link']}\nÜrün ID: {product_id}"
                        )
                        await send_message_to_group(group_id, message)

                brand_prices[product_id] = {"price": product_price, "name": product_name, "link": product["link"]}

            previous_prices[brand] = brand_prices 

        save_previous_prices(previous_prices) 
        await asyncio.sleep(30)

app.start()
app.run(main())
app.idle()