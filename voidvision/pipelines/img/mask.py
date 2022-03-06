import cv2
import glob
import numpy as np

def process(img):
    lower_green = np.array([50.179, 89.433, 34.397])
    higher_green = np.array([83.03, 255, 255])
    mask = cv2.inRange(img, lower_green, higher_green)
    return img

source = "C:/Users/Bob/Pictures/Void_342022_data/png/exposure7_brightness1"
for img in glob.glob(source + "/*.png"):
    img = cv2.imread(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    img = process(img)
    cv2.imshow("raw img", img)
    cv2.waitKey(0)