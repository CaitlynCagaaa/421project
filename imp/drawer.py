import cv2 
import numpy as np
from matplotlib import pyplot as plt
import datetime;
import math
import json

def find_drawer(frame, drawers, events, tools, UserID, timestampFrame,record):
   print("Enter find")
   print(drawers)
   for drawer in drawers:
     print("drawer")
     found, template, place = is_open(frame, drawer["drawersymbols"],record)
     if found:
        events["events"].append({"ID": 0, "EventType": 0, "ToolID": None, "UserID": UserID, "Timestamp":timestampFrame ,"Location": drawer["ID"]})
        drawSize = drawer_location(frame, place, drawer, template,record)
        return drawer, drawSize
      
   return None, None

def drawer_location(frame, place, drawer, template, record):
  xDiff = template["X"]-place[0][0]
  yDiff = template["Y"]-place[0][1]
  drawSize = (drawer["W"] +xDiff,drawer["H"] +yDiff)
  if record ==1:
    cv2.rectangle(frame, (drawer["X"],drawer["Y"]), drawSize, (256,256,256), 1 )
  return drawSize
def is_open(frame, templates,record):
  i = 0
  color = [(256,0,0), (0,256,0), (0,0,256)]
  placeMax =None
  similarityMax = 0
  foundTemplate =None
  for template in templates:
     pic = cv2.imread(template["picall"])
     frame_width = pic.shape[1]
     frame_height = pic.shape[0]
     found,place,similarity = drawtemp(pic, frame, frame_width, frame_height,color[i], .8,record,1,10)
     if found == True and similarity>similarityMax:
       max =i
       placeMax = place
       similarityMax = similarity
       foundTemplate =template
     i=i+1
     
  return found, foundTemplate, placeMax


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
    

  
  
