#!/usr/bin/env python3

import os
from re import A, I

from matplotlib import use
from pipeline import VisionPipeline
import camera
import numpy as np
import cv2
import sys
from time import sleep
import threading
import time
import processingpipeline

class HubPipeline(VisionPipeline):

    def __init__(self, config: str, cam_num: int, cam_name: str, output_name: str, table) -> None:

        self.nttable = table
		
        # start camera
        self.inp, self.out, self.width, self.height, self.cam, self.exposure, self.brightness, self.cameraPath = camera.start(config, cam_num, cam_name, output_name)

        # initial intensity threshold
        self.intensity_thresh = 100

        # Decides how many images to capture and write to jetson, writes are sequential with processed output
        self.imgs_to_capture = 1
        self.last_save_time = time.clock()
        # self.img_capture_interval = table.getEntry('Image capture interval (seconds)')
        # self.img_capture_interval.setNumber()

        # Set this to true for tuning
        self.debug = True
        if self.debug:
            self.init_debug()
        # Horizontal and vertical field of view
        self.fov_horiz = 99 
        self.fov_vert = 68.12 


		# dashboard outputs
        self.target_distance_entry = table.getEntry('Target Distance')
        self.target_angle_entry = table.getEntry('Target Angle')
        # self.target_distance_entry.setNumber(-1)
        # self.target_angle_entry.setNumber(0)

    def save_image(self):
        fname = str('/tmp/{}.png'.format(self.t))
        cv2.imwrite(fname, self.img)

    def process(self):
        # This is to verify camera parameters we want set are set
        # set exposure
        # TODO: not call every time process is run, only when updated

        if self.debug:
           self.process_debug() 

        # get frame from camera
        self.t, self.img = self.inp.grabFrame(self.img)

        # Saves the time every 5 seconds, time.clock is in seconds
        now = time.process_time()
        if now - self.last_save_time > 5:
            threading.Thread(target=self.save_image).start()
            self.last_save_time = now

        pipeline = processingpipeline.Processing()

        pipeline.return_contours(self.img)

        targetDistance, targetAngle = pipeline.process_contours()
        
        self.target_distance_entry.setDouble(targetDistance)
        self.target_angle_entry.setDouble(targetAngle)


        # print('DIST: {} | ANGLE: {}'.format(targetDistance, targetAngle))

        # TODO: Puts number of contours detected in current image to the dashboard
        # self.nttable.putNumber('Contour Number', numContours)
        def process_debug(self):
            """
            Functions to be run if we're in debug mode 
            """
            # print("we're in debug")
            new_exposure = self.exposure_entry.getNumber(self.exposure)

            if (new_exposure is not self.exposure):
                self.exposure = new_exposure
                os.system("v4l2-ctl --device " + self.cameraPath + " --set-ctrl=exposure_absolute=" + str(self.exposure))

            new_brightness = self.brightness_entry.getNumber(self.brightness)
            if new_brightness != self.brightness:
                self.brightness = new_brightness
                os.system("v4l2-ctl --device " + self.cameraPath + " --set-ctrl=brightness=" + str(self.brightness))

            self.intensity_thresh = self.intensity_thresh_entry.getNumber(self.intensity_thresh)

            # Writes camera to Jetson if we press button on dashboard, or if number of frames to capture is specified on dashboard
            if self.capture_entry.getBoolean(False) or self.imgs_to_capture.getNumber(0) >= 1:
                # Sets capture entry back to false so we don't run again
                self.capture_entry.setBoolean(False)

                mills = str(int(time.time() * 1000))
                dist = self.distance_entry.getString('42-thousand-tonnes')
                fname = str('/home/lightning/voidvision/images/frame-distance-{}-{}.png'.format(dist, mills))
                cv2.imwrite(fname, self.img)
                print('FILE: {} WRITTEN'.format(fname))
                if self.imgs_to_capture.getNumber(0) >= 1:
                    self.imgs_to_cap = self.imgs_to_capture.getNumber(0)
                    self.imgs_to_cap -= 1
                    self.imgs_to_capture.setNumber(self.imgs_to_cap)

    def init_debug(self):
        """
        Variables to be initialized for debug mode only 
        """
        self.exposure_entry = self.table.getEntry('exposure')
        self.brightness_entry = self.table.getEntry('brightness')
        self.capture_entry = self.table.getEntry('capture frame')
        self.distance_entry = self.table.getEntry('distance input')
        self.intensity_thresh_entry = self.table.getEntry('Intensity Threshold')
        self.imgs_to_capture = self.table.getEntry('Images to capture')

        # Initialize network table entries
        self.capture_entry.setBoolean(False)
        self.distance_entry.setString('42-thousand-tonnes')
        self.exposure_entry.setNumber(self.exposure)
        self.brightness_entry.setNumber(self.brightness)
        self.intensity_thresh_entry.setNumber(self.intensity_thresh)
        self.imgs_to_capture.setNumber(0)
        # self.green_lower_threshold.setNumber(100) # 100 is default for now
        os.system("v4l2-ctl --device " + self.cameraPath +  " --set-ctrl=exposure_auto_priority=0")