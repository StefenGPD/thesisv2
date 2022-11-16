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
import os, glob, re, sys
import shutil
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QStackedWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import Qt,QUrl, QTimer

#GUI
class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("GUI/WelcomeScreen.ui", self)
        self.counter = 0
        self.n = 200 # total instance

        self.timer = QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(20)


    def loading(self):
        self.progressBar.setValue(self.counter)

        if self.counter == int(self.n * 0.3):
            self.labelDescription.setText('<strong>Loading...</strong>')
        elif self.counter == int(self.n * 0.6):
            self.labelDescription.setText('<strong>Loading User Interface...</strong>')
        elif self.counter >= self.n:
            self.timer.stop()
            time.sleep(1)
            widget.setCurrentIndex(widget.currentIndex()+1)

        self.counter += 1

class MainScreen(QDialog):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("GUI/MainScreen.ui", self)
        
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("GUI/search icon.png"))
        
        self.searchButton = QtWidgets.QPushButton(self.searchFrame)
        self.searchButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.searchButton.setIcon(icon)
        self.searchButton.setIconSize(QtCore.QSize(30, 50))
        self.searchButton.setObjectName("searchButton")
        self.horizontalLayout.addWidget(self.searchButton, 0, QtCore.Qt.AlignRight)

        self.searchButton.clicked.connect(self.gotoInputPageDialog) 

    def gotoInputPageDialog(self):
        pages_number, done1 = QtWidgets.QInputDialog.getInt(self, 'Item Search', 'Enter number of pages:')
        main_search(self, pages_number)
        
    def link(self, itemURL):
        QDesktopServices.openUrl(QUrl(itemURL))
    
    def gotoCreateWidgets(self):
        #Sorts the image number in ascending order
        def numericalSort(value):
            parts = numbers.split(value)
            parts[1::2] = map(int, parts[1::2])
            return parts
        
        df = pd.read_csv('Extracted and Cheapest Selected.csv')
        imgPaths = []

        for File in sorted(glob.glob('Distinct Images/*.jpg'), key=numericalSort):
            imgPaths.append(os.path.join(File))

        # rows
        for index, row in df.iterrows():
                    newName = "label" + str(index)

                    #Product Number
                    self.label = QtWidgets.QLabel(self.ProductResultFrame)
                    self.label.setMaximumSize(QtCore.QSize(20, 200))
                    self.label.setWordWrap(True)
                    self.label.setText(str(index+1))
                    self.label.setObjectName(newName)
                    self.label.setStyleSheet("color: rgb(255, 255, 255);")
                    self.gridLayout.addWidget(self.label, index, 0, 1, 1)
                    
                    #Product Image
                    self.label = QtWidgets.QLabel(self.ProductResultFrame)
                    self.label.setObjectName(newName)
                    self.label.setPixmap(QtGui.QPixmap(imgPaths[index]))
                    self.label.setScaledContents(True)
                    self.label.setMaximumSize(QtCore.QSize(200, 200))
                    self.gridLayout.addWidget(self.label, index, 1, 1, 1)
        
                    #Product Name
                    self.label = QtWidgets.QLabel(self.ProductResultFrame)
                    self.label.setMaximumSize(QtCore.QSize(400, 200))
                    self.label.setWordWrap(True)
                    self.label.setText(row["Name"])
                    self.label.setObjectName(newName)
                    self.label.setStyleSheet("color: rgb(255, 255, 255);")
                    self.gridLayout.addWidget(self.label, index, 2, 1, 1)

                    #Product Price
                    self.label = QtWidgets.QLabel(self.ProductResultFrame)
                    self.label.setMaximumSize(QtCore.QSize(50, 100))
                    self.label.setText(str(row["Price"]))
                    self.label.setObjectName(newName)
                    self.label.setStyleSheet("color: rgb(255, 255, 255);")
                    self.gridLayout.addWidget(self.label, index, 3, 1, 1)

                    #Product Link
                    itemURL = row["Item URL"]
                    self.linkButton = QtWidgets.QLabel(self.ProductResultFrame)
                    self.linkButton.setMaximumSize(QtCore.QSize(100, 200))
                    self.linkButton.setText(f"<a href ={itemURL} style=color:#3498DB;>Proceed to Website</a>")
                    self.linkButton.setObjectName(newName)
                    self.linkButton.linkActivated.connect(self.link)
                    #self.linkButton.setStyleSheet("color: rgb(98, 114, 164);")
                    self.gridLayout.addWidget(self.linkButton, index, 4, 1, 1)
        print("Selection done. Feel free to browse!")

# Accepts a string, the url
# Writes into Extracted.csv
def downloadPage(urlname, pagecheck):
    print("Accessing the pages...")
    PATH = "chromedriver.exe"

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

def download_distinct_images(self):
    DirPath = 'Extracted and Cheapest Selected.csv'

    df = pd.read_csv(DirPath)
    price_sorted = df.sort_values(by=['Price'], ascending=True)
    price_sorted['sortedId'] = df.index + 1
    price_sorted.set_index("sortedId", inplace=True)
    price_sorted.to_csv(DirPath)

    #print(df.loc[:, ["Name","Price", "Img URL", "Cluster_Number"]])

    def save_image(link, filename):
        with open(filename, 'wb') as f:
            f.write(requests.get(link).content)

    for index, row in price_sorted.iterrows():
        link = row['Img URL']
        filename = index
        filepath = f"Distinct Images/{filename}.jpg"
        save_image(link, filepath)
    
    self.gotoCreateWidgets()

    

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
    print("Downloading individual images from the site...")
    # Read the csv file
    df = pd.read_csv(csv_name)

    for index, row in df.iterrows():
        link = row['Img URL']
        filename = row['itemId']

        filepath = f"Images/{filename}.jpg"

        save_image(link, filepath)

