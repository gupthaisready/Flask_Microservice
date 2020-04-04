from flask import Flask, jsonify
import json

app = Flask(__name__)

def collect_volume_statistics():
	volStat = {"name": "/u01",
			   "size": 540,
			   "foo": "bar"}

	return volStat

@app.route('/')
def hello_world():
	return 'Welcome to Get Volume Statistics Microservice app!'

@app.route('/getVolumeStat')
def get_volume_statistics():
	return jsonify(collect_volume_statistics())

if __name__ == '__main__':
	app.run(port=5000)
