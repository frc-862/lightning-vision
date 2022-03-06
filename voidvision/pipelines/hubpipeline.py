#!/usr/bin/env python3

from pipeline import VisionPipeline
import camera
import time
import cv2
import os
import numpy as np
from filterimage import findCentroid, estimate_target_angle, estimate_target_distance

class HubPipeline(VisionPipeline):

	def __init__(self, config: str, cam_num: int, cam_name: str, output_name: str, table) -> None:

		# Define Camera Constants
		self.hfov = 100.0 # degrees
		self.vfov = 68.12 # degrees

		# Network Table
		self.nttable = table
		
		# Start Camera
		self.inp, self.out, self.cam, self.debug, self.cfg = camera.start(config, cam_num, cam_name, output_name)

		# Set Camera Settings
		os.system("v4l2-ctl --device " + self.cfg.getCameraPath() + " --set-ctrl=exposure_absolute=" + str(self.cfg.getExposure()))	
		os.system("v4l2-ctl --device " + self.cfg.getCameraPath() + " --set-ctrl=brightness=" + str(self.cfg.getBrightness()))

		# Initialize Debug/Tune Mode
		if self.debug:
			self.initDebug()

		# Vision HSV Threshold Limits
		self.lower_green = np.array([50.179, 89.433, 34.397])
		self.high_green = np.array([83.03, 255, 255])
	   
		self.target_distance_entry = table.getEntry('Target Distance')
		self.target_angle_entry = table.getEntry('Target Angle')
		self.target_distance_entry.setNumber(-1)
		self.target_angle_entry.setNumber(0)

		# Allocate Images
		self.img = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)
		self.output_img = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)

	def process(self):

		# Run Tuning Updates
		if self.debug:
			self.processDebug()

		# Read Frame
		self.t, self.img = self.inp.grabFrame(self.img)
		
		# Find Centroid
		row, col = findCentroid(self.img)

		# Extrapolate Distance From Centroid
		targetDistance = estimate_target_distance(row, self.cfg.getHeight())
		targetAngle =  estimate_target_angle(col, self.hfov, self.cfg.getWidth())

		# Route Numbers to Dashboard
		self.target_distance_entry.setDouble(targetDistance)
		self.target_angle_entry.setDouble(targetAngle)

	def initDebug(self):
		"""
		Initialize dashboard entries
		"""

		# HSV Thresholds
		self.h_low = self.nttable.getEntry('H LOW')
		self.s_low = self.nttable.getEntry('S LOW')
		self.v_low = self.nttable.getEntry('V LOW')
		self.h_high = self.nttable.getEntry('H HIGH')
		self.s_high = self.nttable.getEntry('S HIGH')
		self.v_high = self.nttable.getEntry('V HIGH')

		self.h_low.setDouble(50.179)
		self.s_low.setDouble(89.433)
		self.v_low.setDouble(34.397)
		self.h_high.setDouble(83.03)
		self.s_high.setDouble(255)
		self.v_high.setDouble(255)

		# Camera Settings
		self.exposure_entry = self.nttable.getEntry('Exposure')
		self.brightness_entry = self.nttable.getEntry('Brightness')
		self.capture_entry = self.nttable.getEntry('Capture Frame')
		self.distance_entry = self.nttable.getEntry('Distance Input')
    
		self.capture_entry.setBoolean(False)
		self.distance_entry.setString('42-thousand-tonnes')
		self.exposure_entry.setNumber(self.cfg.getExposure())
		self.brightness_entry.setNumber(self.cfg.getBrightness())

	def processDebug(self):
		"""
		Update tunable items
		"""

		# Update Thresholds From Dash
		self.lower_green = np.array([self.h_low.getDouble(50.179), self.s_low.getDouble(89.433), self.v_low.getDouble(34.397)])
		self.high_green = np.array([self.h_high.setDouble(83.03), self.s_high.setDouble(255), self.v_high.setDouble(255)])

		# Button To Collect Data if Needed
		if self.capture_entry.getBoolean(False):
				mills = str(int(time.time() * 1000))
				dist = self.distance_entry.getString('42-thousand-tonnes')
				fname = str('/home/lightning/voidvision/images/frame-distance-{}-{}.png'.format(dist, mills))
				cv2.imwrite(fname, self.img)
				print('FILE: {} WRITTEN'.format(fname))
				self.capture_entry.setBoolean(False)

		# Sync Camera Settings From Dash
		os.system("v4l2-ctl --device " + self.cfg.getCameraPath() + " --set-ctrl=exposure_absolute=" + str(self.exposure_entry.getNumber(self.exposure)))	
		os.system("v4l2-ctl --device " + self.cfg.getCameraPath() + " --set-ctrl=brightness=" + str(self.brightness_entry.getNumber(self.brightness)))
