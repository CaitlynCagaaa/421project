import toolrecognition
import drawer
import main
import datetime
import argparse
import cv2
import yaml
import json

gcon =open("g_conf.yaml", "r")
gcon =yaml.safe_load(gcon)
ap = argparse.ArgumentParser()
ap.add_argument("-test", "--test",type=str, required=True,
help="location of video for testing", default=None)
args = ap.parse_args()
drawerList = main.retrieve_drawers(0,True)
events = {"events":[]}
errors = {"errors":[]}
frame =cv2.imread(args.test,cv2.IMREAD_UNCHANGED)
tools = None
drawerWasOpen =0
lastDrawer= None
modFrame, currentDrawer, drawerSize = drawer.find_drawer(frame, drawerList,True)
if lastDrawer==None and currentDrawer!=None:
    print(currentDrawer)
    events["events"].append({"ID": 0, "EventType": 0, "ToolID": None, "UserID": 1, "Timestamp":0 ,"Location": currentDrawer["ID"]})
    tools = main.retrieve_tools(currentDrawer["ID"],0)
    dconfig =open("drawer0/conf.yaml", "r") 
    drawerConfig =yaml.safe_load(dconfig)
    oldtools= tools.copy()
if lastDrawer!=None and currentDrawer!=lastDrawer:
    events["events"].append({"ID": 0, "EventType": 1, "ToolID": None, "UserID": 1, "Timestamp":0 ,"Location": lastDrawer["ID"]})
net =  cv2.dnn.readNetFromONNX(gcon.get("onnxfile")) 
tools, errors= toolrecognition.update_tools_for_frames(frame, modFrame, tools, errors, drawerSize,0,currentDrawer,drawerConfig,net,1)
print(events)
main.create_error_records(events,errors)
main.update_tools(oldtools,tools, events, True)
main.print_records(events,0)
cv2.imwrite("test.jpg",modFrame)
lastDrawer = currentDrawer
main.print_records(events, 0)
