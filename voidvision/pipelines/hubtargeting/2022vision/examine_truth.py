#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 22:18:44 2022

@author: johnwegrzyn
"""

import numpy as np
import matplotlib.pyplot as plt


import os
import sys
import copy



def my_strip_nonnumber ( in_string ):
    
    temp = ''
    for index in range(len(in_string)):
        if ( ( (in_string[index]>='0') and (in_string[index]<='9') ) or (in_string[index]=='.') ):
            temp += in_string[index]
    return(float(temp))


if __name__ == "__main__":

    

    base_path = r'C:\Users\sdtul\Data'
    
    
    images_total = 0
    
    distance = []
    measure = []
    
    with open('truth.csv', 'r') as f:
        
        done = False
        
        while not(done):
        
            # Read the next line in this comma separated file
            line = f.readline()
            if (len(line)==0):
                done = True
            else:
                #print(line)
                
                # Break the line into elements
                elements = line.split(',')
            
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
                distance.append(temp_distance)
                
                # Read the image
                in_image = plt.imread(os.path.join(base_path,elements[0]))
                gray_image = np.sum(in_image,axis=2)
                
                # Convert the input comma separated values into the manually clicked row,col positions
                rows = []
                cols = []
                if (False):
                    # Convert all of the 5 extracted boxes into a list
                    for point in range(0,10):
                        rows.append(my_strip_nonnumber(elements[1+point*2+1]))
                        cols.append(my_strip_nonnumber(elements[1+point*2+0]))
                else:
                    # ONLY CONVERT THE 'MIDDLE' BOX to a list
                    for point in range(4,6):
                        rows.append(my_strip_nonnumber(elements[1+point*2+1]))
                        cols.append(my_strip_nonnumber(elements[1+point*2+0]))
                
                UL_row = int(np.floor(np.min(rows)))
                LR_row = int(np.ceil(np.max(rows)))
                UL_col = int(np.floor(np.min(cols)))
                LR_col = int(np.ceil(np.max(cols)))
                
                debug_measure = False
                if (debug_measure):
                    debug_image = np.zeros( (LR_row-UL_row+1,LR_col-UL_col+1), dtype=np.float )
                
                # Define a bounding box from the user input individual boxes
                minv = np.inf
                maxv = 0
                for r in range(UL_row,LR_row):
                    for c in range(UL_col,LR_col):
                        if (debug_measure):
                            debug_image[r-UL_row][c-UL_col] = gray_image[r][c]
                        
                        minv = np.min([minv,gray_image[r][c]])
                        maxv = np.max([maxv,gray_image[r][c]])
                threshold = minv + 0.5*(maxv-minv)

                if (debug_measure):
                    plt.figure(10)
                    plt.clf()
                    plt.imshow(debug_image)
                
                # Look in the user defined bounding box to estimate some measure
                count = 0
                sumv = 0
                for r in range(int(np.floor(np.min(rows))),int(np.ceil(np.max(rows)))):
                    for c in range(int(np.floor(np.min(cols))),int(np.ceil(np.max(cols)))):
                        if (gray_image[r][c]>=threshold):
                            if (debug_measure):
                                plt.plot(c-UL_col,r-UL_row,'rx')
                            sumv += r
                            count += 1
                weighted_row = sumv/count
                if (debug_measure):
                    plt.plot([0,LR_col-UL_col],[weighted_row-UL_row,weighted_row-UL_row],'r-',linewidth=2)
                    plt.draw()
                    plt.show()
                    plt.pause(1)
                    plt.ginput(1,timeout=0)
                
                # SAVE THE MEASURE
                measure.append(weighted_row)




    # Take the accumulated X and Y (distance and row) and fit a line to them
    
    # POLYNOMIAL FIT
    # fit measure given distance
    Pxy1 = np.polyfit(distance,measure,2)
    x_new1 = list(range(0,np.max(distance)+20))
    y_new1 = np.polyval(Pxy1,x_new1)
    # fit distance given measure
    Pyx1 = np.polyfit(measure,distance,3)
    y_new2 = list(range(1,480)) # Assume a limit based on a 640x480 image - this measure is a row 0-479
    x_new2 = np.polyval(Pyx1,y_new2)
    for index in range(len(x_new2)):
        x_new2[index] = np.min([np.max(distance)+20,np.max([0,x_new2[index]])]) # Bound the fit 0-max considered distance
        
    # LOG-SCALED FIT
    # LOG fit measure given distance
    Pxy2 = np.polyfit(distance,np.log10(np.subtract(480,measure)),2)
    x_new3 = list(range(0,np.max(distance)+20))
    y_new3 = np.subtract(480,np.power(10,np.polyval(Pxy2,x_new3)))
    # LOG fit distance given measure
    Pyx2 = np.polyfit(np.log10(np.subtract(480,measure)),distance,2)
    y_new4 = list(range(1,480)) # Assume a limit based on a 640x480 image - this measure is a row 0-479
    x_new4 = np.polyval(Pyx2,np.log10(np.subtract(480,y_new4)))
    for index in range(len(x_new2)):
        x_new4[index] = np.min([np.max(distance)+20,np.max([0,x_new4[index]])]) # Bound the fit 0-max considered distance
        
        
    # DISPLAY SOME RESULTS
    plt.figure(1)
    plt.clf()
    plt.plot(distance,measure,'bo')
    plt.plot(x_new1,y_new1,'k-')
    plt.plot(x_new2,y_new2,'r-')
    plt.plot(x_new3,y_new3,'b-')
    plt.plot(x_new4,y_new4,'g-')
    plt.xlabel('(Approximate) Distance (inches from leading target edge)')
    plt.ylabel('MEASURE VALUE (Row Pixel)')
    plt.legend(['Data','Polynomial Fit - measure given distance','Polynomial Fit - distance given measure','LOG Fit - measure given distance','LOG Fit - distance given measure'])
    plt.draw()
    plt.show()
    plt.pause(1)
    
    exit()