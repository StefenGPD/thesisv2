# Selenium Tutorial 1
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

PATH = "chromedriver.exe"

#Because executable path is deprecated, use Service instead
driver_service = Service(executable_path=PATH)

#select the web browser
driver = webdriver.Chrome(service=driver_service)

driver.get('https://www.lazada.com.ph/catalog/?page=1&q=earphones')

#Waits and then closes the tab
time.sleep(2)
driver.close()

# close() for tab, quit() for entire browser