#!/usr/bin/env python3

from voidvision.pipeline import VisionPipeline
import numpy as np
import cv2


class TestPipeline(VisionPipeline):

	def __init__(self, config: str, camera: int, cam_name: str, output_name: str) -> None:

		# one camera thing
		self.inp, self.out, self.width, self.height = camera.start(config, camera, cam_name, output_name)

		# allocate image for whenever
		self.img = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)
		self.output_img = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)

	def process(self):

		# get frame from camera
		self.t, self.img = self.inp.grabFrame(self.img)

		# process image
		self.output_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)

		self.out.putFrame(self.output_img)

