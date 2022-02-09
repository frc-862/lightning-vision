#!/usr/bin/env python3

from cscore import CameraServer
from networktables import NetworkTablesInstance, NetworkTables
from threading import Thread
from time import sleep
from pipeline import VisionPipeline

import cv2
import json
import time
import numpy as np

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

	# start threads
	for pipe in pipes:
		thread = Thread(target=vision_thread, args=(pipe[1],table,pipe[0],))
		thread.start()

	print('APPLICATION STARTED SUCCESSFULLY')
	
	while True:
		sleep(10)

def vision_thread(pipe: VisionPipeline, table, pipe_name: str) -> None:

	while True:
		start_time = time.time()
		pipe.process()
		processing_time = time.time() - start_time
		fps = 1 / processing_time
		table.putNumber('FPS_'+pipe_name, fps)

if __name__ == "__main__":
	main()
