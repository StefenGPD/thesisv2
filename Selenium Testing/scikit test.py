import cv2
import numpy as np
import pandas as pd
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import mean_squared_error as mse
from PIL import Image


# Accepts an image, returns an ndarray of image
def img_to_array(img):
    img = np.array(img)
    img = img[:, :, ::-1].copy()
    img = cv2.resize(img, (400,400))

    return img


# Image 1 and Image 2 are same, Image 3 is different
img1 = Image.open('Images/13.jpg').convert('RGB')
img1 = img_to_array(img1)

img2 = Image.open('Images/55.jpg').convert('RGB')
img2 = img_to_array(img2)

img3 = Image.open('Images/92.jpg').convert('RGB')
img3 = img_to_array(img3)

### This entire process could be a function instead so I'll do that
# img1 = np.array(img1)
# img1 = img1[:, :, ::-1].copy()
# img1 = cv2.resize(img1, (400,400))

ssim_value = ssim(img1, img3, channel_axis=2)
psnr_value = psnr(img1, img3)
mse_value = mse(img1, img3)
print(ssim_value)
print(psnr_value)
print(mse_value)