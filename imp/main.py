import cv2 
import numpy as np
import math
import json
import yaml
from matplotlib import pyplot as plt
import argparse
import drawer
from datetime import datetime, timedelta
def create_error_records(events,errors):
    for error in errors:
        events = events["events"].append({"ID": 0, "EventType": error["EventType"], "ToolID": error["ToolID"], "UserID": error["UserID"], "Timestamp":error['timestamp'] ,"Location": error['location'], "notes":error["notes"]})
    updatedEvents= events
    return updatedEvents
def print_records(events, toolboxID):
    print(events)
    for event in events["events"]:
        if event["EventType"] == 0:
            print("Opened: Toolbox " + str(toolboxID) + " Drawer "+ str(event["Location"]) + ": " + str(event["Timestamp"]) + " " + str(event["UserID"]))
        elif event["EventType"] == 1:
            print("Closed: Toolbox " + str(toolboxID) + " Drawer "+ str(event["Location"] )+ ": " + str(event["Timestamp"]) + " " + str(event["UserID"]))
        #etc
        elif event["EventType"] == 2:
            print("Closed: Toolbox " + str(toolboxID) + " Drawer "+ str(event["Location"] )+ ": " + str(event["Timestamp"]) + " " + str(event["UserID"]))
    return
def retrieve_drawers(toolBoxID,test):
    if test == True:
        input("Please enter the Toolbox number for the drawer in the given video:")
        f = open('drawer.json')
        drawers = json.load(f)
    else:
        print("Databsase not connected yet")
        exit()
    return drawers
def  retrieve_tools(drawerID,toolboxID):
    f = open('tools.json')
    tools = json.load(f)
    for tool in tools:
        tool.append({"timestamp": None, "error":0 })
        print(tool)

    return tools

def update_events(events):
    for event in events:
        print("No database")
        return 0
    return 0

def update_tools(oldTools, newTools, events,test):
    for oldTool,newTool in zip(oldTools,newTools):
        if oldTool['CheckedOut']!=newTool['CheckedOut']:
            if test ==False:
                #apicall
                print("database not set up yet")
            if newTool['CheckedOut'] == True:
                events = events["events"].append({"ID": 0, "EventType": 2, "ToolID": None, "UserID": 1, "Timestamp":newTool['timestamp'] ,"Location": newTool['location']})
            else:
                 events = events["events"].append({"ID": 0, "EventType": 3, "ToolID": None, "UserID": 1, "Timestamp":newTool['timestamp'] ,"Location": newTool['location']})

    return events, True
                
                
        
    

def main():
    timestampStart= datetime.now()
    timestampFrame =timestampStart
    ap = argparse.ArgumentParser()
    ap.add_argument("-test", "--test",type=str, required=False,
    help="location of video for testing", default=None)
    ap.add_argument("-record", "--record", action='store_true',
    help="int value for save modified video or not", default=False)
    args = ap.parse_args()
    if args.test!=None:
        vid = cv2.VideoCapture(args.test) 
        if args.record:
            print("recording")
            frame_width = int(vid.get(3)) 
            frame_height = int(vid.get(4)) 
            size = (frame_width, frame_height) 
            recordedVideo = cv2.VideoWriter( "test2" + ".avi",  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         30, size) 
            print("test" +str(timestampStart) + ".avi")
        if vid.isOpened():
            print(args.test)
            ret, frame = vid.read()
            print(ret)
            drawerList = retrieve_drawers(0,True)
            events = {"events":[]}
            tools = None
            drawerWasOpen =0
            lastDrawer= None
            while(ret):
                print(ret)
                modFrame, currentDrawer, drawerSize = drawer.find_drawer(frame, drawerList,args.record)
                if lastDrawer==None and currentDrawer!=None:
                    print(currentDrawer)
                    events["events"].append({"ID": 0, "EventType": 0, "ToolID": None, "UserID": 1, "Timestamp":timestampFrame ,"Location": currentDrawer["ID"]})
                if lastDrawer!=None and currentDrawer!=lastDrawer:
                    events["events"].append({"ID": 0, "EventType": 1, "ToolID": None, "UserID": 1, "Timestamp":timestampFrame ,"Location": lastDrawer["ID"]})

                if args.record==1:
                    print("write")
                    recordedVideo.write(modFrame)
                ret, frame = vid.read() 
                timedel = (timestampFrame + timedelta(milliseconds= 5))-timestampFrame 
                timestampFrame = timestampFrame +timedel
                print(timestampFrame)
                lastDrawer = currentDrawer
            vid.release() 
            print_records(events, 0)




            
    else:
        print(' no ')
    
    #retrieve from database
        
   


    return

config =open("g_conf.yaml", "r") 
con =yaml.safe_load(config)
if __name__ == "__main__":
    main()