#!/usr/bin/env python3
import os
from cscore import CameraServer, UsbCamera
from pipelinecfg import CameraConfig
import json

def start(config_file: str, cam_num: int, cam_name: str, output_name: str):

	with open(config_file) as cfg:
		config = json.load(cfg)
		debug = config['debug']
	camera = config['cameras'][cam_num]
	print(camera)

	cfg = CameraConfig(camera)

	cs = CameraServer.getInstance()

	# Test making camera
	cam = UsbCamera(dev=cam_num, name=cam_name)
	cam.setFPS(cfg.getFPS())

	# Set Camera Stats & Start Capture
	cam.setResolution(cfg.getWidth(), cfg.getHeight())
	cs.startAutomaticCapture(camera=cam, return_server=True)
	
	# Get Input/Output
	inp = cs.getVideo(name=cam_name) # Returns `CvSink`
	out = cs.putVideo(name=output_name, width=cfg.getWidth(), height=cfg.getHeight())

	return inp, out, cam, debug, cfg

if __name__ == "__main__":
	print('do not run this script\nsomething is wrong')
