# import required packages for performing OCR
import cv2
import pytesseract
import numpy as np
from matplotlib import pyplot as plt
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# Reading image file from where the text is to be extracted
img1 = cv2.imread("boundries/im15full.jpg")

# Converting the image into to gray scaled image
Gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
ret1, thresh_1 = cv2.threshold(Gray1, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
result =cv2.resize(thresh_1,(500,500))
cv2.imshow("op", result)
# specifying structure shape, kernel size, increase/decreases the kernel area
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh_1,cv2.MORPH_OPEN,kernel, iterations = 1)
result =cv2.resize(opening,(500,500))
cv2.imshow("ope", result)
dilation1 = cv2.dilate(opening, kernel, iterations = 1)
result =cv2.resize(dilation1,(500,500))
cv2.imshow("open", result)
# finding contouring for the image
contours1, hierarchy1 = cv2.findContours(dilation1, cv2.RETR_EXTERNAL,
cv2.CHAIN_APPROX_NONE)
# creating a copy
img2 = img1.copy()
file1 = open("recognized.txt", "w+")
file1.write("")
file1.close()
# looping for ocr through the contours found
for cnt in contours1:
 x1, y1, w1, h1 = cv2.boundingRect(cnt)
 rect1 = cv2.rectangle(img2, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)
 cropped1 = img2[y1:y1 + h1, x1:x1 + w1]
 file_1 = open("recognized.txt", "a")
# apply ocr
 text_1 = pytesseract.image_to_string(cropped1)
 file_1.write(text_1)
 file_1.close
cv2.waitKey(0)
cv2.destroyAllWindows()