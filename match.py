import cv2
import numpy as np

img = cv2.imread(r"boundries/im15full.jpg",cv2.IMREAD_UNCHANGED)
cv2.imshow('im1',img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

template = cv2.imread(r"boundries/im15s1match.jpg",cv2.IMREAD_UNCHANGED)
cv2.imshow('Template',template)
gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
h,w = template.shape[0], template.shape[1]

matched = cv2.matchTemplate(img,template, cv2.TM_CCOEFF_NORMED)
threshold = .8

(y_points, x_points) = np.where( matched >= threshold)

for pt in zip( x_points,y_points):
   cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,255,255), 5)
result =cv2.resize(img,(700,700))
cv2.imshow('Matched with Template',result)
cv2.waitKey(0)
cv2.destroyAllWindows()