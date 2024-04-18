#!/bin/bash

  echo "running"
 python main.py  -test 45shadowbox/45_fishsp_0.avi -record > drawer3/zero.txt  & 
 pid1=$!
 wait $pid1
 echo "zero"
  python main.py  -test 45shadowbox/45_fishsp_1.avi -record > drawer3/one.txt  &
  pid1=$!
 wait $pid1
 echo "one"
   python main.py  -test 45shadowbox/45_fishsp_2.avi -record > drawer3/two.txt  &
   pid1=$!
 wait $pid1
 echo "two"
   python main.py  -test 45shadowbox/45_fishsp_3.avi -record > drawer3/three.txt  &
   pid1=$!
   wait $pid1
 echo "three"
   python main.py  -test 45shadowbox/45_fishsp_4.avi -record > drawer3/four.txt  &
   pid1=$!
   wait $pid1
 echo "four"
   python main.py  -test 45shadowbox/45_fishsp_5.avi -record > drawer3/five.txt  &
   pid1=$!
   wait $pid1
 echo "five"
   python main.py  -test 45shadowbox/45_fishsp_6.avi -record > drawer3/six.txt  &
 
   pid1=$!
   wait $pid1 
 echo "six"
   python main.py  -test 45shadowbox/45_fishsp_7.avi -record > drawer3/seven.txt  &
   pid1=$!
   wait $pid1
echo "seven"
  python main.py  -test 45shadowbox/45_fishsp_8.avi -record > drawer3/eight.txt  &
  pid1=$!
  wait $pid1
echo "eight"
  python main.py  -test 45shadowbox/45_fishsp_9.avi -record > drawer3/nine.txt  &
  pid1=$!
  wait $pid1
echo "nine"
  python main.py  -test 45shadowbox/45_fishsp_10.avi -record > drawer3/ten.txt  &
  pid1=$!
  wait $pid1
echo "ten"
  echo "end"