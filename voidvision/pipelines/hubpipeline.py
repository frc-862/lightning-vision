#!/usr/bin/env python3

import os
from re import I
from tkinter import W
from pipeline import VisionPipeline
import camera
import numpy as np
import cv2
import sys
from gripipeline import GripPipeline
from time import sleep
import grip
import time


class HubPipeline(VisionPipeline):

    def __init__(self, config: str, cam_num: int, cam_name: str, output_name: str, table) -> None:

        self.nttable = table

        self.exposure_entry = table.getEntry('exposure')
        self.capture_entry = table.getEntry('capture frame')
        self.distance_entry = table.getEntry('distance input')

        # Initialize entry as 7	(idk why, just 7)	
        self.exposure_entry.setNumber(7)
        self.capture_entry.setBoolean(False)
        self.distance_entry.setString('42-thousand-tonnes')

        # Horizontal and vertical field of view
        self.fov_horiz = 99 
        self.fov_vert = 68.12 

        # start camera
        self.inp, self.out, self.width, self.height, self.cam, self.exposure, self.cameraPath = camera.start(config, cam_num, cam_name, output_name)

        # TODO: Determine usefulness
        self.targetHeightRatio = 0
        self.targetRatioThreshold = 0

        # allocate image for whenever
        self.img = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)
        self.output_img = np.zeros(shape=(self.height, self.width, 3), dtype=np.uint8)

    # =======================================================
    # TODO: Determine usefulness of functions and delete?

    def get_angle_from_target(self, target_center_col, image_width_cols):
            return (target_center_col - (image_width_cols / 2) * (self.fov_horiz / image_width_cols))
        
    def checkTargetProportion(self, targetBoxHeight, targetCenterRow):
            ratio = targetBoxHeight / targetCenterRow
            return (ratio - self.targetHeightRatio) < self.targetRatioThreshold
     # =======================================================

    def estimate_tape_width(self, row, col):
    
        estimate_width = ((6-24)/(400-80))*row+28.5
        estimate_wtolerance = (((-5.0/self.height)*row+6.0+0.6)*2)
    
        return estimate_width, estimate_wtolerance
    
    def estimate_tape_height(self, row, col):
    
        estimate_height = ((2.3-5)/(400-50))*row+5.4
        #estimate_htolerance = 10*((-5.0/480.0)*row+8.0+0.8)
        estimate_htolerance = (0.5*(((-5.0/self.height)*row+6.0+0.6)*2))

        return estimate_height, estimate_htolerance
    
    def estimate_target_distance(self, row, col):
    
        Pyx2 = np.array([  191.51511229, -1126.75769868,  1666.51815349])
    
        estimate_distance = np.polyval(Pyx2,np.log10(self.height-row))
    
        return estimate_distance
    
    def estimate_target_angle(self, row, col):
    
        estimate_angle = (self.fov_horiz/self.width)*(col-self.width/2)
    
        return estimate_angle

    def process(self):
        # This is to verify camera parameters we want set are set
        # set exposure
        # TODO: not call every time process is run, only when updated
        os.system("v4l2-ctl --device " + self.cameraPath + " --set-ctrl=exposure_absolute=" + str(self.exposure_entry.getNumber(7)))	

        # get frame from camera
        self.t, self.img = self.inp.grabFrame(self.img)

        # Debugging installed to allow us to capture raw images from robot camera
        if self.capture_entry.getBoolean(False):
            mills = str(int(time.time() * 1000))
            dist = self.distance_entry.getString('42-thousand-tonnes')
            fname = str('/home/lightning/voidvision/images/frame-distance-{}-{}.jpg'.format(dist, mills))
            cv2.imwrite(fname, self.img)
            print('FILE: {} WRITTEN'.format(fname))
            self.capture_entry.setBoolean(False)
        
        # Process input image through conditioning filters
        if (False):
            # Threshold on 'color' (initilaly just keep bright things...)
            # BGR not RGB
            color_mask = cv2.inRange(self.img,(0,96,0),(255,255,255))
        else:
            green_layer = self.img[:,:,1] # Pull out just the green layer
            color_mask = cv2.inRange(green_layer,100,256) # Just looking at mostly bright green layer
        # Define a dilate/erode kernel
        kernel = np.ones((5,5), np.uint8)
        # 'round' the kernel a little
        kernel[0][0] = 0
        kernel[4][0] = 0
        kernel[0][4] = 0
        kernel[4][4] = 0
        # Use the kernel to clean holes in blobs and smooth shape edges
        im_dilate = cv2.dilate(color_mask,kernel,iterations=2)
        im_erode = cv2.erode(im_dilate,kernel,iterations=2)

        #------------------------------------------------------
        # On the "best processed output mask", find all the contours
        contours, hierarchy = cv2.findContours(im_erode, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
        #========================================================
        # ADD A SANITY CHECK
        #    If there are an insane number of contours - bail!!!!!!
        #========================================================
        max_expected_contours = 30
        if (len(contours)>max_expected_contours):
            print("WARNING - TOO MANY CONTOURS ("+str(len(contours))+" VERSUS "+str(max_expected_contours)+")")
            # TODO: determine best course of action if getting too many contours
            # ex: auto adjust exposure, save image to understand what's going on

        # EXAMINE THE POSSIBILITIES FOR CONTOUR PROCESSING:
        # https://docs.opencv.org/3.4/dd/d49/tutorial_py_contour_features.html


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
            # print([contour_width, contour_height, rect[0]])
            #-------------------------------------------------------
            # NOTICE - SIZE CHECK - Use bounds around a fit to determine acceptable sizing
            estimate_width, estimate_wtolerance = self.estimate_tape_width(rect[0][1],rect[0][0])
            estimate_height, estimate_htolerance = self.estimate_tape_height(rect[0][1],rect[0][0])
            #print([contour_width,contour_height,estimate_width,estimate_wtolerance,estimate_height,estimate_htolerance])
            
            # Check to see if the width and height meet our expectations
            match_size = False
            if ( (contour_width>=estimate_width-estimate_wtolerance) \
                 and (contour_width <= estimate_width+estimate_wtolerance) \
                 and (contour_height >= estimate_height-estimate_htolerance) \
                 and (contour_height <= estimate_height+estimate_htolerance) ):
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
        if (len(pass_size_contours) > max_expected_size_contours):
            print("WARNING - TOO MANY SIZE CONTOURS (" + str(len(pass_size_contours)) + " VERSUS " + str(max_expected_size_contours) + ")")
            pass
        
        #============================================================
        # Add a check looking for nearby contours that also pass size check!!!
        #   this should help screen false alarms
        # TODO: FIX ME - decide what to do if there is only 1 remaining contour:  believe it or pass
        used = [0]*len(pass_size_contours)
        for index in range(len(pass_size_contours)):
            #print("Processing contour number "+str(index)+" of "+str(len(pass_size_contours)))
            this_contour = pass_size_contours[index]
            this_center = np.array(cv2.minAreaRect(this_contour)[0])
            #print(this_center)
            
            # Get the estimate of the tape width
            estimate_width, estimate_wtolerance = self.estimate_tape_width(this_center[1],this_center[0])
            # We expect that the distance between legit tape centers is 2*(current tape size)
            estimate_distance = 2.0*estimate_width # Double the size of tape (from above)?
            estimate_tolerance = 2.0*estimate_wtolerance # Double the tolerance as above?
            
            # Compare this contour to every subsequent 'correct size' contour for distance
            for index2 in range(index+1,len(pass_size_contours)):
                # Get the next/comparison contour
                another_contour = pass_size_contours[index2]
                another_center = np.array(cv2.minAreaRect(another_contour)[0])
                # Compute distance in pixels
                dist = np.sqrt(np.sum(np.power(this_center-another_center,2.0)))
                #print("  Distance to "+str(index2)+" is "+str(dist)+" pixels ("+str(estimate_distance)+","+str(estimate_tolerance)+")")
                if (dist>=estimate_distance-estimate_tolerance) \
                   and (dist<=estimate_distance+estimate_tolerance):
                    used[index] = 1
                    used[index2] = 1
        # Convert the list of 'accepted' spaced/distanced contours to the output set
        final_contours = []
        for index in range(len(pass_size_contours)):
            if (used[index]==1):
                final_contours.append(pass_size_contours[index])
        print("PASSED "+str(len(final_contours))+" CONTOURS") 
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
            
            targetDistance = self.estimate_target_distance(this_row,this_col)
            targetAngle = self.estimate_target_angle(this_row,this_col)

        # TODO: Test code for quality of truth

        self.nttable.putNumber('Target Angle', targetAngle)
        self.nttable.putNumber('Target Distance', targetDistance)

        # TODO: Puts number of contours detected in current image to the dashboard
        # self.nttable.putNumber('Contour Number', numContours)