#!/usr/bin/env python3

from pipeline import VisionPipeline
import camera
import numpy as np
import cv2
import sys
# TODO import grip pipeline


class HubPipeline(VisionPipeline):

	def __init__(self, config: str, cam_num: int, cam_name: str, output_name: str, table) -> None:

		self.nttable = table

		# TODO instantiate GRIP pipeline

		# one camera thing
		self.inp, self.out, self.width, self.height = camera.start(config, cam_num, cam_name, output_name)

		# allocate image for whenever
		self.img = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)
		self.output_img = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)

	def process(self):

		# get frame from camera
		self.t, self.img = self.inp.grabFrame(self.img)

		# TODO pass self.img to grip pipeline process function

		# TODO grab center of bounding box around target from grip pipeline
		#row, col = grip.getBlahBlahBlah()

		# TODO do some math to correspond the column to an angle offset
		targetAngle = 0 # TODO fixme

		# TODO do some more math to correspond row to distance (interpolation table?)
		distance = 0 # TODO fixme

		self.nttable.putNumber('Distance', distance)
		self.nttable.putNumber('Target Angle', targetAngle)

		# throw output image to dashboard
		#self.out.putFrame(self.output_img)
