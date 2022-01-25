#!/usr/bin/env python3

# Imports
import time
import cv2
from networktables import NetworkTablesInstance

# Define variables - TODO push this to a config file later
server = True
team = 862

# Main function
if __name__ == "__main__":
    
    # Start NetworkTables
    ntinst = NetworkTablesInstance.getDefault()
    if server:
        print("Setting up NetworkTables server")
        ntinst.startServer()
    else:
        print("Setting up NetworkTables client for team {}".format(team))
        ntinst.startClientTeam(team)
        ntinst.startDSClient()

    # Push test values
    ntinst.getTable("SmartDashboard").putNumber("test", 0)
    
    # Start camera
    cap = cv2.VideoCapture(0)

    # Loop
    t_init = time.time()
    t = t_init
    
    while(t < (t_init + 10)):

        t = time.time()
        
        ret, frame = cap.read()
        
        ntinst.getTable("SmartDashboard").putNumber("time", t)
        ntinst.getTable("SmartDashboard").putNumber("an-img-shape-thing", frame.shape[0])
        
        if cv2.waitKey(1):
            break
