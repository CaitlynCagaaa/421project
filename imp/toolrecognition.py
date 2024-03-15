import cv2 
import numpy as np
from matplotlib import pyplot as plt
import datetime;
import math
import json

def update_tools_for_frames(frame, modframe, tools, errors, drawerLocation,timestamp,drawer,configuration,classifier):
    global con 
    con = configuration
    drawer_segment(frame, drawerLocation)
    for tool in tools:
        is_visible()
        remove_from_contours()
        status = is_checked_out()
        if (tool['checkedOut'] == True and status == 1) or  (tool['checkedOut'] == False and status == 0):
            tool['checkedOut'] = not tool['checkedOut']
    check_extra_tools()
    updatedTools = tools
    updatedErrors =errors
    return updatedTools, updatedErrors

def drawer_segment(frame, drawerLocation):
    crop = frame[drawerLocation[1]:drawerLocation[3], drawerLocation[0]:drawerLocation[2]].copy()
    gray = cv2.cvtColor(crop,con.get('grayscale'))
    gray=cv2.medianBlur(crop,con.get('blur'))
    cv2.imshow("blurring", gray)
    ret, thresh = cv2.threshold(gray,con.get('minThreshValue'),255,con.get('threshType') )
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = con.get("increasewhite"))
    sure_bg = cv2.dilate(opening,kernel,iterations=con.get("decreaseblack"))
    contours, hierarchy= cv2.findContours(sure_bg, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)
    return contours
def is_visible(tool,drawerLocation,drawer,buffer):
    toolLocation =calculate_location(tool,drawer,drawerLocation)
    if toolLocation[3]*toolLocation[2]>=tool['W']*tool['H']*buffer:
        visible = True
    else:
        visible =False
    return toolLocation, visible
def calculate_location(tool,drawer,drawerLocation):
    # i can't think it through right now 
    xDiff = drawer["W"]-drawerLocation[2]
    yDiff = drawer["H"]-drawerLocation[3]
#print(xDiff, yDiff)
    if tool['X']<=drawer['X']-xDiff:
        toolSize = (drawer["X"]+ciel(con['bufferX']/2),tool["Y"]+ciel(con['bufferY']/2), tool["W"] - xDiff+con['bufferX'],tool["H"] -yDiff+con['bufferY'])
    else:
         toolSize = (tool["X"]-xDiff,tool["Y"]-yDiff, tool["W"],tool["H"])
    return toolSize
def remove_from_contours(contours, toolLocation):
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if toolLocation[0] > x > toolLocation[0] + toolLocation[2] and toolLocation[0] > y > toolLocation[0] + toolLocation[3] or cv2.pointPolygonTest(contour, (toolLocation[0],toolLocation[1]), False)== 1 or cv2.pointPolygonTest(contour, (toolLocation[0],toolLocation[1]), False)== 0:
            contours.remove(contour) 

    return contours
def check_extra_tools(contours, errors, timeStamp, drawer,drawerLocation,frame,modFrame, record) :
    updatedErrors = {"errors":[]}
    for contour in contours:
        toolType = classifier_check() 
        x,y,w,h = cv2.boundingRect(contour)
        if toolType in gcon['onnxtools']:
            if record:
                modFrame = cv2.rectangle(modFrame, (x, y), (x + w, y+h), (255, 0,0), 3)
            for error in errors:
                if error['X'] > x > error['X']  + error['W'] and error['Y']  > y > error['Y'] + error['H'] or cv2.pointPolygonTest(contour, (error['X'],error['Y']), False)== 1 or cv2.pointPolygonTest(contour, (error['X']+error['W'],error['H']+error['Y']), False)== 1:
                    updatedErrors["errors"].append(error)
                    errors['error'].remove(error)
                else:
                  updatedErrors["errors"].append({"ID": 0, "EventType": 2, "ToolID": None, "UserID": 1, "Timestamp":timeStamp ,"Location": drawer["ID"], "X": x, "Y": y, "W": w, "H": h})  
    for error in errors:
       location, visible = is_visible()
       if not visible:
            updatedErrors["errors"].append(error)

    return updatedErrors
def is_checked_out(image, modFrame, tool, threshold, degrees, degreesDiv, errors, timeStamp,drawerID,record):
    return
def classifier_check(classifier, image):
    return
def symbol_check(tool, image, modFrame, threshold, degrres, degreesDiv, record):
    return        
    

                


    


    
           
          
        
        

