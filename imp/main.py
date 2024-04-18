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

def create_error_records(events,errors):
    #print(events)
    #print(errors)
    for error in errors["errors"]:
        if error == None:
            continue
        #print(error)
        #print(events)
        events["events"].append({"ID": events["total"], "EventType": error["EventType"], "ToolID": error["ToolID"], "UserID": error["UserID"], "Timestamp":error['Timestamp'] ,"Location": error["Location"], "notes":error["ToolType"]+ str(error["X"])+ str(error["Y"])})
        #print(events["total"])
        events["total"] = events["total"]+1
        #print(events)
    updatedEvents= events
    return updatedEvents
def print_records(events, toolboxID):
    #print(events)
    for event in events["events"]:
        if event["EventType"] == 0:
            print("Opened: Toolbox " + str(toolboxID) + " Drawer "+ str(event["Location"]) + ": " + str(event["Timestamp"]) + " " + str(event["UserID"]))
        elif event["EventType"] == 1:
            print("Closed: Toolbox " + str(toolboxID) + " Drawer "+ str(event["Location"] )+ ": " + str(event["Timestamp"]) + " " + str(event["UserID"]))
        #etc
        elif event["EventType"] == 2: #<Tool identifier> <employee id> <time>  <location>
            print("Tool Checked Out:\n\t"  + str(event["ToolID"]) +" " + str(event["Timestamp"]) + " " + str(event["UserID"]) + " " + str(event["Location"] ))
        elif event["EventType"] == 3:   
            print("Tool Check In:\n\t"  + str(event["ToolID"]) +" " + str(event["Timestamp"]) + " " + str(event["UserID"]) + " " + str(event["Location"] ))  
        elif event["EventType"] == 4:  #<error type> <tool identifier> <employee id> <time> <location> 
            print("Error:\n\t"  +"wrong tool" + str(event["ToolID"]) +" " + str(event["Timestamp"]) + " " + str(event["UserID"]) + " " + str(event["Location"]) + " " +str(event["notes"]))
        elif event["EventType"] == 5:   
            print("Error:\n\t"  +"extra tool" + str(event["ToolID"]) +" " + str(event["Timestamp"]) + " " + str(event["UserID"]) + " " + str(event["Location"]) + " " +str(event["notes"]))
        elif event["EventType"] == 6:   
            print("Error:\n\t"  + "runtime error" + str(event["ToolID"]) +" " + str(event["Timestamp"]) + " " + str(event["UserID"]) + " " + str(event["Location"]) + " " +str(event["notes"]))      

    return
def retrieve_drawers(toolBoxID,test):
    if test == True:
        #input("Please enter the Toolbox number for the drawer in the given video:")
        f = open('drawer3_symbol/drawer.json')
        drawers = json.load(f)
    else:
        print("Databsase not connected yet")
        f = open('drawer1/drawer.json')
        drawers = json.load(f)
    return drawers
def  retrieve_tools(drawerID,toolboxID):
    f = open('drawer1/tools.json')
    tools = json.load(f)
    for tool in tools["Tools"]:
        #print(tool)
        tool["timestamp"] = None
        tool["error"] = 0 
        #print(tool)

    return tools

def update_events(events):
    print("No database")
    print_records(events,0)
    for event in events:
        print("No database")
        return 0
    return 0

def update_tools(oldTools, newTools, events,test):
    if newTools!=None and oldTools!=None:
        #print("check")
        for oldTool,newTool in zip(oldTools["Tools"],newTools["Tools"]):
            #print(oldTool['CheckedOut'],newTool['CheckedOut'])
            if oldTool['CheckedOut']!=newTool['CheckedOut']:
                if test ==False:
                    #apicall
                    print("database not set up yet")
                if newTool['CheckedOut'] == True:
                 #print(events)
                 events["events"].append({"ID": events["total"], "EventType": 2, "ToolID": newTool['ID'], "UserID": 1, "Timestamp":newTool['timestamp'] ,"Location": newTool['Location']})
                else:
                 events["events"].append({"ID": events["total"], "EventType": 3, "ToolID": newTool['ID'], "UserID": 1, "Timestamp":newTool['timestamp'] ,"Location": newTool['Location']})
                events["total"] = events["total"]+1
    return events, True
                
