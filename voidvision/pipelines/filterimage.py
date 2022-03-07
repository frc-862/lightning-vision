#!/usr/bin/env python3

import cv2
import numpy as np

def threshold(img, thresh_green_low, thresh_green_high):
	# HSV Color
	img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# Threshold
	img = cv2.inRange(img, thresh_green_low, thresh_green_high)

	# Remove Small Things
	img = cv2.erode(img, None, (-1, -1), iterations = 1, borderType = cv2.BORDER_CONSTANT, borderValue = -1)
	img = cv2.dilate(img, None, (-1,-1), iterations = 1,borderType = cv2.BORDER_CONSTANT, borderValue = -1)
	
	return img

def findCentroid(img):
	"""
	Returns row, col of centroid of target
	"""
	# Fly Through Contours
	contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	# Find Corners of Contours
	maxPt = [-np.inf, -np.inf]
	minPt = [np.inf, np.inf]

	for c in contours:
		maxc = np.max(c, axis = 0)[0]
		minc = np.min(c, axis = 0)[0]
		# Max Point
		if maxPt[0] < maxc[0]:
			maxPt[0] = maxc[0]
		if maxPt[1] < maxc[1]:
			maxPt[1] = maxc[1]
		# Min Point
		if minPt[0] > minc[0]:
			minPt[0] = minc[0]
		if minPt[1] > minc[1]:
			minPt[1] = minc[1]

	# Find Higher Centerpoint
	row = (maxPt[0] + minPt[0]) / 2
	col = (maxPt[1] + minPt[1]) / 2

	return row, col

def estimate_target_distance(row, height):
	"""
	Estimate distance based on regression from test data
	"""
	Pyx2 = np.array([719.87601135, -3905.32210081,  5362.87630488])
	estimate_distance = np.polyval(Pyx2,np.log10(height-row))
	return estimate_distance

def estimate_target_angle(col, hfov, width):
	"""
	Estimate angle based on camera info
	"""
	estimate_angle = (hfov/width) * (col-width/2)
	return estimate_angle
