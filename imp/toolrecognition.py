import cv2 
import numpy as np
from matplotlib import pyplot as plt
import datetime;
import math
import json
import drawer
import yaml
from shapely.geometry import Polygon
gcon =open("g_conf.yaml", "r")
gcon =yaml.safe_load(gcon)

def update_tools_for_frames(frame, modframe, tools, errors, drawerLocation,timestamp,drawer,configuration,classifier, record):
    global con 
    global onnx
    onnx = classifier

    con = configuration
    countours =drawer_segment(frame, drawerLocation)
    for tool in tools["Tools"]:
        toolLocation, visible= is_visible(tool,drawerLocation,drawer,record)
        if visible:
            countours =remove_from_contours(countours, toolLocation,drawerLocation)
            crop = frame[toolLocation[1]:toolLocation[3]+toolLocation[1], toolLocation[0]:toolLocation[2]+toolLocation[0]].copy()
            status = is_checked_out(crop,modframe,tool,toolLocation,gcon.get("thresholdtool"),gcon.get("degrees"),gcon.get("degreesdiv"),errors,timestamp,drawer["ID"],record)
            if (tool['CheckedOut'] == True and status == 1) or  (tool['CheckedOut'] == False and status == 0):
                tool['CheckedOut'] = not tool['CheckedOut']
    updatedErrors = check_extra_tools(countours, errors, timestamp, drawer,drawerLocation,frame,modframe, onnx, record)
    updatedTools = tools
   
    return updatedTools, updatedErrors

