import cscore
import cv2
import numpy as np


width = 1920
height = 1080
cscore.CameraServer.enableLogging()
cam = cscore.UsbCamera("lol", "/dev/video0")
inst = cscore.CameraServer.getInstance()
camera = inst.startAutomaticCapture(camera=cam, return_server=True)
camera.setResolution(width, height)



