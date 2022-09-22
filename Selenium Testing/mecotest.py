import pandas as pd
import cv2
from skimage.metrics import structural_similarity as ssim
from PIL import Image
import numpy as np
# df = pd.read_csv('Selenium Testing\Extracted.csv')
# print(len(df.index))
# print(df.loc[0]["Item URL"])




arr_img1 = cv2.imread(f"Selenium Testing/Images/1.jpg", -1)
print(arr_img1)



img2 = Image.open("Selenium Testing/Images/1.jpg" )
arr_img2 = np.array(img2)
arr_img2 = arr_img2[:, :, ::-1].copy()


print(arr_img1 == arr_img2)