def drawer_segment(frame, drawerLocation):
    crop = frame[drawerLocation[1]:drawerLocation[3]+drawerLocation[1], drawerLocation[0]:drawerLocation[2]+drawerLocation[0]].copy()
    gray = cv2.cvtColor(crop,con.get('grayscale'))
    gray=cv2.medianBlur(gray,con.get('blur'))
    cv2.imshow("blurring", gray)
    ret, thresh = cv2.threshold(gray,con.get('minThreshValue'),255,con.get('threshType') )
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = con.get("increasewhite"))
    sure_bg = cv2.dilate(opening,kernel,iterations=con.get("decreaseblack"))
    contours, hierarchy= cv2.findContours(sure_bg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours
def is_visible(tool,drawerLocation,drawer,buffer):
    toolLocation =calculate_location(tool,drawer,drawerLocation)
    if toolLocation[3]*toolLocation[2]>=tool["W"]*tool["H"]*buffer:
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
        toolSize = (drawerLocation[0],tool["Y"], tool["W"] - xDiff+con['bufferX'],tool["H"] -yDiff+con['bufferY'])
    else:
         toolSize = (tool["X"],tool["Y"], tool["W"]+con['bufferX'],tool["H"]+con['bufferY'])
    print(toolSize)
    return toolSize
def remove_from_contours(contours, toolLocation,drawerLocation):
    tool  = Polygon([(toolLocation[0] -10,toolLocation[1]-10), (toolLocation[0] -10,toolLocation[1]+toolLocation[3]+10),(toolLocation[0]+toolLocation[2]+10,toolLocation[3]+10), (toolLocation[0]+toolLocation[2]+10,toolLocation[1]+toolLocation[1]-10)])
    print(tool.area)
    contourss =[]
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        cont  = Polygon([(x+drawerLocation[0],y+drawerLocation[1]), (x+drawerLocation[0],y+h+drawerLocation[1]),(x+w+drawerLocation[0],y+h+drawerLocation[1]), (x+w+drawerLocation[0],y+drawerLocation[1])])
        print(cont.area)
        if tool.buffer(1).intersects(cont) or tool.buffer(1).contains(cont) or cont.buffer(1).contains(tool):
        #if toolLocation[0]-10 < x+drawerLocation[0] > toolLocation[0] + toolLocation[2]+10 and toolLocation[1]-10 < y+drawerLocation[1] > toolLocation[1] + toolLocation[3]+10 or cv2.pointPolygonTest(contour, (drawerLocation[0]-toolLocation[0],drawerLocation[1]-toolLocation[1]), False)== 1 or cv2.pointPolygonTest(contour, (drawerLocation[0] - toolLocation[0],drawerLocation[1] -toolLocation[1]), False)== 0:
            continue
        contourss.append(contour) 
    return contourss
def check_extra_tools(contours, errors, timeStamp, drawer,drawerLocation,frame,modFrame, classifier, record) :
    updatedErrors = {"errors":[]}
    crop = frame[drawerLocation[1]:drawerLocation[3]+drawerLocation[1], drawerLocation[0]:drawerLocation[2]+drawerLocation[0]].copy()
    image =cv2.drawContours(image=crop, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=5, lineType=cv2.LINE_AA)
    cv2.imwrite("contours.jpg", image)
    cv2.waitKey(0)
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if w > con.get("minWidth") and h > con.get("minHeight"):
            image = crop[y:y+h,x:x+w,].copy()
            cv2.imshow("ch",image)
            cv2.waitKey(0)
            toolType = classifier_check(classifier, image) 
            if toolType in gcon['onnxtools']:
                if record:
                    modFrame = cv2.rectangle(modFrame, (x, y), (x + w, y+h), (255, 0,0), 3)
                for error in errors["errors"]:
                    if (error["X"] > x+drawerLocation[0] > error['X']  + error['W'] and error['Y']  > y+drawerLocation[1] > error['Y'] + error['H'] or 
                    cv2.pointPolygonTest(contour, (error['X'],error['Y']), False)== 1 or cv2.pointPolygonTest(contour, (error['X']+error['W'],error['H']+error['Y']), False)== 1):
                        updatedErrors["errors"].append(error)
                        errors['errors'].remove(error)
                    else:
                        updatedErrors["errors"].append({"ID": 0, "ToolType": toolType,"EventType": 2, "ToolID": None, "UserID": 1, "Timestamp":timeStamp ,"Location": drawer["ID"], "X": x, "Y": y, "W": w, "H": h})  
    for error in  errors["errors"]:
       location, visible = is_visible(error,drawerLocation,drawer, gcon.get("buffer"))
       if not visible:
            updatedErrors["errors"].append(error)

    return updatedErrors
def is_checked_out(image, modFrame, tool, toolLocation, threshold, degrees, degreesDiv, errors, timeStamp,drawerID,record):
    picno = cv2.imread(tool["picnull"])
    foundNoTool,placeNoTool,similarityNoTool = drawer.draw_temp(picno,image, modFrame, image.shape[0], image.shape[1],(256,0,256), .8,0,1,5)
    if foundNoTool ==False:
        similarityNoTool =0
    picfull = cv2.imread(tool["picfull"])
    foundTool,placeTool,similarityTool = drawer.draw_temp(picfull,image, modFrame, image.shape[0], image.shape[1],(0,256,256), .8,0,1,5)
    cv2.imshow("check",modFrame)
    cv2.waitKey(0)
    if foundTool ==False:
        similarityTool =0   
    if similarityTool >= similarityNoTool:
        toolType = classifier_check(onnx,image)
        if toolType == tool["ClassifierThinks"] and symbol_check(tool,image,modFrame,threshold,degrees,degreesDiv,0):
            checkedOut =1
            color = (256,0,256)
        else:
            errors["errors"].append({"ID": 0, "ToolType": toolType,"EventType": 3, "ToolID": tool["ID"], "UserID": 1, "Timestamp":timeStamp ,"Location": drawerID, "X": placeTool[0][0], "Y": placeTool[0][1], "W": placeTool[1][0], "H": placeTool[1][1]})   
            checkedOut = -1
            color = (0,0,0)
    else:
        checkedOut = 0
        color =(0,256,256)
    if record ==1:
        cv2.rectangle(modFrame, (toolLocation[0],toolLocation[1]), (toolLocation[2]+toolLocation[0],toolLocation[3]+toolLocation[1]), color, 1 )
        
        
    return checkedOut
def classifier_check(classifier, image):
    if classifier ==None:
        return None
    normalized_image = cv2.normalize(image, None, 0, 1, cv2.NORM_MINMAX)
    classifier.setInput(cv2.dnn.blobFromImage(normalized_image, size=(224, 224), swapRB=False, crop=True))
    detection = classifier.forward()
    print(detection)
    answer = np.absolute(detection)
    maximum = np.max(answer)
    answer = np.where(answer == maximum)[0]
    labels= gcon.get("onnxlabels")
    print(labels)
    print(answer)
    index = answer.item()
    return labels[index]
def symbol_check(tool, image, modFrame, threshold, degrees, degreesDiv, record):
    if tool["IDAvail"] ==True:
        found,_,_ = drawer.draw_temp(tool["picall"],image, modFrame, image.shape[0], image.shape[1],(256,256,256), threshold,record,degrees,degreesDiv)  
    else:
        found =True
    return found       
    

                


    


    
           
          
        
        

