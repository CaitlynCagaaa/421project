import cv2
import numpy as np

img = cv2.imread(r"match.jpg",cv2.IMREAD_UNCHANGED)
cv2.imshow('im1',img)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

template = cv2.imread(r"plier.jpg",cv2.IMREAD_UNCHANGED)
cv2.imshow('Template',template)
gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
h,w = template.shape[0], template.shape[1]

matched = cv2.matchTemplate(img,template, cv2.TM_CCOEFF_NORMED)
threshold = .8
least_value, peak_value, least_coord, peak_coord = cv2.minMaxLoc(matched)


if(peak_value >=threshold):
    highlight_start = peak_coord
    
    highlight_end = (highlight_start[0] + w, highlight_start[1] + h)
   
    cv2.rectangle(img, highlight_start, highlight_end, (0,255,255), 5 )
   
result =cv2.resize(img,(700,700))
cv2.imshow('Matched with Template',result)
cv2.imwrite('match.jpg',img)
cv2.waitKey(0)
cv2.destroyAllWindows()