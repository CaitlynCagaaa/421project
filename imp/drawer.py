import cv2 
import numpy as np
from matplotlib import pyplot as plt
import datetime;
import math
import json

def find_drawer(frame, drawers, record):
   #print("Enter find")
   modFrame=frame.copy()
   #print(drawers)
   for drawer in drawers:
     #print("drawer")
     found, template, place = is_open(frame,modFrame, drawer["drawersymbols"],record)
     if found:
        drawSize = drawer_location(modFrame, place, drawer, template,record)
        return modFrame, drawer, drawSize
      
   return modFrame, None, None

def drawer_location(modFrame, place, drawer, template, record):
  xDiff = template["X"]-place[0][0]
  yDiff = template["Y"]-place[0][1]
  wDiff = drawer["W"]-xDiff
  hDiff = drawer["H"]-yDiff 
  #print(xDiff, yDiff)
  drawSize = (drawer["X"],drawer["Y"], wDiff,hDiff)
  print(drawSize)
  if record ==1:
    cv2.rectangle(modFrame, (drawer["X"],drawer["Y"]), (drawSize[2]+drawer["X"], drawSize[3]+drawer["Y"]), (256,256,256), 1 )
  return drawSize


def is_open(frame,modFrame, templates,record):
  i = 0
  color = [(256,0,0), (0,256,0), (0,0,256)]
  placeMax =None
  similarityMax = 0
  foundTemplate =None
  foundMax =False
  for template in templates:
     pic = cv2.imread(template["picall"])
     frame_width = pic.shape[1]
     frame_height = pic.shape[0]
     found,place,similarity = draw_temp(pic,frame, modFrame, frame_width, frame_height,color[i], .8,record,1,10)
     if found == True and similarity>similarityMax:
       placeMax = place
       similarityMax = similarity
       foundTemplate =template
       foundMax=found
     
  return foundMax, foundTemplate, placeMax


def rotated_rect_with_max_area(w, h, angle):
 # """https://stackoverflow.com/questions/16702966/rotate-image-and-crop-out-black-borders
  #Given a rectangle of size wxh that has been rotated by 'angle' (in
  #radians), computes the width and height of the largest possible
  #axis-aligned rectangle (maximal area) within the rotated rectangle.
  #"""
  if w <= 0 or h <= 0:
    return 0,0

  width_is_longer = w >= h
  side_long, side_short = (w,h) if width_is_longer else (h,w)

  # since the solutions for angle, -angle and 180-angle are all the same,
  # if suffices to look at the first quadrant and the absolute values of sin,cos:
  sin_a, cos_a = abs(math.sin(angle)), abs(math.cos(angle))
  if side_short <= 2.*sin_a*cos_a*side_long or abs(sin_a-cos_a) < 1e-10:
    # half constrained case: two crop corners touch the longer side,
    #   the other two corners are on the mid-line parallel to the longer line
    x = 0.5*side_short
    wr,hr = (x/sin_a,x/cos_a) if width_is_longer else (x/cos_a,x/sin_a)
  else:
    # fully constrained case: crop touches all 4 sides
    cos_2a = cos_a*cos_a - sin_a*sin_a
    wr,hr = (w*cos_a - h*sin_a)/cos_2a, (h*cos_a - w*sin_a)/cos_2a

  return wr,hr
def rotate_max_area(image, angle):
    """ image: cv2 image matrix object
        angle: in degree
        https://stackoverflow.com/questions/16702966/rotate-image-and-crop-out-black-borders
    """
    wr, hr = rotated_rect_with_max_area(image.shape[1], image.shape[0],
                                    math.radians(angle))
    rotated = rotate_bound(image, angle)
    h, w, _ = rotated.shape
    y1 = h//2 - int(hr/2)
    y2 = y1 + int(hr)
    x1 = w//2 - int(wr/2)
    x2 = x1 + int(wr)
    rotatedObject=rotated[y1:y2, x1:x2]
    return rotatedObject

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


def draw_temp(template, frame,modFrame, w, h, color1, threshold, draw,degrees,degreeDiv):
    found = False
    place =None
    similarity =None
    temp = template
    x =0
    while x <=degrees*degreeDiv:
     template =temp
   #  print(str(x) + " 1")
     template = rotate_max_area(template, x/degreeDiv)
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
        cv2.rectangle(modFrame, highlight_start, highlight_end, color1, 1 )
      
      break
     
     x=-(x)
     if 0>=x:
        x= x-1
    template =temp
     
     
    
   # print(str(x) + "angle")
    return found, place, similarity
    

  
  
