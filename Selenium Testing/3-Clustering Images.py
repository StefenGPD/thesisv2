import cv2
import numpy as np
import pandas as pd
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from PIL import Image
import math
import os
import shutil

# Template for the testing
def compare(csv_name='Extracted.csv'):
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
                img2save.save(f"Clustered Images/Cluster {cluster_count} - {index + 1}.jpg")

            #print this if u want
            #print(similarity)
            print(index)
           
        #assign a cluster to model image
        cluster_list[no_cluster_index] = (cluster_count, "distinct image") 
        #Save the image
        
        img1save.save(f"Clustered Images/Cluster {cluster_count} - {no_cluster_index + 1}.jpg")
        cluster_count = cluster_count + 1
    
    df['Cluster_Similarity'] = cluster_list
    df.to_csv(csv_name, index = False)

# Default threshold of 0.70, may be adjusted if needed
# It also creates a folder with the format "Clustered SSIM {threshold}"
def compare_ssim(csv_name='Extracted.csv', threshold=0.70):
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
            print(index)
           
        #assign a cluster to model image
        cluster_list[no_cluster_index] = (cluster_count, "distinct image") 
        #Save the image
        
        img1save.save(f"{directorypath}/Cluster {cluster_count} - {no_cluster_index + 1}.jpg")
        cluster_count = cluster_count + 1
    
    df['Cluster_Similarity'] = cluster_list
    df.to_csv(f"Extracted SSIM - Threshold {threshold}.csv", index = False)


def main():
    compare_ssim(threshold=0.9)

main()