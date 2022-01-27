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
        ntinst.startServer(port=862) # TODO: test if you can assign port based on var, ie port=team
    else:
        print("Setting up NetworkTables client for team {}".format(team))
        ntinst.startClientTeam(team)
        ntinst.startDSClient()

    # Push test values
    ntinst.getTable("SmartDashboard").putNumber("test", 0)
    
    # Loop
    t_init = time.time()
    t = t_init
    p = 6

    while(True):

        t = time.time()
        
        ntinst.getTable("SmartDashboard").putNumber("time", t)
        ntinst.getTable("SmartDashboard").putNumber("6", p)
