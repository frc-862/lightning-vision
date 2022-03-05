import cv2
from greenLedPipeline import GripPipeline as pipe
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os

#my_gp = pipe()

# names the video window preview
cv2.namedWindow("preview")

#starts the video capture
vc = cv2.VideoCapture(0)

#sets the exposure
vc.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
exposure = -12
vc.set(cv2.CAP_PROP_EXPOSURE, exposure)

#sets the width and height
vc.set(cv2.CAP_PROP_FRAME_WIDTH,640)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

# Frame rate.
vc.set(cv2.CAP_PROP_FPS,60)

# Brightness of the image (only for cameras).
vc.set(cv2.CAP_PROP_BRIGHTNESS,144)

# Contrast of the image (only for cameras).
vc.set(cv2.CAP_PROP_CONTRAST,27)

# Saturation of the image (only for cameras).
vc.set(cv2.CAP_PROP_SATURATION,255)

# Hue of the image (only for cameras).
vc.set(cv2.CAP_PROP_HUE,0)


print(vc.get(cv2.CAP_PROP_EXPOSURE))


if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False


collect_image_debug = True


while rval:
    rval, frame = vc.read()
    cv2.imshow("preview", frame)
    key = cv2.waitKey(100)
    if key == 27: # exit on ESC
        break
    
    if (collect_image_debug):
        key = input("Press c to collect image, enter to continue: ")

        if key == 'c':
            #grab current image
            rval, frame = vc.read()
    
            # counter to use to make unique file name
            counter = 0
            # set up to loop until we write a file
            done = False
            # LOOP!
            while not(done):
                print("you saved a picture")
    
                # Make a temp file name to see if it exists
                imagePath = r'C:\Users\sdtul\DataV4'
                imageName = 'debug'+str(counter)+'_exposure'+str(exposure)+'.png'
                tempfilename = os.path.join(imagePath,imageName)
                # Check if this is an unused file name
                if not (os.path.exists(tempfilename)):
                    # If it is unused, write the image in this name and exit loop
                    cv2.imwrite(tempfilename,frame)
                    print("capture")
                    done = True
                
                else:
                    # Increment counter to try to get the next sequential n ame to try
                    counter += 1
                    
                
    plt.figure(1)
    plt.clf()
    imgplot = plt.imshow(frame)
    plt.title("video")
    plt.draw()
    plt.show()
    plt.pause(0.01)
    #value = plt.ginput(1,timeout=0)

    #value = my_gp.process(frame)

vc.release()
cv2.destroyWindow("preview")