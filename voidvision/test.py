# import time
# import cv2
# from networktables import NetworkTablesInstance
# import numpy as np
# import cscore
# camera = cscore.VideoSource(0)
# cscore.CameraServer.addCamera(camera)
# cscore.CameraServer.addServer("camera1", 862)

from cscore import CameraServer

import cv2
import numpy as np

# vid = cv2.VideoCapture(0)
cs = CameraServer.getInstance()
# cs.addCamera("/dev/video0")
cs.enableLogging()
# UsbCamera camera = new UsbCamera(config.name, config.path);
# MjpegServer server = inst.startAutomaticCapture(camera);

print(cs)    
# Capture from the first USB Camera on the system
camera = cs.startAutomaticCapture("camera", 0)
camera.setResolution(320, 240)
# Get a CvSink. This will capture images from the camera
cvSink = cs.getVideo()
# (optional) Setup a CvSource. This will send images back to the Dashboard
outputStream = cs.putVideo("Name", 320, 240)

# Allocating new images is very expensive, always try to preallocate
img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)
time, img = cvSink.grabFrame(img)
print(time)
"""
i = 0
while i < 10:
    i += 1
    time, img = cvSink.grabFrame(img)
    if time == 0:
        # Send the output the error.
        outputStream.notifyError(cvSink.getError());
        continue
    outputStream.putFrame(img)
    """
