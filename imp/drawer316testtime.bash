#!/bin/bash

 echo "running"
 echo "zero"
 time python main.py  -test drawer316_0.avi -record  &
pid1=$!
wait $pid1
echo "one"
 time python main.py  -test drawer316_1.avi -record   &
  pid1=$!
 wait $pid1
 echo "two"
  time python main.py  -test drawer316_2.avi -record   &
   pid1=$!
 wait $pid1
 echo "three"
  time python main.py  -test drawer316_3.avi -record   &
   pid1=$!
   wait $pid1
   echo "four"
  time python main.py  -test drawer316_4.avi -record   &
   pid1=$!
   wait $pid1
   echo "five"
  time python main.py  -test drawer316_5.avi -record   &
   pid1=$!
   wait $pid1
   echo "six"
  time python main.py  -test drawer316_6.avi -record   &
   pid1=$!
   wait $pid1 
   echo "seven"
 time python main.py  -test drawer316_7.avi -record  &
  pid1=$!
  wait $pid1
  echo "eight"
 time python main.py  -test drawer316_8.avi -record   &
  pid1=$!
  wait $pid1
  echo "end"