import cv2 
import numpy as np
import math
import json
import yaml
from matplotlib import pyplot as plt
import argparse
import drawer
from datetime import datetime, timedelta
import socket
from pathlib import Path
import jsonschema 
import toolrecognition
import copy
import main
config =open("g_conf.yaml", "r") 
gcon =yaml.safe_load(config)


ap = argparse.ArgumentParser()
ap.add_argument("-test", "--test",type=str, required=False,
help="location of video for testing", default=None)
ap.add_argument("-record", "--record", action='store_true',
help="int value for save modified video or not", default=False)
args = ap.parse_args()
if args.test!=None:
        vid = cv2.VideoCapture(args.test) 
        if args.record:
            #print("recording")
            frame_width = int(vid.get(3)) 
            frame_height = int(vid.get(4)) 
            size = (frame_width, frame_height) 
            recordedVideo = cv2.VideoWriter( Path(args.test).stem + "record.avi",  
                         cv2.VideoWriter_fourcc(*'MJPG'), 
                         15, size) 
            #print("test" +str(timestampStart) + ".avi")
        if vid.isOpened():
            print(args.test)
            ret, frame = vid.read()
            print(ret)
            drawerList = main.retrieve_drawers(0,True)
            events = {"events":[],"total": 0}
            #print(events)
            errors = {"errors":[], "total": 0}
            #print(errors)
            cv2.waitKey(0)
            tools = None
            drawerWasOpen =0
            lastDrawer= None
            while(ret):
                #print(ret)
                modFrame, currentDrawer, drawerSize = drawer.find_drawer(frame, drawerList,args.record)
                if lastDrawer==None and currentDrawer!=None:
                    #print(currentDrawer)
                    events["events"].append({"ID": events["total"], "EventType": 0, "ToolID": None, "UserID": 1, "Timestamp":timestampFrame ,"Location": currentDrawer["ID"]})
                    events["total"] =events["total"]+1
                    tools = main.retrieve_tools(currentDrawer["ID"],0)
                    dconfig =open(currentDrawer["drawerYaml"], "r") 
                    drawerConfig =yaml.safe_load(dconfig)
                    oldtools = copy.deepcopy(tools)
                    newtools = copy.deepcopy(tools)
                if lastDrawer!=None and currentDrawer!=lastDrawer:
                    main.create_error_records(events,errors)
                    main.update_tools(oldtools,newtools, events, True)
                    events["events"].append({"ID": events["total"], "EventType": 1, "ToolID": None, "UserID": 1, "Timestamp":timestampFrame ,"Location": lastDrawer["ID"]})
                    events["total"] =events["total"]+1
                    main.print_records(events,0)
                    events = {"events":[],"total": events["total"]}
                    oldtools = None
                    newtools =None
                    tools = None
                    errors = {"errors":[],"total": errors["total"]}
                if currentDrawer!=None:
                    net =  cv2.dnn.readNetFromONNX(gcon.get("onnxfile")) 
                    #print(oldtools)
                    newtools, errors= toolrecognition.update_tools_for_frames(frame, modFrame, newtools, errors, drawerSize,timestampFrame,currentDrawer,drawerConfig,net,1)
                    #print(oldtools)
                if args.record==1:
                    #print("write")
                    recordedVideo.write(modFrame)
                ret, frame = vid.read() 
                timedel = (timestampFrame + timedelta(milliseconds= 1000/15))-timestampFrame 
                timestampFrame = timestampFrame +timedel
                #print(timestampFrame)
                lastDrawer = currentDrawer
            vid.release() 
            main.create_error_records(events,errors)
            #print(events)
            main.update_tools(oldtools,newtools, events, True)
            main.print_records(events,0)
        else:
            print("failed to open")        
else:
    data, startTimeStamp = main.wait_for_signal(gcon.get("rfidhost"),gcon.get("rfidport")) 
    rtsp = gcon.get("RTSP")
    endTimeStamp, savedVideo = main.get_footage(rtsp[data["toolbox"]],"temp"+ str(data["toolbox"])+".avi", gcon.get("rfidhost"),gcon.get("rfidport"), startTimeStamp) 
    #retrieve from database
    #print("done")
