#!/bin/bash

 echo "running"
python main.py  -test drawer330_1_0.avi -record > drawer2/zero.txt  & 
pid1=$!
wait $pid1
echo "zero"
 python main.py  -test drawer330_1_1.avi -record > drawer2/one.txt  &
 pid1=$!
wait $pid1
echo "one"
  python main.py  -test drawer330_1_2.avi -record > drawer2/two.txt  &
  pid1=$!
wait $pid1
echo "two"
  python main.py  -test drawer330_1_3.avi -record > drawer2/three.txt  &
  pid1=$!
  wait $pid1
echo "three"
  echo "end"