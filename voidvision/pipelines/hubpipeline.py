#!/usr/bin/env python3

import os

from matplotlib import use
from pipeline import VisionPipeline
import camera
import numpy as np
import cv2
import sys
from time import sleep
import time

class HubPipeline(VisionPipeline):

    def __init__(self, config: str, cam_num: int, cam_name: str, output_name: str, table) -> None:
        self.nttable = table
		
        # start camera
        self.inp, self.out, self.width, self.height, self.cam, self.exposure, self.brightness, self.cameraPath = camera.start(config, cam_num, cam_name, output_name)

        self.lower_green = np.array([50.179, 89.433, 34.397])
        self.high_green = np.array([83.03, 255, 255])
        # Set this to true for tuning

            # self.green_lower_threshold.setNumber(100) # 100 is default for now

        # Horizontal and vertical field of view


		# dashboard outputs
        # self.target_distance_entry.setNumber(-1)
        # self.target_angle_entry.setNumber(0)

        # allocate image for whenever
        self.img = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)
        self.output_img = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)

    def threshold(self, img):
        hue_lower_upper = [50.17985611510791, 83.03030303030302]
        saturation_lower_upper = [89.43345323741008, 255.0]
        value_lower_upper = [34.39748201438849, 255.0]

        lower_green = np.array([50.179, 89.433, 34.397])
        high_green = np.array([83.03, 255, 255])
        img = cv2.inRange(img, lower_green, high_green)
        return img

    def process(self):
        self.t, self.img = self.inp.grabFrame(self.img)
        img = self.img
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img = self.threshold(img)
        img = cv2.erode(img, None, (-1, -1), iterations = 1, borderType = cv2.BORDER_CONSTANT, borderValue = -1)
        img = cv2.dilate(img, None, (-1,-1), iterations = 1,borderType = cv2.BORDER_CONSTANT, borderValue = -1)
        contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
        maxPt = [-np.inf, -np.inf]
        minPt = [np.inf, np.inf]
    
        for c in contours:
            maxc = np.max(c, axis = 0)[0]
            minc = np.min(c, axis = 0)[0]

            if maxPt[0] < maxc[0]:
                maxPt[0] = maxc[0]

            if maxPt[1] < maxc[1]:
                maxPt[1] = maxc[1]

            if minPt[0] > minc[0]:
                minPt[0] = minc[0]

            if minPt[1] > minc[1]:
                minPt[1] = minc[1]

        y = (maxPt[0] + minPt[0]) / 2
        x = (maxPt[1] + minPt[1]) / 2
        self.nttable.putNumber('x', x)
        self.nttable.putNumber('y', y)