import json
import yaml
import cv2
import numpy as np
from matplotlib import pyplot as plt
config =open("conf.yaml", "r") 
file = "boundries/im6"
con =yaml.safe_load(config)
print(config)
# optimized using im14
# Load the image
image = cv2.imread(r""+file +".jpg",cv2.IMREAD_UNCHANGED)
print(con)
# Display the image
#normalized_image = cv2.normalize(image, None, 0, 1, cv2.NORM_MINMAX)
#cv2.imshow("norm", normalized_image)
gray = cv2.cvtColor(image,con.get('grayscale'))
gray=cv2.medianBlur(gray,con.get('blur'))
cv2.imshow("Im", gray)
#normalized_image = cv2.normalize(image, None, 0, 1, cv2.NORM_MINMAX)
#cv2.imshow("norm", normalized_image)
ret, thresh = cv2.threshold(gray,con.get('minThreshValue'),255,con.get('threshType') )
#thresh = cv2.bitwise_not(thresh) 
cv2.imshow("Ima", thresh)
result = image.copy()
kernel = np.ones((3,3),np.uint8)
#cv2.imshow("kernel", kernel)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = con.get("dilateObject"))
cv2.imshow("open", opening)
# sure background area

sure_bg = cv2.dilate(opening,kernel,iterations=2)
cv2.imshow("Imag", sure_bg)
# Finding sure foreground area
#dist_transform = cv2.distanceTransform(thresh,cv2.DIST_L1,0)
#cv2.imshow("I", dist_transform)
contours, hierarchy= cv2.findContours(sure_bg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#print(contours)
#print(hierarchy)
res_cpy = result.copy()
cv2.drawContours(image=res_cpy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=5, lineType=cv2.LINE_AA)
print(hierarchy)
cv2.imshow("contour", image)
cv2.imwrite(file+'/imgbound.jpg',res_cpy)
#contours = contours[0] if len(contours) == 2 else contours[1]
check = 1
with open('data.json', 'w') as f:
 f.write('{"Tools": [')
 for i in range(len(contours)):
    #print(i)
    #print(hierarchy[0,i,3])
    if hierarchy[0,i,3] ==0 and check == 1:
         check = 0
         print("1")
         with open('drawer.json', 'w') as d:
          x,y,w,h = cv2.boundingRect(contours[i])
          if w > con.get('minWidth') and h >con.get('minHeight'):
            cv2.rectangle(result, (x, y), (x+w, y+h), (255, 0, 0), 1)
            (wt, ht), _ = cv2.getTextSize(
        'drawer ' + str(0)+'%', cv2.FONT_HERSHEY_SIMPLEX, .003*w, 1)

# Prints the text.    
            img = cv2.rectangle(result, (x, y - ht), (x + wt, y), (255, 0,0), -1)
            cv2.putText(result, 'drawer ' + str(0)+'%', (x, y),cv2.FONT_HERSHEY_SIMPLEX,.003*w, (36,255,12), 1)
            temp= 'drawer ' +str(x) +str(y) +str(w) +str(h) +".jpg"
    #print("x,y,w,h:",x,y,w,h)
            if w>con.get('minWidth') and h>con.get('minHeight'):
        #print(image.shape) 
                cropped_image = image[y:y+h, x:x+w].copy()
               
                dump = {'ID': i, 'DrawerNum': 0 , 'BoxNum': 0,'X': x, 'Y' :y ,'W' :w , 'H' : h, 'picall':file+'/img' + temp, 'picno':file+'/img' + temp, 'locations':[{'ID': 1,'X': 0, 'Y' :0 ,'W' :0 , 'H' : 0, 'picall': 'none' }, {'ID': 1,'X': 0, 'Y' :0 ,'W' :0 , 'H' : 0, 'picall': 'none' },{'ID': 1,'X': 0, 'Y' :0 ,'W' :0 , 'H' : 0, 'picall': 'none' }] }
                json.dump(dump,d)
                
        #print(cropped_image)
                cv2.imshow( "cropped",cropped_image )
                cv2.imwrite(file+'/img' +temp,cropped_image)
            
    else:
        print("2")
        x,y,w,h = cv2.boundingRect(contours[i])
        if w > con.get('minWidth') and h >con.get('minHeight'):
            cv2.rectangle(result, (x, y), (x+w, y+h), (0, 0, 255), 1)
            (wt, ht), _ = cv2.getTextSize(
        'toolname ' + str(0)+'%', cv2.FONT_HERSHEY_SIMPLEX, .003*w, 1)

# Prints the text.    
            img = cv2.rectangle(result, (x, y - ht), (x + wt, y), (0, 0, 255), -1)
            cv2.putText(result, 'toolname ' + str(0)+'%', (x, y),cv2.FONT_HERSHEY_SIMPLEX,.003*w, (36,255,12), 1)
            temp= str(x) +str(y) +str(w) +str(h) +".jpg"
    #print("x,y,w,h:",x,y,w,h)
            if w>con.get('minWidth') and h>con.get('minHeight'):
        #print(image.shape) 
                cropped_image = image[y:y+h, x:x+w].copy()
               
                dump = {'ID': i, 'Name': 'img' + str(i), 'Location': 0, 'CheckedOut': False,'X': x, 'Y' :y ,'W' :w , 'H' : h, 'pic': file+'/img' +temp}
                json.dump(dump,f)
                f.write(',\n')
        #print(cropped_image)
                cv2.imshow( "cropped",cropped_image )
                cv2.imwrite(file+'/img' +temp,cropped_image)
 f.write("]}")
    #i=i+1

cv2.imwrite(file+'/imgbounded.jpg',result)
#result =cv2.resize(result,None,.75,.75)
cv2.imshow("bounding boxes", result)
# noise removal

#ret, sure_fg = cv2.threshold(dist_transform,0.10*dist_transform.max(),255,50)
# Finding unknown region
#sure_fg = np.uint8(sure_fg)
#cv2.imshow("Imagee", sure_fg)
#unknown = cv2.subtract(sure_bg,sure_fg)

# Marker labelling
#ret, markers = cv2.connectedComponents(sure_fg)

# Add one to all labels so that sure background is not 0, but 1
#markers = markers+1
# Now, mark the region of unknown with zero
#markers[unknown==255] = 0
#markers = cv2.watershed(image,markers)

#image[markers == -1] = [255,0,0]
cv2.imshow("Image", image)
# Wait for the user to press a key
cv2.waitKey(0)
cv2.destroyAllWindows()