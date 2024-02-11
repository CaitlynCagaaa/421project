

# import the opencv library 
import cv2 
import numpy as np
import math

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
def rotate_bound(image, angle):
    # CREDIT: https://www.pyimagesearch.com/2017/01/02/rotate-images-correctly-with-opencv-and-python/
    # https://stackoverflow.com/questions/16702966/rotate-image-and-crop-out-black-borders
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    return cv2.warpAffine(image, M, (nW, nH))


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
    return rotated[y1:y2, x1:x2]

def drawtemp(template, frame, w, h, color1):
    temp = template
    x =0
    while x <=50:
     template =temp
     #print(str(x) + " 1")
     template = rotate_max_area(template, x/10)
     #cv2.imshow("temp", template)
     matched = cv2.matchTemplate(frame,template, cv2.TM_CCOEFF_NORMED)
     threshold = .7

     least_value, peak_value, least_coord, peak_coord = cv2.minMaxLoc(matched)
    #print(peak_value)
     if peak_value >= threshold:
      highlight_start = peak_coord
    
      highlight_end = (highlight_start[0] + w, highlight_start[1] + h)
   
      cv2.rectangle(frame, highlight_start, highlight_end, color1, 1 )
      
      break
     
     x=-(x)
     if 0>=x:
        x= x-1
    template =temp
     
     
    
    print(str(x) + "angle")
    

  

template1 = cv2.imread('testvideo3temp1.jpg',cv2.IMREAD_UNCHANGED)
h,w = template1.shape[0], template1.shape[1]
template2= cv2.imread('testvideo3temp2.jpg',cv2.IMREAD_UNCHANGED)
h2,w2 = template2.shape[0], template2.shape[1]
template3= cv2.imread('testvideo3temp3.jpg',cv2.IMREAD_UNCHANGED)
h3,w3 = template3.shape[0], template3.shape[1]
template4= cv2.imread('testvideo3temp4.jpg',cv2.IMREAD_UNCHANGED)
h4,w4 = template4.shape[0], template4.shape[1]
template5= cv2.imread('testvideo3temp5.jpg',cv2.IMREAD_UNCHANGED)
h5,w5 = template5.shape[0], template5.shape[1]
# define a video capture object 
vid = cv2.VideoCapture('testvideo3p2.mp4') 
frame_width = int(vid.get(3)) 
frame_height = int(vid.get(4)) 
   
size = (frame_width, frame_height) 
result = cv2.VideoWriter('resulttestvideo50p2.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         12, size) 
#template5 = rotate_max_area(template5, 20)
#cv2.imwrite("t.jpg", template5)
i =0
while(True): 
      
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 
    ret, frame = vid.read() 
    ret, frame = vid.read() 
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
    print(i)
    i+=1
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 
