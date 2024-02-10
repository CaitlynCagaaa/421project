import cv2
import numpy as np
 
# Read the original image
img = cv2.imread(r'boundries/im15s1match.jpg') 
img1 = cv2.imread(r'boundries/im15full.jpg') 
# Display original image
cv2.imshow('Original', img)
cv2.waitKey(0)
 
# Convert to graycsale
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
# Blur the image for better edge detection
img_blur = cv2.GaussianBlur(img_gray, (15,15), 0) 
img_blur1 = cv2.GaussianBlur(img_gray1, (15,15), 0) 
 
# Sobel Edge Detection
sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=7) # Sobel Edge Detection on the X axis
sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=7) # Sobel Edge Detection on the Y axis
sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=7) # Combined X and Y Sobel Edge Detection
# Display Sobel Edge Detection Images
cv2.imshow('Sobel X', sobelx)
cv2.waitKey(0)
cv2.imshow('Sobel Y', sobely)
cv2.waitKey(0)
cv2.imshow('Sobel X Y using Sobel() function', sobelxy)
cv2.waitKey(0)
 
# Canny Edge Detection
edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=200) # Canny Edge Detection
edges1 = cv2.Canny(image=img_blur1, threshold1=150, threshold2=200)
# Display Canny Edge Detection Image
cv2.imshow('Canny Edge Detection', edges)
h,w = edges.shape[0], edges.shape[1]

matched = cv2.matchTemplate(edges1,edges, cv2.TM_CCOEFF_NORMED)
threshold = .1

(y_points, x_points) = np.where( matched >= threshold)

for pt in zip( x_points,y_points):
   cv2.rectangle(img1, pt, (pt[0] + w, pt[1] + h), (0,255,255), 5)
result =cv2.resize(img1,(700,700))
cv2.imshow('Matched with Template',result)
edges1 =cv2.resize(edges1,(2000,2000))
cv2.imshow('edges1',edges1)
cv2.waitKey(0)
 
cv2.destroyAllWindows()