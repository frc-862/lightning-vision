#!/usr/bin/env python3

from re import I
from pipeline import VisionPipeline
import camera
import numpy as np
import cv2
import sys
from time import sleep
import grip


class HubPipeline(VisionPipeline):

	def __init__(self, config: str, cam_num: int, cam_name: str, output_name: str, table) -> None:

		self.nttable = table

		self.pipeline = grip.GripPipeline()

		self.fov_horiz = 0 # TODO Measure horizontal fov on cameras
		self.fov_vert = 0 # TODO Measure vertical fov on cameras

		# start camera
		self.inp, self.out, self.width, self.height = camera.start(config, cam_num, cam_name, output_name)

		self.targetHeightRatio = 0
		self.targetRatioThreshold = 0

		# allocate image for whenever
		self.img = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)
		self.output_img = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)

	def process(self):

		# get frame from camera
		self.t, self.img = self.inp.grabFrame(self.img)

		self.pipeline.process(self.img)

		# TODO grab center of bounding box arounuuud target from grip pipeline
		#row, col = grip.getBlahBlahBlah()

		self.output_img = self.pipeline.rgb_threshold_output
		self.out.putFrame(self.output_img)

		# TODO do some math to correspond the column to an angle offset based on these vars
		targetAngle = 0 # TODO fixme
		centerCol = 0 # Center column of target
		imgWidthCols = 0 # Center Row of target


		# TODO do some more math to correspond row to distance (interpolation table?)
		distance = 3 # TODO fixme

		targetCenterCol = 0 # Should hold the center height of target
		imgWidthCols = 0 # Should hold width of target in columns

		# targetAngle = get_angle_from_target(targetCenterCol, imgWidthCols)
		targetAngle = 15 
		self.nttable.putNumber('Target Angle', targetAngle)
		self.nttable.putNumber('Target Distance', distance)
		try: 
			numContours = len(self.pipeline.filter_contours_output)
		except:
			numContours = -1

		# Puts number of contours detected in current image to the dashboard
		self.nttable.putNumber('Contour Number', numContours)

		# throw output image to dashboard
		self.out.putFrame(self.output_img)

	def get_angle_from_target(self, target_center_col, image_width_cols):
			return (target_center_col - (image_width_cols / 2) * (self.fov_horiz / image_width_cols))
		
	def interpolated_dist_from_target(self):
			pass

	def checkTargetProportion(self, targetBoxHeight, targetCenterRow):
			ratio = targetBoxHeight / targetCenterRow
			return (ratio - self.targetHeightRatio) < self.targetRatioThreshold