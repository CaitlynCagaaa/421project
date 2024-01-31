

# import the opencv library 
import cv2 
import numpy as np

def drawtemp(template, frame, w, h, color1):
    matched = cv2.matchTemplate(frame,template, cv2.TM_CCOEFF_NORMED)
    threshold = .8

    least_value, peak_value, least_coord, peak_coord = cv2.minMaxLoc(matched)
    print(peak_value)
    if peak_value >= threshold:
     

     highlight_start = peak_coord
    
     highlight_end = (highlight_start[0] + w, highlight_start[1] + h)
   
     cv2.rectangle(frame, highlight_start, highlight_end, color1, 1 )

  
template1 = cv2.imread('testvideo1template1.jpg',cv2.IMREAD_UNCHANGED)
h,w = template1.shape[0], template1.shape[1]
template2= cv2.imread('testvideo1template2.jpg',cv2.IMREAD_UNCHANGED)
h2,w2 = template2.shape[0], template2.shape[1]
template3= cv2.imread('testvideo1template3.jpg',cv2.IMREAD_UNCHANGED)
h3,w3 = template3.shape[0], template3.shape[1]
# define a video capture object 
vid = cv2.VideoCapture('testvideo1.mp4') 
frame_width = int(vid.get(3)) 
frame_height = int(vid.get(4)) 
   
size = (frame_width, frame_height) 
result = cv2.VideoWriter('resulttestvideo1.avi',  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         10, size) 
  
while(True): 
      
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 
  
    # Display the resulting frame 
    cv2.imshow('frame', frame) 
   
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
