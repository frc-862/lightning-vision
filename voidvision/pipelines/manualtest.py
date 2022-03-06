#!/usr/bin/

import cv2
import os
import numpy as np
from filterimage import findCentroid, estimate_target_angle, estimate_target_distance
import glob
import matplotlib.pyplot as plt
import pathlib


thresh_lower_green = np.array([50.179, 89.433, 34.397])
thresh_high_green = np.array([83.03, 255, 255])
width = 640
height = 480
hfov = 100
vfov = 68.12

def main():
	# Gets path we're running this from, assumes images are in img dir
	path = str(pathlib.Path(__file__).parent.absolute()) + "\img"

	# Init empty lists
	estimated_distances = []
	estimated_angles = []
	real_angles = []
	real_distances = []

	for file_name in glob.glob(path + "/*.png"):
		if file_name.endswith('.png'):
			# Parse file name to get real values
			# TODO: make parsing work with pos/neg angle files, not just 0
			split_file_name = file_name.split("-")
			real_distance = split_file_name[3]
			real_distance = real_distance.replace('ft', '')
			real_distance = float(real_distance)
			real_angle = split_file_name[5]
			real_angle = float(real_angle)

			# Read image, run processing pipeline on it to get estimated distance and angle
			img = cv2.imread(file_name)
			row, col = findCentroid(img, thresh_lower_green, thresh_high_green)
			est_dist = estimate_target_distance(row, height)
			est_dist = est_dist / 12  # Output is in inches, truth is in feet so we convert
			est_angle = estimate_target_angle(col, hfov, width)

			# Add estimated values and true values to lists
			estimated_distances.append(est_dist)
			estimated_angles.append(est_angle)
			real_angles.append(real_angle)
			real_distances.append(real_distance)
			print('FILE: {} | EST-DIST: {} | EST-ANG: {}'.format(file_name, est_dist, est_angle))
		
	plot(real_angles, estimated_angles, real_distances, estimated_distances)

def plot(real_angle, est_angle, real_dist, est_dist):
	plt.subplot(211)
	plt.xlabel("Real Distance")
	plt.ylabel("Estimated Distance")
	plt.scatter(real_dist, est_dist)
	plt.subplot(212)
	plt.xlabel("Estimated Angle")
	plt.ylabel("Real Angle")
	plt.scatter(est_angle, real_angle)
	plt.show()


if __name__ == "__main__":
	main()
