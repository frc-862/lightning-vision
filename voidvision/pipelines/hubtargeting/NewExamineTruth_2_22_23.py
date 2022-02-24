#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 22:18:44 2022

@author: johnwegrzyn
"""

import numpy as np
import matplotlib.pyplot as plt

import cv2

import os
import sys
import copy


#=======================================================================
def estimate_tape_width(row,col):
    
    estimate_width = ((6-24)/(400-80))*row+28.5
    estimate_wtolerance = (-5.0/480.0)*row+6.0+0.6

    return estimate_width, estimate_wtolerance

#=======================================================================
def estimate_tape_height(row,col):
    
    estimate_height = ((2.3-5)/(400-50))*row+5.4
    #estimate_htolerance = 10*((-5.0/480.0)*row+8.0+0.8)
    estimate_htolerance = 0.5*((-5.0/480.0)*rect[0][1]+6.0+0.6)

    return estimate_height, estimate_htolerance

#=======================================================================
def estimate_target_distance(row,col):
    
    Pyx2 = np.array([  191.51511229, -1126.75769868,  1666.51815349])

    estimate_distance = np.polyval(Pyx2,np.log10(480-row))
    
    return estimate_distance

#=======================================================================
def estimate_target_angle(row,col):
    
    hfov = 120.0 # Degrees
    
    estimate_angle = (640/hfov)*(col-640/2)
    
    return estimate_angle


#=======================================================================
def fit_ellipse ( points ):
    # Estimate the size of the detection by fitting an
    #    ellipse to the point through projection
    
    # Compute the covariance matrix on the de-meaned points
    if (len(points)>1):
        # Find the avergaed value center
        # FIX ME - might move to a weighted center
        center = np.mean(points,0)
        
        # remove the mean pixel location from the list of pixels
        demeaned_points = np.subtract(points,center)
        
        # Compute the covariance matrix of the demeaned list of pixels
        cov_mat = (1.0/len(demeaned_points))*np.transpose(demeaned_points).dot(demeaned_points)
        # Do eigen vector decomposition to reduce points to a new basis representation
        [d,v] = np.linalg.eig(cov_mat)
        # Define the major and minor axes by their decomposition eignevalues
        if (d[0]>d[1]):
            semimajor = np.sqrt(d[0])*2.0
            semiminor = np.sqrt(d[1])*2.0
            orientation = np.arctan2(v[0][1],v[0][0])*(180.0/np.pi)-90.0
        else:
            semimajor = np.sqrt(d[1])*2.0
            semiminor = np.sqrt(d[0])*2.0
            orientation = np.arctan2(v[1][1],v[1][0])*(180.0/np.pi)-90.0
        # Check and fix the major and minor axis sizes
        major = max(0.5,semimajor*2.0)
        semimajor = 0.5*major
        minor = max(0.5,semiminor*2.0)
        semiminor = 0.5*minor
    else:
        # For a single detection point fake a small ellipse
        center = [0,0]
        orientation = 0.0
        major = 0.5
        semimajor = 0.5*major
        minor = 0.5
        semiminor = 0.5*minor
    
    return center, orientation, semimajor, semiminor


def plot_ellipse ( figure_number, center, orientation, semimajor, semiminor ):
    
    # Compute the ellipse estimated by the points in the detected blob
    #npoints = 120.0
    npoints = 32.0
    phi = 2.0*np.pi*(1.0/npoints)*np.arange(0.0,npoints,1.0)
    x = semimajor*np.cos(phi)
    y = semiminor*np.sin(phi)
    xprime = center[1] - x*np.cos(orientation*(np.pi/180.0)) + y*np.sin(orientation*(np.pi/180.0))
    yprime = center[0] - x*np.sin(orientation*(np.pi/180.0)) - y*np.cos(orientation*(np.pi/180.0))
        
    # Plot the ellipse on the contrast enhanced image
    plt.figure(figure_number)
    plt.plot(xprime,yprime,'k^-',linewidth=3)
    plt.plot(xprime,yprime,'w^-',linewidth=1)
    plt.draw()
    plt.pause(0.1)
                            
    
def contourIntersect(original_image, contour1, contour2):

    blank1 = np.zeros(original_image.shape[0:2])
    cv2.fillPoly(blank1, pts=[contour1], color=(1))
    
    blank2 = np.zeros(original_image.shape[0:2])
    cv2.fillPoly(blank2, pts=[contour2], color=(1))
    
    # Use the logical AND operation on the two images
    # Since the two images had bitwise AND applied to it,
    # there should be a '1' or 'True' where there was intersection
    # and a '0' or 'False' where it didnt intersect
    intersection = np.logical_and(blank1, blank2)

    # Check if there was a '1' in the intersection array
    return intersection.any()




# Crappy way to convert a hard string to a number
def my_strip_nonnumber ( in_string ):
    
    temp = ''
    for index in range(len(in_string)):
        if ( ( (in_string[index]>='0') and (in_string[index]<='9') ) or (in_string[index]=='.') ):
            temp += in_string[index]
    return(float(temp))



#****************************************************************************
#****************************************************************************
#****************************************************************************
#****************************************************************************
if __name__ == "__main__":

    # Set interactive display to be on
    plt.ion()
    # plt.ioff() # Turn interactive mode off
    
    
    # For some functions the version matters for return arguments
    (cv2_major, cv2_minor, cv2_patch) = map(int,cv2.__version__.split("."))
    
    base_path = r'C:\Users\sdtul\DataV2'
    
    
    images_total = 0
    
    control_row = []
    control_col = []
    control_contour_row = []
    control_contour_col = []
    control_distance = []
    
    measure_contour_width = []
    measure_contour_height = []
    measure_contour_orientation = []
    
    measure_target_row = []
    measure_target_col = []
    measure_target_distance = []
    measure_target_angle = []
    
    # Build a matrix of results [ right size, target; right_size, not target;
    #                             not right size, target; not right size, not target ]
    accumulate_results = np.zeros( (2,2), dtype=np.float )
    total_found = 0
    total_tried = 0
        
    with open(os.path.join(base_path,'truth_0.csv'), 'r') as f:
        
        done = False
       
        while not(done):
        
            # Read the next line in this comma separated file
            line = f.readline()
            if (len(line)==0):
                done = True
            else:
                #print(line)
                
                #---------------------------------------------------
                # Break the line into elements
                elements = line.split(',')
            
                #---------------------------------------------------
                # Parse the filename to get the distance
                end_index = elements[0].find('in')
                start_index = end_index
                
                while (start_index>=0):
                    if (elements[0][start_index]=='/'):
                        break
                    start_index -= 1
                start_index += 1
                temp_distance = int(elements[0][start_index:end_index])
                
                # SAVE THE DISTANCE
                control_distance.append(temp_distance)
                
                #---------------------------------------------------
                # Convert the input comma separated values into the manually clicked row,col positions
                rows = []
                cols = []
                # Convert all of the 5 extracted boxes into a list
                for point in range(0,10):
                    rows.append(my_strip_nonnumber(elements[1+point*2+1]))
                    cols.append(my_strip_nonnumber(elements[1+point*2+0]))

                # Convert the read 'truth' points into a set of contours
                truth_contours = []
                row_pad = 0
                col_pad = 0
                for index in range(int(len(rows)/2)):                    
                    UL_row = int(np.floor(np.min([rows[2*index+0],rows[2*index+1]]))-row_pad)
                    LR_row = int(np.ceil(np.max([rows[2*index+0],rows[2*index+1]]))+row_pad)
                    UL_col = int(np.floor(np.min([cols[2*index+0],cols[2*index+1]]))-col_pad)
                    LR_col = int(np.ceil(np.max([cols[2*index+0],cols[2*index+1]]))+col_pad)
                    truth_contours.append( np.array([ [[LR_col,LR_row]],[[UL_col,LR_row]],[[UL_col,UL_row]],[[LR_col,UL_row]] ],dtype=np.int32) )
                
                #---------------------------------------------------
                # Read the image (!!!!CV2 forces BGR NOT RGB!!!!)
                if not(os.path.exists(os.path.join(base_path,elements[0]))):
                    continue
                in_image = cv2.imread(os.path.join(base_path,elements[0]))
                
                #----------------------------------------------------
                # GRIP-like OpenCV/cv2 pipeline of processing
                
                if (False):
                    # Threshold on 'color' (initilaly just keep bright things...)
                    # BGR not RGB
                    color_mask = cv2.inRange(in_image,(0,96,0),(255,255,255))
                else:
                    green_layer = in_image[:,:,1] # Pull out just the green layer
                    color_mask = cv2.inRange(green_layer,100,256) # Just looking at mostly bright green layer
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
                
                # Review the processing images
                debug_input = False
                if (debug_input):
                    plt.figure(1)
                    plt.clf()
                    plt.imshow(cv2.cvtColor(in_image,cv2.COLOR_BGR2RGB))
                    plt.draw()
                    plt.show(block=False)
                    
                    plt.figure(2)
                    plt.clf()
                    plt.imshow(color_mask)
                    plt.draw()
                    plt.show(block=False)
                    
                    plt.figure(3)
                    plt.clf()
                    plt.imshow(im_dilate)
                    plt.draw()
                    plt.show(block=False)
                    
                    plt.figure(4)
                    plt.clf()
                    plt.imshow(im_erode)
                    plt.draw()
                    plt.show(block=False)
                    
                    plt.ginput(1,timeout=0)
                    foo = 0
                            
            
                #------------------------------------------------------
                # On the "best processed output mask", find all the contours
                if (cv2_major>=4):
                    contours, hierarchy = cv2.findContours(im_erode, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                else:
                    im2, contours, hierarchy = cv2.findContours(im_erode, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    
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
                    estimate_width, estimate_wtolerance = estimate_tape_width(rect[0][1],rect[0][0])
                    estimate_height, estimate_htolerance = estimate_tape_height(rect[0][1],rect[0][0])
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
                
                    #=======================================================
                    # DO SOME DEBUG ON THE SIZING CHECK
                    # Check to see if the fit box intersects with any truth
                    fit_contour = np.int0(cv2.boxPoints(rect))
                    match_truth_contour = False
                    for truth_contour in truth_contours:
                        if contourIntersect(in_image, truth_contour, fit_contour):
                            match_truth_contour = True
                            
                            control_contour_row.append(rect[0][1])
                            control_contour_col.append(rect[0][0])
                    
                            measure_contour_width.append(contour_width)
                            measure_contour_height.append(contour_height)
                            measure_contour_orientation.append(rect[2])
    
                    if (match_truth_contour):
                        # Contours intersect
                        if (match_size):
                            # There was a size match and overlapping contours - CORRECT
                            accumulate_results[0][0] += 1
                        else:
                            # There was not a size match but overlapping contours - MISTAKE (truth location not matched)
                            accumulate_results[0][1] += 1
                            #print("MATCH TRUTH, NOT SIZE")
                            #print([contour_height,contour_width,estimate_height,estimate_width,estimate_tolerance])
                            match_truth_not_size.append(this_contour)
                    else:
                        # Contours do not intersect
                        if (match_size):
                            # There was a size match but the no overlapping contours - MISTAKE (false alarm passes size check)
                            accumulate_results[1][0] += 1
                            #print("MATCH SIZE, NOT TRUTH")
                            #print([contour_height,contour_width,estimate_height,estimate_width,estimate_tolerance])
                            match_size_not_truth.append(this_contour)
                        else:
                            # There was not a size match and no overlapping contours - CORRECT (ignore false alarm)
                            accumulate_results[1][1] += 1


                #===========================================================
                # Do some debug on the final result of the target search checking
                pass_size_debug = False
                if (pass_size_debug):
                    plt.figure(321)
                    plt.clf()
                    plt.imshow(im_erode)
                    for this_contour in truth_contours:
                        for index in range(len(this_contour)):
                            plt.plot([this_contour[index][0][0],this_contour[(index+1)%len(this_contour)][0][0]], \
                                     [this_contour[index][0][1],this_contour[(index+1)%len(this_contour)][0][1]],'w-')
                    for this_contour in pass_size_contours:
                        rect = cv2.minAreaRect(this_contour)
                        plt.plot(rect[0][0],rect[0][1],'bo')
                    for this_contour in match_truth_not_size:
                        rect = cv2.minAreaRect(this_contour)
                        plt.plot(rect[0][0],rect[0][1],'r^')
                    for this_contour in match_size_not_truth:
                        rect = cv2.minAreaRect(this_contour)
                        plt.plot(rect[0][0],rect[0][1],'rv')
                    plt.draw()
                    plt.show(block=False)
                    plt.ginput(1,timeout=0)
                    
            
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
                for index in range(len(pass_size_contours)):
                    #print("Processing contour number "+str(index)+" of "+str(len(pass_size_contours)))
                    this_contour = pass_size_contours[index]
                    this_center = np.array(cv2.minAreaRect(this_contour)[0])
                    #print(this_center)
                    
                    # Get the estimate of the tape width
                    estimate_width, estimate_wtolerance = estimate_tape_width(this_center[1],this_center[0])
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
            
                total_found += int(len(final_contours)>0)
                total_tried += 1
                
                #===========================================================
                # Do some debug on the final contours
                final_contours_debug = True
                if (final_contours_debug):
                    plt.figure(421)
                    plt.clf()
                    plt.imshow(im_erode)
                    for this_contour in truth_contours:
                        for index in range(len(this_contour)):
                            plt.plot([this_contour[index][0][0],this_contour[(index+1)%len(this_contour)][0][0]], \
                                     [this_contour[index][0][1],this_contour[(index+1)%len(this_contour)][0][1]],'w-')
                    for this_contour in pass_size_contours:
                        rect = cv2.minAreaRect(this_contour)
                        plt.plot(rect[0][0],rect[0][1],'bo')
                    for this_contour in match_truth_not_size:
                        rect = cv2.minAreaRect(this_contour)
                        plt.plot(rect[0][0],rect[0][1],'r^')
                    for this_contour in match_size_not_truth:
                        rect = cv2.minAreaRect(this_contour)
                        plt.plot(rect[0][0],rect[0][1],'rv')
                    for this_contour in final_contours:
                        rect = cv2.minAreaRect(this_contour)
                        plt.plot(rect[0][0],rect[0][1],'go',markersize=10,alpha=0.5)
                    plt.draw()
                    plt.show(block=False)
                    #plt.ginput(1,timeout=0)            
                    foo = 0
            
                #------------------------------------------------------------
                # Convert the passing contours to a return distance estimate
                if (len(final_contours)==0):
                    # No contours so return a failure status
                    this_col = -1
                    this_row = -1
                    
                    this_distance = -1
                    this_angle = 0
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
                    
                    this_distance = estimate_target_distance(this_row,this_col)
                    this_angle = estimate_target_angle(this_row,this_col)
            
                measure_target_row.append(this_row)
                measure_target_col.append(this_col)
                measure_target_distance.append(this_distance)
                measure_target_angle.append(this_angle)

    # Debug run statistics
    print("Matrix of contour size results:  [right size, target; right_size, not target; not right size, target; not right size, not target]")
    print(accumulate_results)
    print("Fraction of images with reasonable targets: "+str(total_found)+"/"+str(total_tried)+"="+str(total_found/total_tried))



    # EXAMINE THE ACCUMULATED CONTROL AND MEASURE VALUES
    plt.figure(101)
    plt.clf()
    plt.plot(control_contour_row,measure_contour_width,'bo')
    plt.plot(control_contour_row,measure_contour_height,'kx')
 
    temp_x = []
    temp_y = []
    temp_tol = []
    for x in range(0,479):
        estimate_width, estimate_wtolerance = estimate_tape_width(x,640/2)

        temp_x.append(x)
        temp_y.append( estimate_width )
        temp_tol.append( estimate_wtolerance )
    plt.plot(temp_x,temp_y,'b-')
    plt.plot(temp_x,np.add(temp_y,temp_tol),'b:')
    plt.plot(temp_x,np.subtract(temp_y,temp_tol),'b:')

    temp_x = []
    temp_y = []
    temp_tol = []
    for x in range(0,479):
        estimate_height, estimate_htolerance = estimate_tape_height(x,640/2)

        temp_x.append(x)
        temp_y.append( estimate_height )
        temp_tol.append( estimate_htolerance )
    plt.plot(temp_x,temp_y,'k-')
    plt.plot(temp_x,np.add(temp_y,temp_tol),'k:')
    plt.plot(temp_x,np.subtract(temp_y,temp_tol),'k:')
    
    plt.title("Image Row VERSUS CONTOUR target width and height")
    plt.draw()
    plt.show(block=False)
    
    
 
    # Take the accumulated X and Y (distance and row) and fit a line to them
    
    # POLYNOMIAL FIT
    # fit measure given distance
    
    # Convert the actual legit target distances
    local_measure = []
    local_distance = []
    for index in range(len(control_distance)):
        if (measure_target_row[index]>0) and \
           ( (measure_target_col[index]>=640/2-100) and (measure_target_col[index]<=640/2+100) ):
            local_measure.append(measure_target_row[index])
            local_distance.append(control_distance[index])
    
    # Normal polynomial fit
    Pxy1 = np.polyfit(local_distance,local_measure,3)
    y = np.polyval(Pxy1,x)
    print(y)
    x_new1 = list(range(0,np.max(local_distance)+20))
    y_new1 = np.polyval(Pxy1,x_new1)
    # fit distance given measure
    Pyx1 = np.polyfit(local_measure,local_distance,2)
    y_new2 = list(range(1,480)) # Assume a limit based on a 640x480 image - this measure is a row 0-479
    x_new2 = np.polyval(Pyx1,y_new2)
    for index in range(len(x_new2)):
        x_new2[index] = np.min([np.max(local_distance)+20,np.max([0,x_new2[index]])]) # Bound the fit 0-max considered distance
        
    # LOG-SCALED FIT
    # LOG fit measure given distance
    Pxy2 = np.polyfit(local_distance,np.log10(np.subtract(480,local_measure)),1)
    x_new3 = list(range(0,np.max(local_distance)+20))
    y_new3 = np.subtract(480,np.power(10,np.polyval(Pxy2,x_new3)))
    # LOG fit distance given measure
    Pyx2 = np.polyfit(np.log10(np.subtract(480,local_measure)),local_distance,2)
    y_new4 = list(range(1,480)) # Assume a limit based on a 640x480 image - this measure is a row 0-479
    x_new4 = np.polyval(Pyx2,np.log10(np.subtract(480,y_new4)))
    for index in range(len(x_new2)):
        x_new4[index] = np.min([np.max(local_distance)+20,np.max([0,x_new4[index]])]) # Bound the fit 0-max considered distance
        
        
    # DISPLAY SOME RESULTS
    plt.figure(543)
    plt.clf()
    plt.plot(local_distance,local_measure,'bo')
    plt.plot(x_new1,y_new1,'k^-')
    plt.plot(x_new2,y_new2,'r>-')
    plt.plot(x_new3,y_new3,'bv-')
    plt.plot(x_new4,y_new4,'g<-')
    plt.xlabel('(Approximate) Distance (inches from leading target edge)')
    plt.ylabel('MEASURE VALUE (Row Pixel)')
    plt.legend(['DATA','Polynomial Fit - measure given distance','Polynomial Fit - distance given measure','LOG Fit - measure given distance','LOG Fit - distance given measure'])
    plt.draw()
    plt.show(block=False)
    plt.pause(1)
        
