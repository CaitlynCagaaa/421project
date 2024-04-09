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
import os
config =open("g_conf.yaml", "r") 
gcon =yaml.safe_load(config)


ap = argparse.ArgumentParser()
ap.add_argument("-test", "--test",type=str, required=False,
help="location of video for testing", default=None)
ap.add_argument("-record", "--record", action='store_true',
help="int value for save modified video or not", default=False)
args = ap.parse_args()
events = {"events":[],"total": 0}
errors = {"errors":[], "total": 0}
tools = None
drawerWasOpen =0
lastDrawer= None
try:
    while(True):
        if args.test!=None:
            savedVideo = cv2.VideoCapture(args.test) 
            data = {"toolbox": 0, "UserID": 0}
            test = True
        else:
            data, startTimeStamp = main.wait_for_signal(gcon.get("rfidhost"),gcon.get("rfidport")) 
            rtsp = gcon.get("RTSP")
            try:
                endTimeStamp, savedVideo = main.get_footage(rtsp[data["toolbox"]],"temp"+ str(data["toolbox"])+".avi", gcon.get("rfidhost"),gcon.get("rfidport"), startTimeStamp) 
            except FileNotFoundError as err:
                events["events"].append({"ID": events["total"], "EventType": 6, "ToolID": None, "UserID": data["UserID"], "Timestamp":startTimeStamp ,"Location": None,"Notes": "FileNotFound "+  str(err)})
                events["total"] =events["total"]+1
                main.update_events(events)
                continue
            events["events"].append({"ID": events["total"], "EventType": 7, "ToolID": None, "UserID": data["UserID"], "Timestamp":startTimeStamp ,"Location": None,"Notes": "Logged into toolbox "+ str(data["toolbox"]) })
            events["total"] =events["total"]+1
            test = False
        if args.record:
            #print("recording")
            os.makedirs(startTimeStamp.month, exist_ok = True) 
            frame_width = int(savedVideo.get(3)) 
            frame_height = int(savedVideo.get(4)) 
            size = (frame_width, frame_height) 
            recordedVideo = cv2.VideoWriter( startTimeStamp.month+ "/" +startTimeStamp.day+ startTimeStamp.hour+ startTimeStamp.second+ startTimeStamp.microsecond + "record.avi",  
            cv2.VideoWriter_fourcc(*'MJPG'), 
            10, size) 
            #print("test" +str(timestampStart) + ".avi")
        if savedVideo.isOpened():
            print(args.test)
            ret, frame = savedVideo.read()
            print(ret)
            try:
                drawerList = main.retrieve_drawers(data["toolbox"],test)
            except RuntimeError as err :
                events["events"].append({"ID": events["total"], "EventType": 6, "ToolID": None, "UserID": data["UserID"], "Timestamp":startTimeStamp ,"Location": None,"Notes": "Closing program, Error in retriving drawers: " +err})
                events["total"] =events["total"]+1
                if -test ==None:
                    main.print_records(events,data["toolbox"])
                    exit(0)
                else:
                    main.update_events(events)   
                    continue
            #print(errors)
            try:
                while(ret):
                    #print(ret)
                    modFrame, currentDrawer, drawerSize = drawer.find_drawer(frame, drawerList,args.record)
                    if lastDrawer==None and currentDrawer!=None:
                    #print(currentDrawer)
                        events["events"].append({"ID": events["total"], "EventType": 0, "ToolID": None, "UserID": 1, "Timestamp":timestampFrame ,"Location": currentDrawer["ID"]})
                        events["total"] =events["total"]+1
                        try:
                            tools = main.retrieve_tools(currentDrawer["ID"],data["toolbox"])
                        except RuntimeError as err :
                            events["events"].append({"ID": events["total"], "EventType": 6, "ToolID": None, "UserID": data["UserID"], "Timestamp":startTimeStamp ,"Location": None,"Notes": "Closing program, Error in retriving tools: " +str(err)})
                            events["total"] =events["total"]+1
                            if -test ==None:
                                main.print_records(events,data["toolbox"])
                                exit(0)
                            else:
                                main.update_events(events)   
                                continue
                        dconfig =open(currentDrawer["drawerYaml"], "r") 
                        drawerConfig =yaml.safe_load(dconfig)
                        oldtools = copy.deepcopy(tools)
                        newtools = copy.deepcopy(tools)
                    if lastDrawer!=None and currentDrawer!=lastDrawer:
                        main.create_error_records(events,errors)
                        main.update_tools(oldtools,newtools, events, True)
                        events["events"].append({"ID": events["total"], "EventType": 1, "ToolID": None, "UserID": 1, "Timestamp":timestampFrame ,"Location": lastDrawer["ID"]})
                        events["total"] =events["total"]+1
                        if test ==True:
                            main.print_records(events,data["toolbox"])
                        else:
                            main.update_events(events)
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
                    ret, frame = savedVideo.read() 
                    timedel = (timestampFrame + timedelta(milliseconds= 1000/15))-timestampFrame 
                    timestampFrame = timestampFrame +timedel
                    #print(timestampFrame)
                    lastDrawer = currentDrawer
                savedVideo.release() 
                main.create_error_records(events,errors)
                #print(events)
                main.update_tools(oldtools,newtools, events, True)
                if test ==True:
                    main.print_records(events,data["toolbox"])
                    exit(0)

                else:
                    events["events"].append({"ID": events["total"], "EventType": 8, "ToolID": None, "UserID": data["UserID"], "Timestamp":startTimeStamp ,"Location": None,"Notes": "Logged out of toolbox "+ str(data["toolbox"]) })
                    main.update_events(events)
            except RuntimeError as err :
                events["events"].append({"ID": events["total"], "EventType": 6, "ToolID": None, "UserID": data["UserID"], "Timestamp":startTimeStamp ,"Location": None,"Notes": " Error in processing frame: " +str(err)})
                events["total"] =events["total"]+1
                if -test ==None:
                    main.print_records(events,data["toolbox"])
                    exit(0)
                else:
                    main.update_events(events)   
                    continue
        else:
            events["events"].append({"ID": events["total"], "EventType": 6, "ToolID": None, "UserID": data["UserID"], "Timestamp":startTimeStamp ,"Location": None,"Notes": "failed to open video "})
            events["total"] =events["total"]+1
            if -test ==None:
                main.print_records(events,data["toolbox"])
                exit(0)
            else:
                main.update_events(events)   
                continue  
except RuntimeError as err :
                    events["events"].append({"ID": events["total"], "EventType": 6, "ToolID": None, "UserID": data["UserID"], "Timestamp":startTimeStamp ,"Location": None,"Notes": "Closing program: " +err})
                    events["total"] =events["total"]+1
                    if -test ==None:
                        main.print_records(events,data["toolbox"])
                        exit(0)
                    else:
                        main.update_events(events)   
                        exit(0)