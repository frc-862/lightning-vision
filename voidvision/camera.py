#!/usr/bin/env python3

from cscore import CameraServer
import json

def start(configFile: str, cam_num: int, cam_name: str, output_name: str):

	with open(configFile) as cfg:
		config = json.load(cfg)
	camera = config['cameras'][cam_num]
	print(camera)

	width = camera['width']
	height = camera['height']
	
	cs = CameraServer.getInstance()
	cap = cs.startAutomaticCapture(dev=cam_num, name=cam_name) # Returns `VideoSource`
	cap.setFPS(camera['fps'])

	inp = cs.getVideo(name=cam_name) # Returns `CvSink`
	out = cs.putVideo(name=output_name, width=width, height=height)

	return inp, out, width, height

if __name__ == "__main__":
	print('do not run this script\nsomething is wrong')
