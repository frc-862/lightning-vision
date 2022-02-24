#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 21:01:04 2022

@author: johnwegrzyn
"""

import numpy as np
import matplotlib.pyplot as plt


import os
import sys
import copy


def color_distance ( image, color ):
    
    # Allocate a return image - single layer, the distance
    ri = np.zeros( (image.shape[0],image.shape[1]), dtype=np.float )
    
    for r in range(0,image.shape[0]):
        for c in range(0,image.shape[1]):
            ri[r][c] = np.sqrt(np.sum(np.power(image[r][c]-color,2)))
            
    # Return the image
    return ri


def color_correlation ( image, color ):
    
    # Allocate a return image - single layer, the distance
    ri = np.zeros( (image.shape[0],image.shape[1]), dtype=np.float )
    
    corr_vec = color-np.mean(color)
    scalar = np.linalg.norm(corr_vec)
    corr_vec = (1.0/scalar)*corr_vec
    
    for r in range(0,image.shape[0]):
        for c in range(0,image.shape[1]):
            loc_vec = image[r][c]-np.mean(image[r][c])
            scalar = np.linalg.norm(loc_vec)
            loc_vec = (1.0/scalar)*loc_vec
            
            ri[r][c] = np.sum(np.multiply(loc_vec,corr_vec))
            
    # Return the image
    return ri


if __name__ == "__main__":
    
    
    base_path = r'/home/johnwegrzyn/Desktop/FRC/2022/Vision/2022 Vision targets v5'
    
    
    images_total = 0
    
    # Make sure we don't overwrite a previous attempt (incase there is good crap in it and there was an error)
    try_number = 0
    done = False
    while not(done):
        output_filename = os.path.join(base_path,'truth_'+str(try_number)+'.csv')
        if os.path.exists(output_filename):
            try_number += 1
        else:
            done = True
    
    # Open a file to write to
    with open(output_filename, 'w') as f:
        
        # Walk through all the files and find images to display/process
        for my_path, my_subdirs, my_files in os.walk(base_path):
            # Process each file in each directory
            for my_file in my_files:
                
                if (my_file.endswith(".png")):
                    images_total += 1
                    
                    temp_string = os.path.join(my_path,my_file)
                    f.write(temp_string[len(base_path)+1:]) # Strip the base path off to allow sharing of data files
                    f.write(",")
                    
                    in_image = plt.imread(os.path.join(my_path,my_file))
                    
                    plt.figure(1)
                    plt.clf()
                    plt.imshow(in_image)
                    
                    if (False):
                        #color_dist = color_distance(in_image,np.array([0,1,0]))
                        color_dist = color_correlation(in_image,np.array([0,1,0]))
        
                        plt.figure(2)
                        plt.clf()
                        plt.imshow(color_dist,cmap='hot')
                    
                    plt.draw()
                    plt.show()
                    plt.pause(0.1)
    
                    # BIG ASSUMPTION - WE FORCE THE USER OF THIS TOOL TO FIND 5 BOXES
                    # BIG ASSUMPTION #2 - THE BOXES ARE FOUND LEFT TO RIGHT
                    # BIG ASSUMPTION #3 - first click on a box is upper left (UL) and the second is lower right (LR)
                    # BIG ASSUMPTION #4 - clicked box spans all of the detectable energy for a reflected target
                    
                    v = plt.ginput(10,timeout=0)
                    for index in range(10):
                        f.write(str(v[index])+",")
                    f.write("\n")
    
    # EXAMPLE OUTPUT LINE:
    # 220in/debug5_exposure-10.png,(306.1321361922536, 430.16001447233117),(309.78830407129533, 432.44511939673225),(315.27255588985804, 428.7889515176905),(322.5848916479416, 431.0740564420916),(330.8112693757855, 427.8749095479301),(338.58062611874936, 431.5310774269718),(346.3499828617131, 427.8749095479301),(353.2052976349165, 430.6170354572114),(359.60359142323955, 430.16001447233117),(364.1738012720418, 433.35916136649274),
    # PROCESSING PROGRAM NEEDS TO BE ABLE TO READ AND PROCESS THIS INFO
    
    print("Total images:  "+str(images_total))
            