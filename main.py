import math
import os
import sys
from pathlib import Path
import logging
import subprocess
import re


"""
####################################################################################################
----------------------------------------------------------------------------------------------------

directory system: 
geometry: 
	- step files from cadquery
mesh: 
	- mesh solver's I/O ( mesh solver: gmsh )
	mainly used for .format output and conv with meshIO  
simulation: 
	- physical solver's I/O (Elmer, OpenFOAM) 
	CFD, FEM, FVM if i can my hands on other solvers, than i will try to integrate more of them
	solution: 
		- results 
log:
	- details about the workflow -> std,war,err
	
----------------------------------------------------------------------------------------------------
####################################################################################################

"""

#####################################################
################ Build Logging ######################
#####################################################

#Create log folder
if not(os.path.exists("./log/log.txt")):
	os.mkdir("./log")

#Set up logging
if os.path.exists("./log/log.txt"):
	logging.basicConfig(filename="./log/log.txt", level=logging.DEBUG,
						format="%(asctime)s - %(levelname)s - %(message)s", filemode="a")
else:
	logging.basicConfig(filename="./log/log.txt", level=logging.DEBUG,
					format="%(asctime)s - %(levelname)s - %(message)s", filemode="w")
logging.info("Start")

#####################################################
########### Build Work Directories ##################
#####################################################

#Create directories
directories = ("./geometry","./mesh","./simulation")
for d in directories:
	try:
		os.mkdir(d)
	except FileExistsError:
		logging.info("%s already exists.",d)
	else:
		logging.info("%s created",d)

#####################################################
################ Build Geometry #####################
#####################################################

# Define command as string
cmd = 'python geometry_processor.py'

# Use shell to execute the command and store it in sp variable
sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

# Separate the output and error.
# This is similar to Tuple where we store two values to two different variables
out,err=sp.communicate()

# clear ANSI codes
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
out = ansi_escape.sub('', out)
err = ansi_escape.sub('', err)

# Store the return code in rc variable
rc=sp.wait()

logging.info('GEOMETRY OUTPUT:\n' + out)
logging.info('GEOMETRY ERROR:\n' + err)
logging.info("GEOMETRY RETURN CODE: " + str(rc))

#####################################################
################ Build Mesh #########################
#####################################################

# Define command as string
cmd = 'python mesh_processor.py'

# Use shell to execute the command and store it in sp variable
sp = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

# Separate the output and error.
# This is similar to Tuple where we store two values to two different variables
out,err=sp.communicate()

# clear ANSI codes
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
out = ansi_escape.sub('', out)
err = ansi_escape.sub('', err)

# Store the return code in rc variable
rc=sp.wait()

logging.info('MESH OUTPUT:\n' + out)
logging.info('MESH ERROR:\n' + err)
logging.info("MESH RETURN CODE: " + str(rc))

logging.info("End")
logging.shutdown()
