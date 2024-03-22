import toolrecognition
import drawer
import main
import datetime
import argparse
import cv2
import yaml
import json

ap = argparse.ArgumentParser()
ap.add_argument("-test", "--test",type=str, required=True,
help="location of video for testing", default=None)
args = ap.parse_args()
drawerList = main.retrieve_drawers(0,True)
events = {"events":[]}
errors = {"errors":[]}
frame =cv2.open(args.test)
tools = None
drawerWasOpen =0
lastDrawer= None
modFrame, currentDrawer, drawerSize = drawer.find_drawer(frame, drawerList,True)
if lastDrawer==None and currentDrawer!=None:
    print(currentDrawer)
    events["events"].append({"ID": 0, "EventType": 0, "ToolID": None, "UserID": 1, "Timestamp":0 ,"Location": currentDrawer["ID"]})
    main.retrieve_tools(currentDrawer["ID"],0)
    dconfig = config =open("drawer0/conf.yaml", "r") 
    drawerConfig =yaml.safe_load(dconfig)
if lastDrawer!=None and currentDrawer!=lastDrawer:
    events["events"].append({"ID": 0, "EventType": 1, "ToolID": None, "UserID": 1, "Timestamp":0 ,"Location": lastDrawer["ID"]})
oldtools= tools.copy()
toolrecognition.update_tools_for_frames(frame, modFrame, tools, errors, drawerSize,0,currentDrawer,drawerConfig,None)
main.create_error_records(events,errors)
main.update_tools(oldtools,tools, events, True)
main.print_records(events,0)
cv2.write(modFrame)
lastDrawer = currentDrawer
main.print_records(events, 0)
