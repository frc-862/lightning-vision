#!/usr/bin/env python3

import cv2
import numpy as np
import json

class FilterImage():
	def __init__(self):
		self.hfov = 99
		self.vfov = 68.12

	def color_mask(self, img, thresh_green_low, thresh_green_high):
		"""
		Applies a color threshold and gives a binary img out	
		"""
		# HSV Color
		img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	
		# Threshold
		img = cv2.inRange(img, thresh_green_low, thresh_green_high)
	
		# Remove Small Things
		img = cv2.erode(img, None, (-1, -1), iterations = 1, borderType = cv2.BORDER_CONSTANT, borderValue = -1)
		img = cv2.dilate(img, None, (-1,-1), iterations = 1,borderType = cv2.BORDER_CONSTANT, borderValue = -1)
		
		return img

	def estimate_tape_width(self, row, col):
		"""
		Estimates width of tape based on corner points, I think?
		TODO: Figure out what this does	
		"""
		point1 = [38,26]
		#point2 = [310,4]
		point2=[340,5]
	
		estimate_width = ((point2[1]-point1[1])/(point2[0]-point1[0]))*row \
						+ (point1[1]-((point2[1]-point1[1])/(point2[0]-point1[0]))*point1[0])
		estimate_wtolerance = 1.1*((-5.0/480.0)*row+6.6)
	
		return estimate_width, estimate_wtolerance
	
	def estimate_tape_height(self, row, col):
		"""
		Estimates height of tape based on corner points, I think?	
		TODO: Figure out what this does
		"""
	
		point1 = [37,7]
		point2 = [312,2]
	
		estimate_height = ((point2[1]-point1[1])/(point2[0]-point1[0]))*row \
						+ (point1[1]-((point2[1]-point1[1])/(point2[0]-point1[0]))*point1[0])
		estimate_htolerance = 0.6*((-5.0/480.0)*row+6.6)
	
		return estimate_height, estimate_htolerance
	
	def findCentroid(self, img):
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

	def filter_noise(self, color_mask):
		"""
		Dilates and erodes a binary mask to get an output of more solid contours	
		"""
		kernel = np.ones((5,5), np.uint8)
		# 'round' the kernel a little
		kernel[0][0] = 0
		kernel[4][0] = 0
		kernel[0][4] = 0
		kernel[4][4] = 0
		# Use the kernel to clean holes in blobs and smooth shape edges
		im_dilate = cv2.dilate(color_mask,kernel,iterations=1)
		im_erode = cv2.erode(im_dilate,kernel,iterations=1)
		return im_erode


	#==================================
	# CONTOUR FILTERING
	#==================================

	def processContours(self, img):
		contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
			
		#========================================================
		# ADD A SANITY CHECK
		#    If there are an insane number of contours - bail!!!!!!
		#========================================================
		max_expected_contours = 30
		if (len(contours)>max_expected_contours):
			print("WARNING - TOO MANY CONTOURS ("+str(len(contours))+" VERSUS "+str(max_expected_contours)+")")
		
		# EXAMINE THE POSSIBILITIES FOR CONTOUR PROCESSING:
		# https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html
			

		# !!!DEBUG VARIABLES THAT REQUIRE TRUTH BOXES/CONTOURS!!!
		match_truth_not_size = []
		match_size_not_truth = []

	
		# First pass through the contours checking for a valid size of the best-fit rectangle
		pass_size_contours = []                
		# Loop over all the contours in this image
		for this_contour in contours:
			
			#-------------------------------------------------------
			# Get the minimized bounding rectangle on the contour
			rect = cv2.minAreaRect(this_contour)
			# (x,y), (width,height), orientation
			# https://theailearner.com/tag/cv2-minarearect/
			# Note:  corners are always counter from the largest row corner clockwise
			# Note:  rotation is always between [-90,0) - may be hard to use...
			# For now, just assume the biggest measure is width and smallest is height
			contour_width = np.max(rect[1])
			contour_height = np.min(rect[1])
			
			#-------------------------------------------------------
			# NOTICE - SIZE CHECK - Use bounds around a fit to determine acceptable sizing
			estimate_width, estimate_wtolerance = self.estimate_tape_width(rect[0][1],rect[0][0])
			estimate_height, estimate_htolerance = self.estimate_tape_height(rect[0][1],rect[0][0])
			#print([contour_width,contour_height,estimate_width,estimate_wtolerance,estimate_height,estimate_htolerance])
			
			# Check to see if the width and height meet our expectations
			match_size = False
			if ( (contour_width>=estimate_width-estimate_wtolerance) \
					and (contour_width<=estimate_width+estimate_wtolerance) \
					and (contour_height>=estimate_height-estimate_htolerance) \
					and (contour_height<=estimate_height+estimate_htolerance) ):
				match_size = True
				pass_size_contours.append(this_contour)
			else:
				# Add debug to explore failing this check
				foo = 0 # Useless line as placeholder for indentation
	
		#========================================================
		# ADD A SANITY CHECK
		#    If there are an insane number of contours - bail!!!!!!
		#========================================================
		max_expected_size_contours = 10
		if (len(pass_size_contours)>max_expected_size_contours):
			print("WARNING - TOO MANY SIZE CONTOURS ("+str(len(pass_size_contours))+" VERSUS "+str(max_expected_size_contours)+")")
		
		#============================================================
		# Add a check looking for nearby contours that also pass size check!!!
		#   this should help screen false alarms
		# FIX ME - decide what to do if there is only 1 remaining contour:  believe it or pass
		used = [0]*len(pass_size_contours)
		next_group = 1
		for index in range(len(pass_size_contours)):
			#print("Processing contour number "+str(index)+" of "+str(len(pass_size_contours)))
			this_contour = pass_size_contours[index]
			this_center = np.array(cv2.minAreaRect(this_contour)[0])
			#print(this_center)
			
			# Get the estimate of the tape width
			estimate_width, estimate_wtolerance = self.estimate_tape_width(this_center[1],this_center[0])
			# We expect that the distance between legit tape centers is 2*(current tape size)
			estimate_distance = 2.0*estimate_width # Double the size of tape (from above)?
			estimate_tolerance = 3.0*estimate_wtolerance # Double the tolerance as above?
			
			# Compare this contour to every subsequent 'correct size' contour for distance
			for index2 in range(index+1,len(pass_size_contours)):
				
				#print(str(index)+","+str(index2))
				
				# Get the next/comparison contour
				another_contour = pass_size_contours[index2]
				another_center = np.array(cv2.minAreaRect(another_contour)[0])
				# Compute distance in pixels
				dist = np.sqrt(np.sum(np.power(this_center-another_center,2.0)))
				#print("  Distance to "+str(index2)+" is "+str(dist)+" pixels ("+str(estimate_distance)+","+str(estimate_tolerance)+")")
				if (dist>=estimate_distance-estimate_tolerance) \
					and (dist<=estimate_distance+estimate_tolerance):
					#print("  PASS "+str(used[index])+","+str(used[index2]))
					if (used[index]==0) and (used[index2]==0):
						#print("    Assign both to next group "+str(next_group))
						used[index] = next_group
						used[index2] = next_group
						next_group += 1
					elif (used[index]==0) or (used[index2]==0):
						this_group = np.max([used[index],used[index2]])
						#print("    Assign both to "+str(this_group))
						used[index] = this_group
						used[index2] = this_group
					else:
						#print("    Reassign every used of "+str(used[index])+" to "+str(used[index2]))
						from_value = used[index]
						to_value = used[index2]
						for index3 in range(0,len(used)):
							if (used[index3]==from_value):
								used[index3] = to_value
						
						
		# LOOK AT THE GROUPS AND PICK THE BEST
		best_group = -1
		best_group_count = -1
		if(len(used) > 0):
			for group_number in range(1,np.max(used)+1):
				
				local_count = used.count(group_number)
				if (local_count==0):
					continue

				if (True):
					# Pull this group out of the big set
					this_group = []
					for index in range(len(used)):
						if (used[index]==group_number):
							this_group.append(pass_size_contours[index])
					#print("THIS GROUP "+str(group_number)+" LEN = "+str(len(this_group)))
					
					# Check for angular validity
					pairwise_angles = []
					for index in range(len(this_group)):
						this_contour = this_group[index]
						this_center = np.array(cv2.minAreaRect(this_contour)[0])    
						for index2 in range(index+1,len(this_group)):
							another_contour = this_group[index2]
							another_center = np.array(cv2.minAreaRect(another_contour)[0])

							if (this_center[0]<=another_center[0]):
								pairwise_angles.append(90.0-(180.0/np.pi)*np.arctan2(another_center[1]-this_center[1],another_center[0]-this_center[0])) 
							else:
								pairwise_angles.append(90.0-(180.0/np.pi)*np.arctan2(this_center[1]-another_center[1],this_center[0]-another_center[0])) 
					# If the variance is 'big' skip
					if (np.std(pairwise_angles)>15.0):
						print("REJECT GROUP WITH STD()="+str(np.std(pairwise_angles)))
						continue
					#print(str(np.std(pairwise_angles)))
					
				# If we are still considering this it passed the group consistency check(s)
				#     then pick the group with the highest content count
				if (local_count > best_group_count):
					best_group_count = local_count
					best_group = group_number
							
						
						
		# Convert the list of 'accepted' spaced/distanced contours to the output set
		final_contours = []
		for index in range(len(pass_size_contours)):
			if (used[index]==best_group):
				final_contours.append(pass_size_contours[index])
		# print("PASSED "+str(len(final_contours))+" CONTOURS")
		
		#------------------------------------------------------------
		# Convert the passing contours to a return distance estimate
		if (len(final_contours)==0):
			# No contours so return a failure status
			this_col = -1
			this_row = -1
			
			targetDistance = -1
			targetAngle = 0
		else:
			# Contours - convert to distance and angle
			count = 0
			this_col = 0
			this_row = 0
			for this_contour in final_contours:
				rect = cv2.minAreaRect(this_contour)
				this_col += rect[0][0]
				this_row += rect[0][1]
				count += 1
				
			this_col /= count 
			this_row /= count
			
		return this_row, this_col
			
	
	def estimate_target_distance(self, row, height):
		"""
		Estimate distance based on regression from test data
		"""
		Pyx2 = np.array([719.87601135, -3905.32210081,  5362.87630488])
		estimate_distance = np.polyval(Pyx2,np.log10(height-row))
		return estimate_distance
	
	def estimate_target_angle(self, col, hfov, width):
		"""
		Estimate angle based on camera info
		"""
		estimate_angle = (hfov/width) * (col-width/2)
		return estimate_angle
	
	
	