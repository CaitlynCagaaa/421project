import cv2 
import numpy as np
import math
import json
import yaml
from matplotlib import pyplot as plt
import argparse
import drawer
import datetime;

def retrieveDrawers():
    f = open('drawer.json')
    data = json.load(f)
    return f

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
    print('check')
    args = ap.parse_args()
    if args.record ==1:
        print("record")
    if args.test!=None:
        vid = cv2.VideoCapture(args.test) 
        if vid.isOpened():
            print(args.test)
            ret, frame = vid.read()
            drawerList = retrieveDrawers()
            events = {"events":[]}
            tools = None
            while(ret):
                drawer.find_drawer(frame, drawerList, events, tools,1, timestampFrame)



            
    else:
        print(' no ')
    
    #retrieve from database
        
   


    return


if __name__ == "__main__":
    main()