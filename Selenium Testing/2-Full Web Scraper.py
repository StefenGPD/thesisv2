import requests
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import cv2
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np
# Accepts a string, the url
# Writes into Extracted.csv
def downloadPage(urlname, pagecheck):
    PATH = "Selenium Testing/chromedriver.exe"

    #Because executable path is deprecated, use Service instead
    driver_service = Service(executable_path=PATH)

    #select the web browser
    driver = webdriver.Chrome(service=driver_service)

    driver.get(urlname)

    driver.fullscreen_window()

    # Scroll down to load images
    for i in range(15):
        driver.execute_script("window.scrollBy(0,300)", "")
        time.sleep(0.8)

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
        df.to_csv('Selenium Testing/Extracted.csv', index=False)
    else:
        df1 = pd.read_csv('Selenium Testing/Extracted.csv')
        df1.columns = column_names
        
        compiled_list = [name_list, price_list, url_list, img_list]
        df2 = pd.DataFrame(compiled_list).transpose()
        df2.columns = column_names

        df = pd.concat([df1, df2], ignore_index=True)
        df.to_csv('Selenium Testing/Extracted.csv', index=False)

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
def download_images(csv_name='Selenium Testing/Extracted.csv'):
    # Read the csv file
    df = pd.read_csv(csv_name)

    for index, row in df.iterrows():
        link = row['Img URL']
        filename = row['itemId']

        filepath = f"Selenium Testing/Images/{filename}.jpg"

        save_image(link, filepath)

# Provides itemId to the entire csv file
def giveItemId(csv_name='Selenium Testing/Extracted.csv'):
    df = pd.read_csv(csv_name)
    df['itemId'] = df.index + 1
    df.to_csv(csv_name)


def iterate_and_compare(csv_name='Selenium Testing/Extracted.csv'):
    df = pd.read_csv(csv_name)
    num_obj = len(df.index)
    threshold = 0.70
    cluster_count = 0
    #create list with number of items as size and initialize all elements to -1 (-1 = no cluster)
    cluster_list = [-1] * num_obj

    #while there are still elements without an assigned cluster
    while(-1 in cluster_list):
        no_cluster_index = cluster_list.index(-1)

        #conversion part to ensure numpy array (image values) is in rgb format, not cmyk 
        img1 = Image.open(f"Selenium Testing/Images/{no_cluster_index + 1}.jpg").convert("RGB")
        #Stefen: added img1save to save the image later on
        img1save = Image.open(f"Selenium Testing/Images/{no_cluster_index + 1}.jpg").convert("RGB")
        img1 = np.array(img1)
        img1 = img1[:, :, ::-1].copy()
        img1 = cv2.resize(img1, (400,400))

        #iterate from the element next to the -1 value onwards till the end and compare image similarity
        #if image already has a cluster, continue on to the next interation
        #if not, we compare the image with model image, if similarity passes the threshold, we assign the image the same cluster
        for index in range(no_cluster_index + 1, num_obj):
            if cluster_list[index] != -1:
                continue
            img2 = Image.open(f"Selenium Testing/Images/{index + 1}.jpg").convert("RGB")
            #Stefen: added img2save to save the image later on
            img2save = Image.open(f"Selenium Testing/Images/{index + 1}.jpg").convert("RGB")
            img2 = np.array(img2)
            img2 = img2[:, :, ::-1].copy()
            img2 = cv2.resize(img2, (400,400))
            similarity =  ssim(img1, img2, channel_axis=2)
            if similarity >= threshold:
                cluster_list[index] = (f"Cluster: {cluster_count}", similarity)

                # This part saves the image
                img2save.save(f"Selenium Testing/Clustered Images/Cluster {cluster_count} - {index + 1}.jpg")

            #print this if u want
            #print(similarity)
           
        #assign a cluster to model image
        cluster_list[no_cluster_index] = (f"Cluster: {cluster_count}", "distinct image")
        #Save the image
        
        img1save.save(f"Selenium Testing/Clustered Images/Cluster {cluster_count} - {index + 1}.jpg")
        cluster_count = cluster_count + 1
    
    df['Cluster_Similarity'] = cluster_list
    df.to_csv(csv_name, index = False)
    
    
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
    iterate_and_compare()


main()