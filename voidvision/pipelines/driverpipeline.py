#!/usr/bin/env python3

from pipeline import VisionPipeline
import camera
import numpy as np
import cv2
import sys


class DriverPipeline(VisionPipeline):

	def __init__(self, config: str, cam_num: int, cam_name: str, output_name: str, table) -> None:

		# one camera thing
		self.inp, self.out, self.width, self.height, self.cam, self.exposure, self.brightness, self.cameraPath = camera.start(config, cam_num, cam_name, output_name)

		# allocate image for whenever
		self.img = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)


	def process(self):
		# get frame from camera
		self.t, self.img = self.inp.grabFrame(self.img)
		return
	    # throw output image to dashboard
		# self.out.putFrame(self.img)
