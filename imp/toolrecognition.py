import cv2 
import numpy as np
from matplotlib import pyplot as plt
import datetime;
import math
import json
import drawer
import yaml
from shapely.geometry import Polygon
import copy
gcon =open("g_conf.yaml", "r")
gcon =yaml.safe_load(gcon)

def update_tools_for_frames(frame, modframe, tools, errors, drawerLocation,timestamp,drawer,configuration,classifier, record):
    global con 
    global onnx
    onnx = classifier

    con = configuration
    countours =drawer_segment(frame, drawerLocation)
    updatedTools = copy.deepcopy(tools)
    for tool in updatedTools["Tools"]:
        toolLocation, visible= is_visible(tool,drawerLocation,drawer,gcon.get("buffer"))
        if visible:
            countours =remove_from_contours(countours, toolLocation,drawerLocation)
            crop = frame[toolLocation[1]-gcon.get("buffery"):toolLocation[3]+toolLocation[1]+2*gcon.get("buffery"), toolLocation[0]-gcon.get("bufferx"):toolLocation[2]+2*gcon.get("bufferx")+toolLocation[0]].copy()
            status = is_checked_out(crop,modframe,tool,toolLocation,gcon.get("thresholdtool"),gcon.get("degrees"),gcon.get("degreesdiv"),errors,timestamp,drawer["ID"],record)
            print(errors)
            if (tool['CheckedOut'] == True and status == 1) or  (tool['CheckedOut'] == False and status == 0):
                tool['CheckedOut'] = not tool['CheckedOut']
            elif status == -1:
                tool['error'] = 1
    updatedErrors = check_extra_tools(updatedTools,countours, errors, timestamp, drawer,drawerLocation,frame,modframe, onnx, record)
    
    print(updatedTools)
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
    print(toolLocation[3]*toolLocation[2],tool["W"]*tool["H"]*buffer,buffer)
    if toolLocation[3]*toolLocation[2]>=tool["W"]*tool["H"]*buffer:
        visible = True
    else:
        visible =False
    return toolLocation, visible
def calculate_location(tool,drawer,drawerLocation):
    # i can't think it through right now 
    xDiff = drawer["W"]-drawerLocation[2]
    yDiff = abs(drawer["H"]-drawerLocation[3])
    print(xDiff, yDiff, drawer["X"]+drawerLocation[2],tool['X']+tool["W"])
    diff = tool['X'] - drawerLocation[0]
    if diff<=xDiff:#something is wrong here 
        toolSize = (drawerLocation[0],tool["Y"]-yDiff, tool["W"]-xDiff,tool["H"]+yDiff)
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    else:
         toolSize = (tool["X"]-xDiff,tool["Y"]-yDiff, tool["W"],tool["H"]+yDiff)
         print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
    print(toolSize)
    return toolSize
def remove_from_contours(contours, toolLocation,drawerLocation):
    tool  = Polygon([(toolLocation[0] -10,toolLocation[1]-10), (toolLocation[0] -10,toolLocation[1]+toolLocation[3]+10),(toolLocation[0]+toolLocation[2]+10,toolLocation[3]+10), (toolLocation[0]+toolLocation[2]+10,toolLocation[1]+toolLocation[1]-10)])
    contourss =[]
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        cont  = Polygon([(x+drawerLocation[0],y+drawerLocation[1]), (x+drawerLocation[0],y+h+drawerLocation[1]),(x+w+drawerLocation[0],y+h+drawerLocation[1]), (x+w+drawerLocation[0],y+drawerLocation[1])])
        #print(cont.area)
        if tool.buffer(1).intersects(cont) or tool.buffer(1).contains(cont) or cont.buffer(1).contains(tool):
        #if toolLocation[0]-10 < x+drawerLocation[0] > toolLocation[0] + toolLocation[2]+10 and toolLocation[1]-10 < y+drawerLocation[1] > toolLocation[1] + toolLocation[3]+10 or cv2.pointPolygonTest(contour, (drawerLocation[0]-toolLocation[0],drawerLocation[1]-toolLocation[1]), False)== 1 or cv2.pointPolygonTest(contour, (drawerLocation[0] - toolLocation[0],drawerLocation[1] -toolLocation[1]), False)== 0:
            continue
        contourss.append(contour) 
    return contourss
