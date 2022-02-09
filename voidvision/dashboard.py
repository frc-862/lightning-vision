#!/usr/bin/env python3

from networktables import NetworkTablesInstance, NetworkTables
import json

def load(configFile: str):

	with open(configFile) as cfg:
		config = json.load(cfg)
	server = True if config['ntmode'] == 'server' else False
	team = config['team']

	ntinst = NetworkTablesInstance.getDefault()
	if server:
		print("Setting up NetworkTables server")
		ntinst.startServer(port=team)
	else:
		print("Setting up NetworkTables client for team {}".format(team))
		ntinst.startClientTeam(team)
		ntinst.startDSClient()

	table = NetworkTables.getTable('Vision')

	return table

if __name__ == "__main__":
	print('do not run this script\nsomething is wrong')
