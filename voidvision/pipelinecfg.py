#!/usr/bin/env python3

class CameraConfig:

	def __init__(self, cameracfg) -> None:
		self.cfg = cameracfg

	def getWidth(self):
		return self.cfg['width']

	def getHeight(self):
		return self.cfg['height']

	def getCameraPath(self):
		return self.cfg['path']

	def getExposure(self):
		return self.cfg['exposure']

	def getBrightness(self):
		return self.cfg['brightness']

	def getFPS(self):
		return self.cfg['fps']
		