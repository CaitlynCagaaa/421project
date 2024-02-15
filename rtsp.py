import cv2 
import numpy as np
import math
vid = cv2.VideoCapture('shapesmatching.ts') 
frame_width = int(vid.get(3)) 
frame_height = int(vid.get(4)) 
size = (frame_width, frame_height) 
result = cv2.VideoWriter('shapematching.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         12, size) 
i =0
while(True): 
      
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 
    if ret == False:
        continue

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
    print(i)
    i+=1
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# After the loop release the cap object 
vid.release() 

# Destroy all the windows 
cv2.destroyAllWindows() 
