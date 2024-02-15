# import required libraries
import cv2

# Read two images as grayscale images
img = cv2.imread(r"shape_all.jpg",cv2.IMREAD_UNCHANGED)
cv2.imshow('im1',img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

template = cv2.imread(r"hammer.jpg",cv2.IMREAD_UNCHANGED)
cv2.imshow('Template',template)
gray1 = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
h,w = template.shape[0], template.shape[1]

# Apply thresholding on the images to convert to binary images
ret, thresh1 = cv2.threshold(gray, 90, 255,0)
ret, thresh2 = cv2.threshold(gray1, 90, 255,0)
cv2.imshow("Thresholded1", thresh1)
cv2.imshow("Thresholded2", thresh2)

# find the contours in the binary image
contours1,hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print("Number of Shapes detected in Image 1:",len(contours1))
cnt1 = contours1[0]
res_cpy = img.copy()
cv2.drawContours(image=res_cpy, contours=contours1, contourIdx=-1, color=(0, 255, 0), thickness=5, lineType=cv2.LINE_AA)
cv2.imshow("contour", res_cpy)


contours2,hierarchy = cv2.findContours(thresh2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print("Number of Shapes detected in Image 2:",len(contours2))
cnt2 = contours2[1]
res_cpy1 = template.copy()
cv2.drawContours(image=res_cpy1, contours=contours2, contourIdx=-1, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
cv2.imshow("contour1", res_cpy1)
ret_max=1
c_max=None
for c in contours1:
        ret = cv2.matchShapes(c, cnt2, 3, 0.0)
        if ret < .5 and ret <ret_max: 
            ret_max = ret
            c_max =c

x,y,w,h = cv2.boundingRect(c_max)
cv2.rectangle(img, (x, y), (x+w, y+h), (255,255, 255), 3)
cv2.imshow("img", img)
cv2.imwrite("shape.jpg", img)
print("Matching Image 1 with Image 2:", ret_max)
cv2.waitKey(0)
 
cv2.destroyAllWindows()