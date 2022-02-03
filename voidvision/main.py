#!/usr/bin/env python3

from cscore import CameraServer
from networktables import NetworkTablesInstance, NetworkTables

import cv2
import json
import numpy as np
import time

import cameraserver
import dashboard

configFile = "/home/lightning/voidvision/camera-config.json"

def main():
	
	# one camera thing
	inp, out, width, height = cameraserver.start(configFile, 0, 'cam', 'output?')

	# start dashboard
	table = dashboard.load(configFile)

	# allocate image for whenever
	img = np.zeros(shape=(height, width, 3), dtype=np.uint8)

	i = 0
	while True:
		start_time = time.time()

		table.putNumber('Loop Number', i)
		i += 1

		t, img = inp.grabFrame(img)

		# process image
		output_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		processing_time = time.time() - start_time
		fps = 1 / processing_time
		table.putNumber('FPS', fps)

		out.putFrame(output_img)

if __name__ == "__main__":
	main()
