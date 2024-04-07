import imutils
import cv2
url = "https://users.tricity.wsu.edu/~jhmiller/CS%20434-534/MATLAB/test%20Flowers/crocus/image_0321.jpg"
image =imutils.url_to_image(url)
cv2.imshow("check",image)
cv2.waitKey(0)