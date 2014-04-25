#!/bin/bash

dir=$(pwd)
cd $1
for pic in $(ls); do
  if [ "${pic##*.}" != "jpg" ] then
    convert $pic "${pic%.*}.jpg"
    rm $pic
  fi
done
cd $dir
