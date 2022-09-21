# Selenium Tutorial 1
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

PATH = "C:/Users/StefenGPD/Desktop/THE01 - Thesis/Prototype Workspace/Selenium Testing/chromedriver.exe"

#Because executable path is deprecated, use Service instead
driver_service = Service(executable_path=PATH)

#select the web browser
driver = webdriver.Chrome(service=driver_service)

driver.get('https://www.lazada.com.ph/catalog/?page=1&q=earphones')

# Find elements will return a list of object
products = driver.find_elements(By.CLASS_NAME, 'ooOxS')
print(type(products))

# element.text extracts the item in the list
for product in products:
    price = product.text
    price = price[1:] # Removes the peso sign at the start which causes the program to crash
    print(price)

# close() for tab, quit() for entire browser


# Class codes for items
# 'ooOxS' - price of an item
# 'jBwCF' - image 