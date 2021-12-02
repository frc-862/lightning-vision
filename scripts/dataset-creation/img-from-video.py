#!/usr/bin/env python3

""" Extract image frames from video

usage: img-from-video.py [-h] [-i IMAGEDIR]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTVIDEO, --inputVideo INPUTVIDEO
                        Path to the input video.
"""

import cv2
import os
import argparse

def main():

    # Initiate argument parser
    parser = argparse.ArgumentParser(description="Extract image frames from video",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '-i', '--inputVideo',
        help='Path to the input video.',
        type=str
    )
    args = parser.parse_args()

    vidcap = cv2.VideoCapture(args.inputVideo)
    ret, frame = vidcap.read()
    cnt=0
    while ret:
        cv2.imwrite('frame-%d.jpg' % cnt, frame)
        ret, frame = vidcap.read()
        cnt += 1



if __name__ == '__main__':
    main()