def check_extra_tools(tools,contours, errors, timeStamp, drawer,drawerLocation,frame,modFrame, classifier, record) :
    updatedErrors = {"errors":[]}
    crop = frame[drawerLocation[1]:drawerLocation[3]+drawerLocation[1], drawerLocation[0]:drawerLocation[2]+drawerLocation[0]].copy()
    image =cv2.drawContours(image=crop, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=5, lineType=cv2.LINE_AA)
    cv2.imwrite("contours.jpg", image)
    
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if w > con.get("minWidth") and h > con.get("minHeight"):
            image = crop[y:y+h,x:x+w,].copy()
            cv2.imshow("ch",image)
            
            toolType = classifier_check(classifier, image) 
            if toolType in gcon['onnxtools']:
                if record:
                    modFrame = cv2.rectangle(modFrame, (x+drawerLocation[0], y+drawerLocation[1] ), (x + w+drawerLocation[0], y+h+drawerLocation[1] ), (255, 0,0), 3)
                for error in errors["errors"]:
                    if (error["X"] > x+drawerLocation[0] > error['X']  + error['W'] and error['Y']  > y+drawerLocation[1] > error['Y'] + error['H'] or 
                    cv2.pointPolygonTest(contour, (error['X'],error['Y']), False)== 1 or cv2.pointPolygonTest(contour, (error['X']+error['W'],error['H']+error['Y']), False)== 1):
                        updatedErrors["errors"].append(error)
                        errors['errors'].remove(error)
                    else:
                        updatedErrors["errors"].append({"ID": 0, "ToolType": toolType,"EventType": 2, "ToolID":None, "UserID": 1, "Timestamp":timeStamp ,"Location": drawer["ID"], "X": x, "Y": y, "W": w, "H": h})  
    for error in  errors["errors"]:
       location, visible = is_visible(error,drawerLocation,drawer, gcon.get("buffer"))
       if not visible :
            updatedErrors["errors"].append(error)
       #elif error["ToolID"]!=None and [tool['error'] for tool in tools['Tools'] if tool['ID']==error["ToolID"]] ==1:
        #    updatedErrors["errors"].append(error)
    #print("error" + str(updatedErrors))
    print(tools)
    return updatedErrors
def is_checked_out(image, modFrame, tool, toolLocation, threshold, degrees, degreesDiv, errors, timeStamp,drawerID,record):
    picno = cv2.imread(tool["picnull"])
    picfull = cv2.imread(tool["picfull"])
    notEntireVisible = False
    if(tool['W']!=toolLocation[2]):
        notEntireVisible = True
        tempY = 0
        tempH = tool["H"]
        tempW = toolLocation[2] - 2*gcon.get("bufferx")
        tempX = tool['X'] - toolLocation[0] +gcon.get("bufferx")
        if  tempX < 0:
            tempX =  toolLocation[0] -tool['X']
        picfull= picfull[tempY:tempY+tempH, tempX:tempX+tempW]
        print(tool["ID"],tempY,tempH,tempW,tempX)
        picno = picno[tempY:tempY+tempH, tempX:tempX+tempW]
        print(picno.shape[0],picno.shape[1],picno.shape[2])
    
    cv2.imshow("wait.jpg",picno)
    cv2.imshow("ck",image)
    #cv2.waitKey(0)
    foundNoTool,placeNoTool,similarityNoTool = drawer.draw_temp(picno,image, modFrame, image.shape[0], image.shape[1],(256,0,256), .8,0,1,5)
    if foundNoTool ==False:
        similarityNoTool =0
    cv2.imshow("wait.jpg",picfull)
    
    #cv2.waitKey(0)
    foundTool,placeTool,similarityTool = drawer.draw_temp(picfull,image, modFrame, image.shape[0], image.shape[1],(0,256,256), .8,0,1,5)
    
    if foundTool ==False:
        similarityTool =0   
    if similarityTool >= similarityNoTool:
        toolType = classifier_check(onnx,image)
        cv2.imshow("check",picfull)
        print(similarityTool, similarityNoTool)
        place = placeTool
        if (notEntireVisible or tool["ClassifierThinks"] ==None or toolType == tool["ClassifierThinks"]) and similarityTool != 0 and symbol_check(tool,image,modFrame,threshold,degrees,degreesDiv,0):
            
            checkedOut =1
            color = (256,0,256)
        else:
            place = ((0,0),(toolLocation[2],toolLocation[3]))
            errors["errors"].append({"ID": 0, "ToolType": toolType,"EventType": 3, "ToolID": tool["ID"], "UserID": 1, "Timestamp":timeStamp ,"Location": drawerID, "X":toolLocation[0], "Y": toolLocation[1], "W": toolLocation[2], "H": toolLocation[3]})   
            checkedOut = -1
            color = (0,0,0)
    else:
        checkedOut = 0
        place = placeNoTool
        color =(0,256,256)
    if record ==1:
        print(toolLocation[0],place[0][0])
        cv2.rectangle(modFrame, (toolLocation[0]+place[0][0],toolLocation[1]+place[0][1]), 
                      (toolLocation[0] +place[0][0]+ toolLocation[2],toolLocation[1] +place[0][1]+ toolLocation[3]), color, 1 )
        
    print(errors) 
    return checkedOut
def classifier_check(classifier, image):
    if classifier ==None:
        return None
    normalized_image = cv2.normalize(image, None, 0, 1, cv2.NORM_MINMAX)
    classifier.setInput(cv2.dnn.blobFromImage(normalized_image, size=(224, 224), swapRB=False, crop=True))
    detection = classifier.forward()
    #print(detection)
    answer = np.absolute(detection)
    #print(answer)
    maximum = np.max(answer)
    #print(maximum)
    answer = np.where(answer == maximum)[1]
    labels= gcon.get("onnxlabels")
    #print(labels)
    #print(answer)
    index = answer.item()
    print(labels[index])
    return labels[index]
def symbol_check(tool, image, modFrame, threshold, degrees, degreesDiv, record):
    if tool["IDAvail"] ==True:
        found,_,_ = drawer.draw_temp(tool["picall"],image, modFrame, image.shape[0], image.shape[1],(256,256,256), threshold,record,degrees,degreesDiv)  
    else:
        found =True
    return found       
    

                


    


    
           
          
        
        

