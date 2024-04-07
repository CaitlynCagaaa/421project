#!/bin/bash

 echo "running"
python rtsp.py "45shadowbox/45_fishws_0"  & 
pid1=$!
wait $pid1
echo "zero"
 python rtsp.py "45shadowbox/45_fishws_1"  &
 pid1=$!
wait $pid1
echo "one"
  python rtsp.py "45shadowbox/45_fishws_2"  &
  pid1=$!
wait $pid1
echo "two"
  python rtsp.py "45shadowbox/45_fishws_3"  &
  pid1=$!
  wait $pid1
echo "three"
  python rtsp.py "45shadowbox/45_fishws_4"  &
  pid1=$!
  wait $pid1
  echo "three"
  python rtsp.py "45shadowbox/45_fishws_5"  &
  pid1=$!
  wait $pid1
  echo "three"
  python rtsp.py "45shadowbox/45_fishws_6"  &
  pid1=$!
  wait $pid1
  echo "three"
  python rtsp.py "45shadowbox/45_fishws_7"  &
  pid1=$!
  wait $pid1
  echo "three"
  python rtsp.py "45shadowbox/45_fishws_8"  &
  pid1=$!
  wait $pid1
  echo "three"
  python rtsp.py "45shadowbox/45_fishws_9"  &
  pid1=$!
  wait $pid1
  echo "three"
  python rtsp.py "45shadowbox/45_fishws_10"  &
  pid1=$!
  wait $pid1
  echo "three"
  python rtsp.py "45shadowbox/45_fishws_11"  &
  pid1=$!
  wait $pid1
  echo "three"
  python rtsp.py "45shadowbox/45_fishws_12"  &
  pid1=$!
  wait $pid1
  echo "three"
  python rtsp.py "45shadowbox/45_fishsp_0"  &
  pid1=$!
  wait $pid1
  echo "three"
  python rtsp.py "45shadowbox/45_fishsp_1"  &
  pid1=$!
  wait $pid1
  echo "three"
  python rtsp.py "45shadowbox/45_fishsp_2"  &
  pid1=$!
  wait $pid1
  echo "three"
  python rtsp.py "45shadowbox/45_fishsp_3"  &
  pid1=$!
  wait $pid1
  echo "three"
  python rtsp.py "45shadowbox/45_fishsp_4"  &
  pid1=$!
  wait $pid1
  echo "three"
  python rtsp.py "45shadowbox/45_fishsp_5"  &
  pid1=$!
  wait $pid1
  echo "three"
  python rtsp.py "45shadowbox/45_fishsp_6"  &
  pid1=$!
  wait $pid1

  echo "three"
  python rtsp.py "45shadowbox/45_fishsp_7"  &
  pid1=$!
  wait $pid1
  echo "three"
  python rtsp.py "45shadowbox/45_fishsp_8"  &
  pid1=$!
  wait $pid1
  echo "three"
  python rtsp.py "45shadowbox/45_fishsp_9"  &
  pid1=$!
  wait $pid1
  echo "three"
  python rtsp.py "45shadowbox/45_fishsp_10"  &
  pid1=$!
  wait $pid1
  echo "three"
  echo "end"