# Provides itemId to the entire csv file
def giveItemId(csv_name='Extracted.csv'):
    print("Assigning itemIds to each item in the csv file...")
    df = pd.read_csv(csv_name)
    df['itemId'] = df.index + 1
    df.to_csv(csv_name)


def iterate_and_compare(self, csv_name='Extracted.csv', threshold=0.9):
    print("Initiating the clustering algorithm...")
    df = pd.read_csv(csv_name)
    num_obj = len(df.index)

    directorypath = f"Clustered SSIM {threshold}"
    #Create the directory to store images in
    try:
        os.mkdir(directorypath)
    except:
        print(f"{directorypath} already exists, removing and recreating the directory.")
        shutil.rmtree(directorypath)
        os.mkdir(directorypath)

    cluster_count = 0
    #create list with number of items as size and initialize all elements to -1 (-1 = no cluster)
    cluster_list = [-1] * num_obj

    #while there are still elements without an assigned cluster
    while(-1 in cluster_list):
        no_cluster_index = cluster_list.index(-1)


        print(f"Looking for candidates for cluster {no_cluster_index}...")
        #conversion part to ensure numpy array (image values) is in rgb format, not cmyk 
        img1 = Image.open(f"Images/{no_cluster_index + 1}.jpg").convert("RGB")
        #Stefen: added img1save to save the image later on
        img1save = Image.open(f"Images/{no_cluster_index + 1}.jpg").convert("RGB")
        img1 = np.array(img1)
        img1 = img1[:, :, ::-1].copy()
        img1 = cv2.resize(img1, (400,400))

        #iterate from the element next to the -1 value onwards till the end and compare image similarity
        #if image already has a cluster, continue on to the next interation
        #if not, we compare the image with model image, if similarity passes the threshold, we assign the image the same cluster
        for index in range(no_cluster_index + 1, num_obj):
            if cluster_list[index] != -1:
                continue
            img2 = Image.open(f"Images/{index + 1}.jpg").convert("RGB")
            #Stefen: added img2save to save the image later on
            img2save = Image.open(f"Images/{index + 1}.jpg").convert("RGB")
            img2 = np.array(img2)
            img2 = img2[:, :, ::-1].copy()
            img2 = cv2.resize(img2, (400,400))
            similarity =  ssim(img1, img2, channel_axis=2)
            if similarity >= threshold:
                cluster_list[index] = (cluster_count, similarity)

                # This part saves the image
                img2save.save(f"{directorypath}/Cluster {cluster_count} - {index + 1}.jpg")

            #print this if u want
            #print(similarity)
            #print(index)
           
        #assign a cluster to model image
        cluster_list[no_cluster_index] = (cluster_count, "distinct image") 
        #Save the image
        
        img1save.save(f"{directorypath}/Cluster {cluster_count} - {no_cluster_index + 1}.jpg")
        cluster_count = cluster_count + 1
    df['Cluster_Similarity'] = cluster_list
    df.to_csv(f"Extracted SSIM - Threshold {threshold}.csv", index = False)
    selecting_cheapest_product(self)
    

def selecting_cheapest_product(self):
    print("Selecting the cheapest products per cluster...")
    # Note: when saving to csv, and then reading, all datatypes get converted to STRING
    # This long ass read_csv converts columns into appropriate datatypes
    df = pd.read_csv("Extracted SSIM - Threshold 0.9.csv", converters={'itemId': pd.eval, 'Cluster_Similarity': pd.eval})

    try:
        df['Price'] = df['Price'].apply(lambda x : x.replace(',',''))
    except:
        pass

    # List comprehension: access the column name (series), what index (value), and the first item of the value
    cluster_number = [df['Cluster_Similarity'][index][0] for index in df.index]
    df['Cluster_Number'] = cluster_number

    df = df.sort_values(by=['Cluster_Number', 'Price'])

    # Ignore column 0
    cheapest_df = pd.DataFrame(columns=df.columns)

    # Make a list of clusters to iterate over as a condition (i.e., if Cluster_Number == cluster in list)
    # Extract a subset of dataframe using the condition

    cluster_set = list(set(df['Cluster_Number']))

    for cluster_num in cluster_set:
        df_portion = df[df['Cluster_Number'] == cluster_num]
        # Since dataframe is sorted secondarily by price, this will always be the cheapest option
        df_portion = df_portion.iloc[0]

        cheapest_df.loc[len(cheapest_df.index)] = list(df_portion)

    # Removes the unnecessary first column and saves it
    cheapest_df = cheapest_df.drop(['Unnamed: 0'], axis=1)
    cheapest_df.to_csv('Extracted and Cheapest Selected.csv', index=False)
    download_distinct_images(self)

    
def main_search(self, pages_number):
    searchword = self.searchBox.text()
    pages = pages_number

    page_list = make_search(searchword, pages)

    pagecheck = True
    for page in page_list:
        script_text = downloadPage(page, pagecheck)
        
        pagecheck = False
    
    giveItemId()
    download_images()
    iterate_and_compare(self)

def createDirectories():
    dirlist = ['Distinct Images', 'Images']
    
    for directory in dirlist:
        try:
            os.mkdir(directory)
        except:
            print(f"{directory} already exists, removing and recreating the directory.")
            shutil.rmtree(directory)
            os.mkdir(directory)


# Main
app = QApplication(sys.argv)
welcome = WelcomeScreen()
main = MainScreen() 
numbers = re.compile(r'(\d+)')

widget = QStackedWidget()
widget.addWidget(welcome)
widget.addWidget(main)
widget.setFixedHeight(900)
widget.setFixedWidth(1000)
widget.show()

# Handles directories to refresh the content
createDirectories()


try:
    sys.exit(app.exec())
except:
    print('exiting')

#main()