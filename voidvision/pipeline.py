#!/usr/bin/env python3

from abc import ABC, abstractmethod

class VisionPipeline(ABC):

	@abstractmethod
	def __init__(self, config: str, cam_num: int, cam_name: str, output_name: str, table) -> None:
		pass
	
	@abstractmethod
	def process(self):
		pass

if __name__ == "__main__":
	print('do not run this script\nsomething is wrong')
