import glob
import cv2
import numpy as np

def threshold(img):
    hue_lower_upper = [50.17985611510791, 83.03030303030302]
    saturation_lower_upper = [89.43345323741008, 255.0]
    value_lower_upper = [34.39748201438849, 255.0]
    
    lower_green = np.array([50.179, 89.433, 34.397])
    high_green = np.array([83.03, 255, 255])
    img = cv2.inRange(img, lower_green, high_green)
    return img

def process(img):
        if self.debug:
            os.system("v4l2-ctl --device " + self.cameraPath + " --set-ctrl=exposure_absolute=" + str(self.exposure_entry.getNumber(self.exposure)))	
            os.system("v4l2-ctl --device " + self.cameraPath + " --set-ctrl=brightness=" + str(self.brightness_entry.getNumber(self.brightness)))
            self.intensity_thresh = self.intensity_thresh_entry.getNumber(self.intensity_thresh)

        # get frame from camera
        self.t, self.img = self.inp.grabFrame(self.img)

        # Debugging installed to allow us to capture raw images from robot camera
        if self.debug:
            if self.capture_entry.getBoolean(False):
                mills = str(int(time.time() * 1000))
                dist = self.distance_entry.getString('42-thousand-tonnes')
                fname = str('/home/lightning/voidvision/images/frame-distance-{}-{}.png'.format(dist, mills))
                cv2.imwrite(fname, self.img)
                print('FILE: {} WRITTEN'.format(fname))
                self.capture_entry.setBoolean(False)
    # self.t, self.img = self.inp.grabFrame(self.img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img = threshold(img)
    img = cv2.erode(img, None, (-1, -1), iterations = 1, borderType = cv2.BORDER_CONSTANT, borderValue = -1)
    img = cv2.dilate(img, None, (-1,-1), iterations = 1,borderType = cv2.BORDER_CONSTANT, borderValue = -1)
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    maxPt = [-np.inf, -np.inf]
    minPt = [np.inf, np.inf]
    
    for c in contours:
        maxc = np.max(c, axis = 0)[0]
        minc = np.min(c, axis = 0)[0]
        
        if maxPt[0] < maxc[0]:
            maxPt[0] = maxc[0]
                        
        if maxPt[1] < maxc[1]:
            maxPt[1] = maxc[1]
                        
        if minPt[0] > minc[0]:
            minPt[0] = minc[0]
                        
        if minPt[1] > minc[1]:
            minPt[1] = minc[1]
                  
    y = (maxPt[0] + minPt[0]) / 2
    x = (maxPt[1] + minPt[1]) / 2
    
    return img   
    
source = "C:/Users/lukas/Desktop/20220304/png/exposure7_brightness1"
for f in glob.glob(source + "/*.png"):
    img = cv2.imread(f)
    img = process(img)
    cv2.imshow("Test", img)
    cv2.waitKey(3)

    