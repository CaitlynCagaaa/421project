import cv2 
import numpy as np
import math
import json
import yaml
from matplotlib import pyplot as plt
import argparse



def main():
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
    else:
        print(' no ')
   


    return


if __name__ == "__main__":
    main()