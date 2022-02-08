#!/usr/bin/env python3

import importlib
import json
from pipeline import VisionPipeline

def loadall(config: str, table):

	# list of pipelines
	piperunners = []

	# read pipelines from config file
	with open(config) as cfg:
		config = json.load(cfg)
	pipes = config['pipelines']

	# initialize and load each pipeline
	for pipe in pipes:
		print(pipe)
		piperunner = load(config, pipe, table)
		piperunners.append(piperunner)
		
	return pipes

def load(config: str, pipe, table) -> VisionPipeline:

	# read json config for pipeline
	name = pipe['name']
	fname = pipe['fname']
	camera = pipe['camera']
	cam_name = pipe['cameraname']

	# dynamically import/load pipeline
	module = importlib.import_module('pipelines.'+fname)
	class_ = getattr(module, name)
	instance = class_(config, camera, cam_name, (name + '_output'))

	# return instance
	return instance
