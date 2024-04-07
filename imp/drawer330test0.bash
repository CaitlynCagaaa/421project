#!/bin/bash

 echo "running"
python main.py  -test drawer330_0_0.avi -record > drawer1/zero.txt  & 
pid1=$!
wait $pid1
echo "zero"
 python main.py  -test drawer330_0_1.avi -record > drawer1/one.txt  &
 pid1=$!
wait $pid1
echo "one"
  python main.py  -test drawer330_0_2.avi -record > drawer1/two.txt  &
  pid1=$!
wait $pid1
echo "two"
  python main.py  -test drawer330_0_3.avi -record > drawer1/three.txt  &
  pid1=$!
  wait $pid1
echo "three"
  python main.py  -test drawer330_0_4.avi -record > drawer1/four.txt  &
  pid1=$!
  wait $pid1
echo "four"
  echo "end"