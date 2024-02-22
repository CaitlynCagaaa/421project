import cv2 
import numpy as np
import math
import json
import yaml
from matplotlib import pyplot as plt
import argparse
import drawer
from datetime import datetime, timedelta

def print_records(events, toolboxID):
    for event in events["events"]:
        if event["EventType"] == 0:
            print("Opened: Toolbox " + str(toolboxID) + " Drawer "+ event["Location"] + ": " + event["Timestamp"] + " " + event["UserID"])
        if event["EventType"] == 1:
            print("Closed: Toolbox " + str(toolboxID) + " Drawer "+ event["Location"] + ": " + event["Timestamp"] + " " + event["UserID"])
    
    return
def retrieve_drawers():
    f = open('drawer.json')
    data = json.load(f)
    return data

def main():
    timestampStart= datetime.now()
    timestampFrame =timestampStart
    config =open("g_conf.yaml", "r") 
    con =yaml.safe_load(config)
    ap = argparse.ArgumentParser()
    ap.add_argument("-test", "--test",type=str, required=False,
    help="location of video for testing", default=None)
    ap.add_argument("-record", "--record", type=int,required=False,
    help="int value for save modified video or not", default=False)
    args = ap.parse_args()
    if args.test!=None:
        vid = cv2.VideoCapture(args.test) 
        if args.record==1:
            print("recording")
            frame_width = int(vid.get(3)) 
            frame_height = int(vid.get(4)) 
            size = (frame_width, frame_height) 
            recordedVideo = cv2.VideoWriter( "test" + ".avi",  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         12, size) 
            print("test" +str(timestampStart) + ".avi")
        if vid.isOpened():
            print(args.test)
            ret, frame = vid.read()
            print(ret)
            drawerList = retrieve_drawers()
            events = {"events":[]}
            tools = None
            drawerWasOpen =0
            lastDrawer= None
            while(ret):
                print(ret)
                currentDrawer = drawer.find_drawer(frame, drawerList, events, tools,1, timestampFrame,args.record)
                if lastDrawer!=None and currentDrawer!=lastDrawer:
                    events["events"].append({"ID": 0, "EventType": 1, "ToolID": None, "UserID": 1, "Timestamp":timestampFrame ,"Location": drawer["ID"]})

                if args.record==1:
                    print("write")
                    recordedVideo.write(frame)
                ret, frame = vid.read() 
                timestampFrame = timedelta(seconds= 1/12)
            vid.release() 
            print_records(events, 0)




            
    else:
        print(' no ')
    
    #retrieve from database
        
   


    return


if __name__ == "__main__":
    main()