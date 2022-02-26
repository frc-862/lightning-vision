import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os


# Initialize camera and get ready to collect images
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)


# Finalize initialization - open the camera object
if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False
    
# set camera settings now that camera coms is open
vc.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
exposure = -13
vc.set(cv2.CAP_PROP_EXPOSURE, exposure)
print(vc.get(cv2.CAP_PROP_EXPOSURE))


# Loop until done/exit
while rval:
    # Grab the current frame
    cv2.imshow("preview"+" exposure "+str(exposure), frame)
    cv2.waitKey(1)
    
    # Check for a key hit
    #key = cv2.waitKey(1000)
    
    key = input("Press p or m: ")
    
    if key == 27 or key == 'q' : # exit on ESC or 'q' (quit)
        break
    elif key == 'p':
        # Use 'p' key as "plus" to add to exposure
        exposure = np.min([0,exposure+1])
        vc.set(cv2.CAP_PROP_EXPOSURE, exposure)

    elif key == 'm':
        # Use 'm' key as "minus" to subtract from exposure
        exposure = np.max([-20,exposure-1])
        vc.set(cv2.CAP_PROP_EXPOSURE, exposure)
    elif key == 'c':
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
            imagePath = r'C:\Users\sdtul\DataV2'
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
                
        
    print(" exposure "+str(exposure))


vc.release()
cv2.destroyWindow("preview")

