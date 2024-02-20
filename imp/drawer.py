import cv2 
import numpy as np
import datetime;
import math
import json

def find_drawer(frame, drawers, events, tools, UserID, timestampFrame):
   for drawer in drawers:
     found, id, place, similarity= is_open(frame, drawer["drawersymbols"],3)
     if is_open(frame, drawer["drawersymbols"],3):
        events["events"].append({"ID": 0, "EventTyp": 0, "ToolID": None, "UserID": UserID, "Timestamp":timestampFrame ,"Location": drawer["ID"]})
        return drawer
      
   return None

def is_open(frame, templates,numboftemplates):
  i = 0
  max =0
  color = (0,0,0)
  placeMax =None
  similarityMax = 0
  for template in templates:
     pic = cv2.imread(template["picall"])
     frame_width = int(frame.get(3)) 
     frame_height = int(frame.get(4))  
     color[i] =256
     found,place,similarity = drawtemp(pic, frame, frame_width, frame_height,color, .8,1,1,10)
     if found == True and similarity>similarityMax:
       max =i
       placeMac = place
       similarityMax = similarity
     i=i+1
     
  return found, max, placeMax, similarityMax


def rotate_bound(image, angle):
    # CREDIT: https://www.pyimagesearch.com/2017/01/02/rotate-images-correctly-with-opencv-and-python/
    # https://stackoverflow.com/questions/16702966/rotate-image-and-crop-out-black-borders
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    return cv2.warpAffine(image, M, (nW, nH))


def drawtemp(template, frame, w, h, color1, threshold, draw,degrees,degreeDiv):
    found = False
    place =None
    similarity =None
    temp = template
    x =0
    while x <=degrees*degreeDiv:
     template =temp
     print(str(x) + " 1")
     template = rotate_bound(template, x/degreeDiv)
     #cv2.imshow("temp", template)
     matched = cv2.matchTemplate(frame,template, cv2.TM_CCOEFF_NORMED)
     

     least_value, peak_value, least_coord, peak_coord = cv2.minMaxLoc(matched)
    #print(peak_value)
     if peak_value >= threshold:
      found = True
      highlight_start = peak_coord
      similarity = peak_value
      highlight_end = (highlight_start[0] + w, highlight_start[1] + h)
      place =(highlight_start,highlight_end)
      if(draw ==1):
        cv2.rectangle(frame, highlight_start, highlight_end, color1, 1 )
      
      break
     
     x=-(x)
     if 0>=x:
        x= x-1
    template =temp
     
     
    
    print(str(x) + "angle")
    return found, place, peak_value
    

  
  
template1 = cv2.imread('plier.jpg',cv2.IMREAD_UNCHANGED)
h,w = template1.shape[0], template1.shape[1]
template2= cv2.imread('hammer.jpg',cv2.IMREAD_UNCHANGED)
h2,w2 = template2.shape[0], template2.shape[1]
template3= cv2.imread('mallet.jpg',cv2.IMREAD_UNCHANGED)
h3,w3 = template3.shape[0], template3.shape[1]
template4= cv2.imread('hammer_full.jpg',cv2.IMREAD_UNCHANGED)
h4,w4 = template4.shape[0], template4.shape[1]
template5= cv2.imread('plier_red.jpg',cv2.IMREAD_UNCHANGED)
h5,w5 = template5.shape[0], template5.shape[1]
# define a video capture object 
vid = cv2.VideoCapture('shapematching.avi') 
frame_width = int(vid.get(3)) 
frame_height = int(vid.get(4)) 
   
size = (frame_width, frame_height) 
result = cv2.VideoWriter('matchvideostrict.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         12, size) 
cv2.imwrite("b.jpg", template5)
template5 = rotate_bound(template5, .1)
cv2.imwrite("t.jpg", template5)
while(True): 
      
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 
  
    # Display the resulting frame 
    #cv2.imshow('frame', frame) 
    #print(ret)
    #cv2.imshow('im1',img)
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    
    #cv2.imshow('Template',template)
    #gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    color = (255, 0, 0)
    drawtemp(template1, frame, w, h, color)
    color = (0, 255, 0) 
    drawtemp(template2, frame, w2, h2, color)
    color = (0, 0, 255) 
    drawtemp(template3, frame, w3, h3,color)
    color = (255, 0, 255) 
    drawtemp(template4, frame, w4, h4,color)
    color = (0, 255, 255) 
    drawtemp(template5, frame, w5, h5,color)

    

    

          

        
        
      
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    result.write(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 