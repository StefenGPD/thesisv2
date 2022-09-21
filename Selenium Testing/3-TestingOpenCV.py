import cv2
from skimage.metrics import structural_similarity as ssim


img1 = cv2.imread('Images/96.jpg', -1)
img2 = cv2.imread('Images/97.jpg', -1)

img1 = cv2.resize(img1, (400,400))
img2 = cv2.resize(img2, (400,400))

print(img1.shape)
print(img2.shape)

cv2.imshow('1',img1)
cv2.imshow('2',img2)


similarity = ssim(img1, img2, channel_axis=2)

print(similarity)

cv2.waitKey(0)
cv2.destroyAllWindows()