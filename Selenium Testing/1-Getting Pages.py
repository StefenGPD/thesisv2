import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

PATH = "C:/Users/StefenGPD/Desktop/THE01 - Thesis/Prototype Workspace/Selenium Testing/chromedriver.exe"

#Because executable path is deprecated, use Service instead
driver_service = Service(executable_path=PATH)

#select the web browser
driver = webdriver.Chrome(service=driver_service)

driver.get('https://www.lazada.com.ph/catalog/?page=1&q=earphones')

# Scroll down to load images
# for i in range(15):
#     driver.execute_script("window.scrollBy(0,300)", "")
#     time.sleep(0.4)

# Class codes for items
# 'ooOxS' - price of an item
# 'jBwCF' - image
# 'RfADt' - name of item, url of item is also here through a tag
# '_95X4G' - selector for image
# 'aBrP0' - selector for prices

# Find elements will return a list of object
prices = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.aBrP0 > span.ooOxS')))
names = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'RfADt')))
imgs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div._95X4G > a > div > img.jBwCF')))
urls = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.RfADt > a')))
assert (len(prices) == len(names) == len(imgs) == len(urls)), f"Prices: {len(prices)}, Names: {len(names)}, Imgs: {len(imgs)}, Urls: {len(urls)}"
price_list = []
name_list = []
img_list = []
url_list = []
# element.text extracts the item in the list

# Pattern for getting price, name
# for i in range(len(price_list)):
#     price = price_list[i].text[1:]
#     name = name_list[i].text

#     print(f"{name} costs {price} pesos.")

# Pattern for getting imgUrl
# for i in range(len(price_list)):
#     img = img_list[i]
#     src = img.get_attribute('src')
    
#     print(src)


# for i in range(len(price_list)):
#     url = url_list[i].get_attribute('href')
#     print(url)

for i in range(len(prices)):
    price = prices[i].text[1:]
    price_list.append(price)

    name = names[i].text
    name_list.append(name)

    img = imgs[i]
    src = img.get_attribute('src')
    img_list.append(src)

    url = urls[i].get_attribute('href')
    url_list.append(url)

# Format: name, price, url, imgUrl
column_names = ['Name', 'Price', 'Item URL', 'Img URL']
compiled_list = [name_list, price_list, url_list, img_list]
df = pd.DataFrame(compiled_list).transpose()

df.to_csv("Extracted.csv")
    

# close() for tab, quit() for entire browser

