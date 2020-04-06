from flask import Flask, jsonify, request
import logging
import json
import os
import subprocess
import shlex
import time
from os import path

#
# Instantiating Log Handlers
##

logging.basicConfig(filename='myApplication.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s : %(message)s')


#
# Instantiating the Flask app
##

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

#
# Subroutines
##

# A subroutine which receives the volume name as input for which the df output has to be returned in python dict format
#
def df_to_json(volName: str) -> dict:
	# We do a df -h and construct a dict of all rows of the output
	# The below is using list comprehension syntax. shlex.split is used to split with quotes. 
	df_array = [shlex.split(x) for x in subprocess.check_output(["df", "-h"], universal_newlines=True).rstrip().split('\n')]

	df_json = {}
	
	# The next line is highly tied to df -h output format. But serves our purpose. Building a dict of dicts
	for each_row in df_array: df_json[each_row[5]] = { "filesystem": each_row[0], "total_size": each_row[1], "used_size": each_row[2], "available_size": each_row[3], "used_percent": each_row[4] }

	# If the volume name given is a filesystem then return the df output for that. Else return "Not a filesystem"
	if volName in df_json: 
		app.logger.info("Given volume name is a filesystem")
		return {volName: df_json[volName]}
	else:
		app.logger.info("Given volume name is not a filesystem")
		return {volName: "Not a filesystem"}


# A subroutine that receives volume name as input for which stat output has to be returned in python dict format
#
def stat_to_json(volName: str) -> dict:
	sObj = os.stat(volName)

	# The next line uses in dict comprehension syntax "a: b for a in a's if a is something"
	return {k: getattr(sObj, k) for k in dir(sObj) if k.startswith('st_')}


# A subroutine that receives volume name as input for which statvfs output has to be returned in python dict format
#
def statvfs_to_json(volName: str) -> dict:
	fObj = os.statvfs(volName)

	app.logger.info("REMINDER: If the given volume name is not a filesystem, then statvfs returns the value of the filesystem to which this directory/file belongs too")
	# The next line uses in dict comprehension syntax "a: b for a in a's if a is something"
	return {k: getattr(fObj, k) for k in dir(fObj) if k.startswith('f_')}


# The main subroutine which calls all required methods and builds the complete dict
#
def collect_volume_statistics(volName):
	# The dict keys starts with a number so that it gets sorted accordingly
	volumeStatistics = {"3_time_details": {}, "4_size_details": {}}
	df_details = df_to_json(volName)
	stat_details = stat_to_json(volName)
	statvfs_details = statvfs_to_json(volName)

	volumeStatistics["3_time_details"]["modification_time"] = time.ctime(stat_details["st_mtime"])
	volumeStatistics["3_time_details"]["metadata_change_time"] = time.ctime(stat_details["st_ctime"])
	volumeStatistics["3_time_details"]["access_time"] = time.ctime(stat_details["st_atime"])

	volumeStatistics["4_size_details"]["total_size_in_mb"] = statvfs_details["f_frsize"] * statvfs_details["f_blocks"] / 1024 / 1024
	volumeStatistics["4_size_details"]["available_size_in_mb"] = statvfs_details["f_frsize"] * statvfs_details["f_bavail"] / 1024 / 1024

	volumeStatistics["2_inode"] = stat_details["st_ino"]

	volumeStatistics["1_df_output_details"] = df_details
	volumeStatistics["5_raw_stat_output"] = stat_details
	volumeStatistics["6_raw_statvfs_output"] = statvfs_details
	return volumeStatistics


# The microservice for '/'. Well this doesn't perform anything other than printing a welcome message and a help message
#
@app.route('/')
def hello_world():
	app.logger.info("No specific service running here. Just welcome message and a help message")
	return 'Welcome to Get Volume Statistics Microservice app!\nCall the endpoint /getVolumeStat with an argument of vol. For example: /getVolumeStat?vol=/home\n'


# The microservice for '/getVolumeStat'. Supposed to be called along with "?vol=<volname>" argument
#
@app.route('/getVolumeStat')
def get_volume_statistics():
	volName = request.args.get('vol')
	if not volName:
		app.logger.error("Volume name not provided as argument")
		return 'ERROR: Volume name was not provided as argument. Please call the endpoint /getVolumeStat with an argument of vol. For example: /getVolumeStat?vol=/home\n'


	if not path.exists(volName):
		app.logger.error("Provided volume name does not exist")
		return 'ERROR: Provided volume name does not exist\n'

	app.logger.info("Request for collecting volume statistics for "+volName+" received.")
	return jsonify(collect_volume_statistics(volName))


#
# If run directly
##

if __name__ == '__main__':
	app.run(port=5000)
