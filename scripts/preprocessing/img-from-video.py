#!/usr/bin/env python3

import cv2

vidcap = cv2.VideoCapture(str(input('Video Filename: ')))
ret, frame = vidcap.read()
cnt=0
while ret:
    cv2.imwrite('frame-%d.jpg' % cnt, frame)
    ret, frame = vidcap.read()
    cnt += 1

