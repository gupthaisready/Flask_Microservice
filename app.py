from flask import Flask, jsonify, request
import json
import os
import subprocess
import shlex
import time

app = Flask(__name__)

def df_to_json(volName: str) -> dict:
	df_array = [shlex.split(x) for x in subprocess.check_output(["df", "-h"], universal_newlines=True).rstrip().split('\n')]
	df_json = {}
	for each_row in df_array: df_json[each_row[5]] = { "filesystem": each_row[0], "total_size": each_row[1], "used_size": each_row[2], "available_size": each_row[3], "used_percent": each_row[4] }
	if volName in df_json: 
		return {volName: df_json[volName]}
	else:
		return {volName: "Not a filesystem"}


def stat_to_json(volName: str) -> dict:
	sObj = os.stat(volName)
	return {k: getattr(sObj, k) for k in dir(sObj) if k.startswith('st_')}

def statvfs_to_json(volName: str) -> dict:
	fObj = os.statvfs(volName)
	return {k: getattr(fObj, k) for k in dir(fObj) if k.startswith('f_')}

def collect_volume_statistics(volName):
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

@app.route('/')
def hello_world():
	return 'Welcome to Get Volume Statistics Microservice app!'

@app.route('/getVolumeStat')
def get_volume_statistics():
	volName = request.args.get('vol')
	return jsonify(collect_volume_statistics(volName))

if __name__ == '__main__':
	app.run(port=5000)
