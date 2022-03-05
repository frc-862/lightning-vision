#!/usr/bin/env python3

import os

from matplotlib import use
from pipeline import VisionPipeline
import camera
import numpy as np
import cv2
import sys
from time import sleep
import time

class HubPipeline(VisionPipeline):

    def __init__(self, config: str, cam_num: int, cam_name: str, output_name: str, table) -> None:

        self.nttable = table
		
        # start camera
        self.inp, self.out, self.width, self.height, self.cam, self.exposure, self.brightness, self.cameraPath = camera.start(config, cam_num, cam_name, output_name)

        # initial intensity threshold
        self.intensity_thresh = 100

        # Set this to true for tuning
        self.debug = True
        if self.debug:
            self.exposure_entry = table.getEntry('exposure')
            self.brightness_entry = table.getEntry('brightness')
            self.capture_entry = table.getEntry('capture frame')
            self.distance_entry = table.getEntry('distance input')
            self.intensity_thresh_entry = table.getEntry('Intensity Threshold')
    
            # Initialize network table entries
            self.capture_entry.setBoolean(False)
            self.distance_entry.setString('42-thousand-tonnes')
            self.exposure_entry.setNumber(self.exposure)
            self.brightness_entry.setNumber(self.brightness)
            self.intensity_thresh_entry.setNumber(self.intensity_thresh)
            # self.green_lower_threshold.setNumber(100) # 100 is default for now

        # Horizontal and vertical field of view
        self.fov_horiz = 99 
        self.fov_vert = 68.12 

        # TODO: Determine usefulness
        self.targetHeightRatio = 0
        self.targetRatioThreshold = 0

		# dashboard outputs
        self.target_distance_entry = table.getEntry('Target Distance')
        self.target_angle_entry = table.getEntry('Target Angle')
        # self.target_distance_entry.setNumber(-1)
        # self.target_angle_entry.setNumber(0)

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
    def estimate_tape_width(self,row,col):
        
        point1 = [38,26]
        #point2 = [310,4]
        point2=[340,5]
        
        estimate_width = ((point2[1]-point1[1])/(point2[0]-point1[0]))*row \
                        + (point1[1]-((point2[1]-point1[1])/(point2[0]-point1[0]))*point1[0])
        estimate_wtolerance = 1.1*((-5.0/480.0)*row+6.6)

        return estimate_width, estimate_wtolerance

    #=======================================================================
    def estimate_tape_height(self,row,col):
        
        point1 = [37,7]
        point2 = [312,2]
        
        estimate_height = ((point2[1]-point1[1])/(point2[0]-point1[0]))*row \
                        + (point1[1]-((point2[1]-point1[1])/(point2[0]-point1[0]))*point1[0])
        estimate_htolerance = 0.6*((-5.0/480.0)*row+6.6)

        return estimate_height, estimate_htolerance

    #=======================================================================
    def estimate_target_distance(self,row,col):
        
        #Pyx2 = np.array([  191.51511229, -1126.75769868,  1666.51815349])
        #Pyx2 = np.array([  594.86317999, -3320.84581578,  4693.62858767]) # 20220303
        Pyx2 = np.array([  719.87601135, -3905.32210081,  5362.87630488])

        estimate_distance = np.polyval(Pyx2,np.log10(480-row))
        
        return estimate_distance

    #=======================================================================
    def estimate_target_angle(self,row,col):
        
        hfov = 100.0 # Degrees
        
        estimate_angle = (hfov/640)*(col-640/2)
        
        return estimate_angle


    def process(self):
        # This is to verify camera parameters we want set are set
        # set exposure
        # TODO: not call every time process is run, only when updated
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
        
        
        # GRIP-like OpenCV/cv2 pipeline of processing
        
        if (False):
            # Threshold on 'color' (initilaly just keep bright things...)
            # BGR not RGB
            color_mask = cv2.inRange(self.img,(0,96,0),(255,255,255))
        elif (False):
            green_layer = self.img[:,:,1] # Pull out just the green layer
            color_mask = cv2.inRange(green_layer,100,256) # Just looking at mostly bright green layer
        else:
            sum_layer = np.array(np.sum(self.img,2),dtype = np.float) # Sum the layers
            color_mask = cv2.inRange(sum_layer,self.intensity_thresh,3*256) # Just looking at mostly bright green layer
    
        # Define a dilate/erode kernel
        kernel = np.ones((5,5), np.uint8)
        # 'round' the kernel a little
        kernel[0][0] = 0
        kernel[4][0] = 0
        kernel[0][4] = 0
        kernel[4][4] = 0
        # Use the kernel to clean holes in blobs and smooth shape edges
        im_dilate = cv2.dilate(color_mask,kernel,iterations=1)
        im_erode = cv2.erode(im_dilate,kernel,iterations=1)
        
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
            
            targetDistance = self.estimate_target_distance(this_row,this_col)
            targetAngle = self.estimate_target_angle(this_row,this_col)
    
        self.target_distance_entry.setDouble(targetDistance)
        self.target_angle_entry.setDouble(targetAngle)

        print('DIST: {} | ANGLE: {}'.format(targetDistance, targetAngle))

        # TODO: Puts number of contours detected in current image to the dashboard
        # self.nttable.putNumber('Contour Number', numContours)