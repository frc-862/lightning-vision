#!/usr/bin/env python3

from cscore import CameraServer
from networktables import NetworkTablesInstance, NetworkTables

import cv2
import json
import numpy as np
import time

import camera
import dashboard
import pipelineloader

config = "/home/lightning/voidvision/vision-config.json"

def main():

	# start dashboard
	table = dashboard.load(config)

	# start pipelines
	pipes = pipelineloader.loadall(config, table)

	# push number of pipelines to dashboard
	table.putNumber('# Pipelines', len(pipes))

	i = 0
	while True:
		start_time = time.time()

		for pipe in pipes:
			pipe.process()

		processing_time = time.time() - start_time
		fps = 1 / processing_time
		table.putNumber('FPS', fps)

if __name__ == "__main__":
	main()
