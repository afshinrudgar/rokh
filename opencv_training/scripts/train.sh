#!/bin/bash

opencv_traincascade -data classifier -vec samples.vec -bg negatives.txt -numStages 20 -minHitRate 0.999 -maxFalseAlarmRate 0.5 -numPos 100 -numNeg 54 -w 40 -h 40 -mode ALL -precalcValBufSize 512 -precalcIdxBufSize 512
