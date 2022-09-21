import requests
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Accepts a string, the url
# Writes into Extracted.csv
def downloadPage(urlname, pagecheck):
    PATH = "C:/Users/StefenGPD/Desktop/THE01 - Thesis/Prototype Workspace/Selenium Testing/chromedriver.exe"

    #Because executable path is deprecated, use Service instead
    driver_service = Service(executable_path=PATH)

    #select the web browser
    driver = webdriver.Chrome(service=driver_service)

    driver.get(urlname)

    # Scroll down to load images
    for i in range(15):
        driver.execute_script("window.scrollBy(0,300)", "")
        time.sleep(0.4)

    # Class codes for items
    # 'ooOxS' - price of an item
    # 'jBwCF' - image
    # 'RfADt' - name of item, url of item is also here through a tag

    # Find elements will return a list of object
    prices = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.aBrP0 > span.ooOxS')))
    names = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'RfADt')))
    imgs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div._95X4G > a > div > img.jBwCF')))
    urls = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.RfADt > a')))

    # Asserts if they are all the same size
    assert (len(prices) == len(names) == len(imgs) == len(urls)), f"Prices: {len(prices)}, Names: {len(names)}, Imgs: {len(imgs)}, Urls: {len(urls)}"
    price_list = []
    name_list = []
    img_list = []
    url_list = []

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


    if pagecheck==True:
        compiled_list = [name_list, price_list, url_list, img_list]
        df = pd.DataFrame(compiled_list).transpose()
        df.columns = column_names
        df.to_csv('Extracted.csv', index=False)
    else:
        df1 = pd.read_csv('Extracted.csv')
        df1.columns = column_names
        
        compiled_list = [name_list, price_list, url_list, img_list]
        df2 = pd.DataFrame(compiled_list).transpose()
        df2.columns = column_names

        df = pd.concat([df1, df2], ignore_index=True)
        df.to_csv('Extracted.csv', index=False)

    # Ensures that the browser is quit
    driver.quit()

# Creates a search link using keywords
# Accepts a string, the keyword(s), and returns a list of search links
def make_search(keyword, pages=1):
    page_list = []
    keywords = keyword.split()

    for i in range(pages):
        if len(keywords) <= 1:
            page_list.append(f"https://www.lazada.com.ph/catalog/?page={i+1}&q={keywords[0]}")
        else:
            indexcheck = 0
            builtword = ''
            for word in keywords:
                builtword += word
                indexcheck += 1

                if indexcheck != len(keywords):
                    builtword += '+'
                else:
                    pass
            page_list.append(f"https://www.lazada.com.ph/catalog/?page={i+1}&q={builtword}")
    
    return page_list

# Downloads the image in a given link
# Accepts 2 strings: link address and name of file to be saved   
def save_image(link, filename):

    # wb means open for writing in binary code
    with open(filename, 'wb') as f:
        f.write(requests.get(link).content)    

# Downloads all the images in a csv file
# If csv name is different, put a parameter
def download_images(csv_name='Extracted.csv'):
    # Read the csv file
    df = pd.read_csv(csv_name)

    for index, row in df.iterrows():
        link = row['Img URL']
        filename = row['itemId']

        filepath = f"Images/{filename}.jpg"

        save_image(link, filepath)

# Provides itemId to the entire csv file
def giveItemId(csv_name='Extracted.csv'):
    df = pd.read_csv(csv_name)
    df['itemId'] = df.index + 1
    df.to_csv(csv_name)


def main():
    searchword = input("Enter the item to be searched: ")
    pages = int(input("How many pages to extract: "))

    page_list = make_search(searchword, pages)

    pagecheck = True
    for page in page_list:
        script_text = downloadPage(page, pagecheck)
        
        pagecheck = False
    
    giveItemId()
    download_images()


main()