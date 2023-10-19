import cv2
import numpy as np
from matplotlib import pyplot as plt
 
# Load the image
image = cv2.imread(r"C:\Users\caitl\OneDrive\Pictures\shadow_box1.jpg",cv2.IMREAD_UNCHANGED)
 
# Display the image

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
cv2.imshow("Im", gray)
ret, thresh = cv2.threshold(gray,90,255,cv2.THRESH_BINARY_INV )
cv2.imshow("Ima", thresh)
# noise removal
kernel = np.ones((3,3),np.uint8)
#cv2.imshow("kernel", kernel)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
cv2.imshow("open", opening)
# sure background area

sure_bg = cv2.dilate(opening,kernel,iterations=1)
cv2.imshow("Imag", sure_bg)
# Finding sure foreground area
dist_transform = cv2.distanceTransform(thresh,cv2.DIST_L1,5)
cv2.imshow("I", dist_transform)
ret, sure_fg = cv2.threshold(dist_transform,0.10*dist_transform.max(),255,50)
# Finding unknown region
sure_fg = np.uint8(sure_fg)
cv2.imshow("Imagee", sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)

# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)

# Add one to all labels so that sure background is not 0, but 1
markers = markers+1
# Now, mark the region of unknown with zero
markers[unknown==255] = 0
markers = cv2.watershed(image,markers)

image[markers == -1] = [255,0,0]
cv2.imshow("Image", image)
# Wait for the user to press a key
cv2.waitKey(0)
cv2.destroyAllWindows()