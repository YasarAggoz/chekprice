import atexit
import asyncio
import time
import subprocess
import psutil
from bs4 import BeautifulSoup
from pyrogram import Client as TelegramClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

api_id = '22569112'
api_hash = '46f5072df87ee8dae7ce4fd138d52df9'
bot_token = '6862866677:AAHS9zLBJF7iR3sRR_TJ5nDWsAQNfTEjLy8'
target_username = '+905543529640'
chatid = '1385445024'
group_id = -1002090703470

app = TelegramClient("my_bot", api_id, api_hash, bot_token=bot_token)
driver = None

def initialize_driver():
    global driver
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1,1")
    chrome_options.add_argument("--window-position=0,0")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

def quit_driver():
    global driver
    if driver:
        driver.quit()
        driver = None
    # Tüm Chrome ve chromedriver süreçlerini kapat
    for process in psutil.process_iter():
        if process.name() == "chrome" or process.name() == "chromedriver":
            process.kill()

# Kapanışta driver'ı kapatmak ve süreçleri sonlandırmak için register
atexit.register(quit_driver)

async def data(url, scroll):
    global driver
    initialize_driver()
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

            urun_bilgileri.append([isim, fiyat, link])

    return urun_bilgileri

async def send_message_to_group(group_id, message):
    while True:
        try:
            await app.send_message(group_id, message)
            break
        except FloodWait as e:  # type: ignore
            print(f"FloodWait hatası aldı: {e.x} saniye bekleniyor.")
            await asyncio.sleep(e.x)
previous_products_samsung = {}
previous_products_xiaomi = {}
previous_products_apple = {}
previous_products_huawei = {}
previous_products_oppo = {}
previous_products_realme = {}
previous_products_poco = {}
previous_products_karisik = {}

previous_prices = {
    'samsung': {},
    'xiaomi': {},
    'apple': {},
    'huawei': {},
    'oppo': {},
    'realme': {},
    'poco': {},
    'karisik': {}
}

async def main():
    while True:
        brands = {
            'samsung': ("https://www.trendyol.com/sr?wb=794&wc=109460&attr=290%7C4183_11046&sst=PRICE_BY_ASC", 30),
            'xiaomi': ("https://www.trendyol.com/sr?wb=101939&wc=109460&attr=290%7C7206_4183_165569&sst=PRICE_BY_ASC", 30),
            'apple': ("https://www.trendyol.com/sr?wc=109460&wb=101470&sst=PRICE_BY_ASC", 25),
            'huawei': ("https://www.trendyol.com/sr?wb=103505&wc=109460&attr=290|4183_286816&sst=PRICE_BY_ASC", 5),
            'oppo': ("https://www.trendyol.com/sr?wb=109251&wc=109460&attr=290%7C4183_285902&sst=PRICE_BY_ASC", 5),
            'realme': ("https://www.trendyol.com/sr?wb=145557&wc=109460&attr=290|4183_7205_7206_285902_286467&sst=PRICE_BY_ASC", 10),
            'poco': ("https://www.trendyol.com/sr?wb=142700&wc=109460&attr=290|7206_4183_165569&sst=PRICE_BY_ASC", 5),
            'karisik': ("https://www.trendyol.com/sr?wb=159554%2C108166%2C103503%2C158303%2C161474%2C149729%2C103502%2C105074&wc=109460&attr=290%7C137119_4182_7206_286467_312768_4183_23352_165569&sst=PRICE_BY_ASC&pi=5", 30)
        }
        for brand, (url, scroll) in brands.items():
            new_products = await data(url=url, scroll=scroll)
            for product in new_products:
                product_name = product[0]
                product_price = product[1]

                if product_name in previous_prices[brand]:
                    previous_price = previous_prices[brand][product_name]
                    if product_price < previous_price and (previous_price - product_price) / previous_price >= 0.02:
                        message = (
                            f"{product_name} ürününün fiyatı değişti!\nEski Fiyat: {previous_price}\nYeni Fiyat: {product_price}\nÜrün Linki: {product[2]}"
                        )
                        await send_message_to_group(group_id, message)

                    previous_prices[brand][product_name] = product_price
                else:
                    previous_prices[brand][product_name] = product_price

            await asyncio.sleep(5)

app.start()
app.run(main())
app.idle()