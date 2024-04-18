import cv2 
import numpy as np
from matplotlib import pyplot as plt
import math
import json
import yaml
import imutils

gcon =open("Global_Config.yaml", "r")
gcon =yaml.safe_load(gcon)

def find_drawer(frame, drawers, record):
   #print("Enter find")
   modFrame=frame.copy()
   #print(drawers)
   for drawer in drawers:
     #print("drawer")
     found, template, place, similairty = is_open(frame,modFrame, drawer["DrawerSymbols"],record)
     if found:
        drawLocation = drawer_location(modFrame, place,similairty, drawer, template,record)
        return modFrame, drawer, drawLocation
   #print("drawer done")
   return modFrame, None, None

def drawer_location(modFrame, place, similarirty, drawer, template, record):
  xDiff = template["X"]-place[0][0]
  yDiff = template["Y"]-place[0][1]
  wDiff = drawer["DrawerPixelWidth"]-xDiff
  hDiff = drawer["DrawerPixelHeight"]-yDiff 
  #print(xDiff, yDiff)
  
  drawLocation = (drawer["DrawerStartX"],drawer["DrawerStartY"], wDiff,hDiff)
  #print(drawSize)
  if record ==1:
    (wt, ht), _ = cv2.getTextSize(
          'drawer '+ str(drawer["DrawerID"]) +" "+ str(round(similarirty,2))+'%', cv2.FONT_HERSHEY_SIMPLEX, .002*drawLocation[3], 5)
    modFrame = cv2.rectangle(modFrame, (drawLocation[0], drawLocation[1] - ht), (drawLocation[0] + wt, drawLocation[1]), (255, 0,0), 3)
    cv2.putText(modFrame, 'drawer '+ str(drawer["DrawerID"]) +" "+ str(round(similarirty,2))+'%', (drawLocation[0], drawLocation[1]),cv2.FONT_HERSHEY_SIMPLEX,.002*drawLocation[3], (36,255,12), 1)
    cv2.rectangle(modFrame, (drawLocation[0],drawLocation[1]), (drawLocation[2]+drawLocation[0], drawLocation[3]+drawLocation[1]), (256,256,256), 3)
    cv2.imwrite("drawer.jpg",modFrame)
    #cv2.waitKey(0)
  return drawLocation


def is_open(frame,modFrame, templates,record):
  
  placeMax =None
  similarityMax = 0
  foundTemplate =None
  foundMax =False
  templates= json.loads(templates)
  print(templates)
  for template in templates:
     #print(template, "check")
     
     pic = imutils.url_to_image(gcon.get("webserverurl")+template["picall"])
     frame_width = pic.shape[1]
     frame_height = pic.shape[0]
     
     #image = frame[template["Y"]-gcon.get("buffery"):template["H"]+template["Y"]+2*gcon.get("buffery"), 0:frame.shape[1]]
     #cv2.imshow("image",image)
     #cv2.waitKey(0)
     found,place,similarity = draw_temp(pic,frame, modFrame, frame_width, frame_height,(256,0,0), gcon.get("thresholdsymbol"),record,gcon.get("degrees"),gcon.get("degreesdiv"))
     if found == True and similarity>similarityMax and template["Y"] -place[0][1] < gcon.get("buffery")*gcon.get("multfordrawersymbolbuffer"):
       placeMax = place
       similarityMax = similarity
       foundTemplate =template
       foundMax=found
     if record ==1 and found ==True :
        text = str(template["ID"]) + " "+ str(similarity) +" "+ str(template["Y"] -place[0][1])
        (wt, ht), _ = cv2.getTextSize(
         text, cv2.FONT_HERSHEY_SIMPLEX, .005*(place[1][0]-place[0][0]), 2)
        modFrame = cv2.rectangle(modFrame, (place[0][0], place[0][1] - ht), (place[0][0] + wt, place[0][1]), (255, 0,0), 3)
        cv2.putText(modFrame, text, (place[0][0], place[0][1]),cv2.FONT_HERSHEY_SIMPLEX,.005*(place[1][0]-place[0][0]), (36,255,12), 1)
  #print("donetemplates")
  return foundMax, foundTemplate, placeMax, similarityMax


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
    similarity =0
    temp = template
    x =0
    while x <=degrees*degreeDiv:
     template =temp
   #  print(str(x) + " 1")
     if x!=0:
        template = rotate_max_area(template, x/degreeDiv)
     #cv2.imshow("temp", template)
     
     if template.shape[0] >= frame.shape[0]:
        template[0:frame.shape[0]-1, 0:template.shape[1]]
     if template.shape[1] >= frame.shape[1]:
        template[0:template.shape[0], 0:frame.shape[1]-1]
     try:
      matched = cv2.matchTemplate(frame,template, cv2.TM_CCOEFF_NORMED)
     except cv2.error:
        x=-(x)
        if 0>=x:
          x= x-1
        template =temp
        continue
     least_value, peak_value, least_coord, peak_coord = cv2.minMaxLoc(matched)
    #print(peak_value)
     if peak_value>similarity:
        similarity = peak_value
        if peak_value >= threshold:
          found = True
          highlight_start = peak_coord
          highlight_end = (highlight_start[0] + w, highlight_start[1] + h)
          place =(highlight_start,highlight_end)
      
     x=-(x)
     if 0>=x:
        x= x-1
    template =temp
     
     
    if found ==True and draw ==1:
      cv2.rectangle(modFrame, highlight_start, highlight_end, color1, 2 )
   # print(str(x) + "angle")
    return found, place, similarity
    

  
  
