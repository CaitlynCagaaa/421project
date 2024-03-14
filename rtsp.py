import cv2 
import numpy as np
import math
import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
vid = cv2.VideoCapture(r'rtsp://admin:NullTerminat0r2%24@192.168.0.17/onvif1' ) 
vid.set(cv2.CAP_PROP_FPS, 10)
frame_width = int(vid.get(3)) 
frame_height = int(vid.get(4)) 
x,y,w,h = 1920-1134,1080-730,1134,730
size = (frame_width, frame_height) 

result = cv2.VideoWriter(r'testrtp10.avi',  
                         cv2.VideoWriter_fourcc(*'XVID'), 
                         15, size) 
i =0
while(True): 
      
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 
    if ret == False:
        continue
    #frame = frame[y:y+h, x:x+w]
    # Display the resulting frame 
    cv2.imshow('frame', frame) 
    #print(ret)
    #cv2.imshow('im1',img)
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    
    #cv2.imshow('Template',template)
    #gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    
    
    

          

        
        
    
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    result.write(frame)
   # print(i)
   # i+=1
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# After the loop release the cap object 
vid.release() 

# Destroy all the windows 
cv2.destroyAllWindows() 
