import matplotlib.image as mpimg
import numpy as np
import os
import matplotlib.pyplot as plt
from greenLedPipeline import GripPipeline as pipe
import cv2

Video_debug = True

my_gp = pipe()

basedir = r'"C:\Users\sdtul\Grip_stuffv2\5foot"'

i = 0
for r, d, f in os.walk(basedir):
    for file in f:
        if file.endswith("12.png"): 
            i = i + 1
            print(file)

            im = mpimg.imread(os.path.join(r,file))
            # converting mattplot lib 0-1 values to expected 0-255 values
            newIm = np.round(np.multiply(255,im))
            
            value = my_gp.process(newIm) 
          
            if Video_debug :

                plt.figure(1)
                plt.clf()
                plt.imshow(im)
                
                plt.draw()
                plt.show()
                print("click in figure 1 to continue")
                plt.ginput(1, timeout = 0)
  

    
                

