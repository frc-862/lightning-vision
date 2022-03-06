#!/usr/bin/

import cv2
import os
import numpy as np
from filterimage import findCentroid, estimate_target_angle, estimate_target_distance

thresh_lower_green = np.array([50.179, 89.433, 34.397])
thresh_high_green = np.array([83.03, 255, 255])
width = 640
height = 480
hfov = 100
vfov = 68.12

def main():

	for fname in os.listdir('./img/'):
		if fname.endswith('.png'):

			img = cv2.imread(fname)
			row, col = findCentroid(img, thresh_lower_green, thresh_high_green)
			est_dist = estimate_target_distance(row, height)
			est_angle = estimate_target_angle(col, hfov, width)

			print('FILE: {} | EST-DIST: {} | EST-ANG: {}'.format(fname, est_dist, est_angle))

if __name__ == "__main__":
	main()
