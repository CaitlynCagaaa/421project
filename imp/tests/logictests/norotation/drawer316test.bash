#!/bin/bash

 echo "running"
python main.py  -test drawer316_0.avi -record > drawer0/zero.txt  & 
pid1=$!
wait $pid1
echo "zero"
 python main.py  -test drawer316_1.avi -record > drawer0/one.txt  &
 pid1=$!
wait $pid1
echo "one"
  python main.py  -test drawer316_2.avi -record > drawer0/two.txt  &
  pid1=$!
wait $pid1
echo "two"
  python main.py  -test drawer316_3.avi -record > drawer0/three.txt  &
  pid1=$!
  wait $pid1
echo "three"
  python main.py  -test drawer316_4.avi -record > drawer0/four.txt  &
  pid1=$!
  wait $pid1
echo "four"
  python main.py  -test drawer316_5.avi -record > drawer0/five.txt  &
  pid1=$!
  wait $pid1
echo "five"
  python main.py  -test drawer316_6.avi -record > drawer0/six.txt  &
  pid1=$!
  wait $pid1 
echo "six"
  python main.py  -test drawer316_7.avi -record > drawer0/seven.txt  &
  pid1=$!
  wait $pid1
echo "seven"
  python main.py  -test drawer316_8.avi -record > drawer0/eight.txt  &
  pid1=$!
  wait $pid1
echo "eight"
  echo "end"