def wait_for_signal(hostIP,port):  
    print("enter signal")
    schema = {
        "type" : "object",
        "properties" : {
             "toolbox" : {"type" : "number"},
             "UserID" : {"type" : "number"},
        },
    }
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((hostIP, port))  
    s.listen(2)
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            conn.send(b"I am alive")
            data = conn.recv(1024)
            data = json.loads(data.decode('utf-8'))
            print(data)
            if data !=None:
                try:
                 jsonschema.validate(instance=data, schema=schema)
                except jsonschema.exceptions.ValidationError as err:
                    continue
                startTimeStamp = datetime.now()
                break
            else:    
                continue
    
    return data, startTimeStamp, conn, s

def get_footage(rtspStream, savedFootage, conn, s, startTimeStamp):
        print("get footage")
        timestampFrame =startTimeStamp
        endTimeStamp =None
        data =None
        schema = {"type" : ['object', 'boolean']
             }
        vid = cv2.VideoCapture(rtspStream) 
        if vid.isOpened():
            print(vid.isOpened())
            frame_width = int(vid.get(3)) 
            frame_height = int(vid.get(4)) 
            size = (frame_width, frame_height) 
            result = cv2.VideoWriter(savedFootage,  
                         cv2.VideoWriter_fourcc(*'XVID'), 
                         10, size) 
            vid.set(cv2.CAP_PROP_BUFFERSIZE,70)
            vid.set(cv2.CAP_PROP_FPS, 10)
            stopNotRecv = True
            while endTimeStamp ==None or timestampFrame <= endTimeStamp:
                #print(timestampFrame)
                if stopNotRecv:
                    s.setblocking(0)
                    try :
                        conn, addr = s.accept()
                        print(conn)
                        conn.setblocking(0)
                        data = conn.recv(1024)
                        print(data)
                        data = json.loads(data.decode('utf-8'))
                    except BlockingIOError:
                        pass
                    if data !=None:
                        try:
                            jsonschema.validate(instance=data, schema=schema)
                            print("check")
                        except jsonschema.exceptions.ValidationError as err:
                            data =None
                            continue
                        endTimeStamp = datetime.now()
                        print(endTimeStamp)
                        print(timestampFrame)
                        stopNotRecv = False
                        data =None
                ret, frame = vid.read() 
                if ret == False:
                    continue
                timedel = (timestampFrame + timedelta(milliseconds= 1000/10))-timestampFrame 
                timestampFrame = timestampFrame +timedel
                result.write(frame)
        else:
             raise FileNotFoundError("unable to open RTSP stream " + rtspStream )
        savedVideo = cv2.VideoCapture(savedFootage) 
        s.close()
        return endTimeStamp, savedVideo
                
                    
                    
    
    

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
            drawerList = retrieve_drawers(0,True)
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
                    tools = retrieve_tools(currentDrawer["ID"],0)
                    dconfig =open(currentDrawer["drawerYaml"], "r") 
                    drawerConfig =yaml.safe_load(dconfig)
                    oldtools = copy.deepcopy(tools)
                    newtools = copy.deepcopy(tools)
                if lastDrawer!=None and currentDrawer!=lastDrawer:
                    create_error_records(events,errors)
                    update_tools(oldtools,newtools, events, True)
                    events["events"].append({"ID": events["total"], "EventType": 1, "ToolID": None, "UserID": 1, "Timestamp":timestampFrame ,"Location": lastDrawer["ID"]})
                    events["total"] =events["total"]+1
                    print_records(events,0)
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
            create_error_records(events,errors)
            #print(events)
            update_tools(oldtools,newtools, events, True)
            print_records(events,0)
        else:
            print("failed to open")        
    else:
         data, startTimeStamp, conn, s = wait_for_signal(gcon.get("rfidhost"),gcon.get("rfidport")) 
         rtsp = gcon.get("RTSP")
         endTimeStamp, savedVideo =get_footage(rtsp[data["toolbox"]],"temp"+ str(data["toolbox"])+".avi", conn,s, startTimeStamp) 
    #retrieve from database
    #print("done")

    return

config =open("g_conf.yaml", "r") 
gcon =yaml.safe_load(config)
if __name__ == "__main__":
    main()