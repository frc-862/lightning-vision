#!/usr/bin/env python3

from abc import ABC, abstractmethod

class VisionPipeline(ABC):

	@abstractmethod
	def __init__(self, config: str, camera: int, cam_name: str, output_name: str) -> None:
		pass
	
	@abstractmethod
	def process(self):
		pass
