#!/usr/bin/

import cv2
import os
import numpy as np
from filterimage import FilterImage
import glob
import matplotlib.pyplot as plt
import pathlib

thresh_lower_green = np.array([50.179, 89.433, 34.397])
thresh_high_green = np.array([83.03, 255, 255])
width = 640.0
height = 480.0
hfov = 99.0
vfov = 68.12

def main():
    # Gets path we're running this from, assumes images are in img dir
    path = str(pathlib.Path(__file__).parent.absolute()) + "/img/"

    # Init class for image filtering
    filterImage = FilterImage()

    # Init empty lists
    estimated_distances = []
    estimated_angles = []
    real_angles = []
    real_distances = []

    for file_name in os.listdir(path):
        if file_name.endswith('.png'):
        



            # Read image, run processing pipeline on it to get estimated distance and angle
            img = cv2.imread(path + file_name)

            # Return binary image based on HSV threshold
            masked_img = filterImage.color_mask(img, thresh_lower_green, thresh_high_green)

            # Dilates and erodes image
            filtered_img = filterImage.filter_noise(masked_img)

            # Create list of contours and then process checks to see if they're the target
            est_dist, est_angle = filterImage.processContours(filtered_img)
            if est_dist == -1 and est_angle == 0:
                os.rename(path + file_name, path + "no_target/" + file_name)



            # Add estimated values and true values to lists
            estimated_distances.append(est_dist)
            estimated_angles.append(est_angle)
            print('FILE: {} | EST-DIST: {} | EST-ANG: {}'.format(file_name, est_dist, est_angle))
        

# TODO: Find a more useful way to visualize data beyond scatter plots of estimated values in relation to real
"""
def plot(real_angle, est_angle, real_dist, est_dist):
    plt.subplot(211)
    plt.xlabel("Real Distance (ft)")
    plt.ylabel("Estimated Distance (ft)")
    plt.scatter(real_dist, est_dist)
    plt.subplot(212)
    plt.xlabel("Estimated Angle (degrees)")
    plt.ylabel("Real Angle (degrees)")
    plt.scatter(est_angle, real_angle)
    plt.show()
"""

if __name__ == "__main__":
    main()
