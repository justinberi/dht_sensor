#!/usr/bin/python

import Adafruit_DHT
import datetime
import time

#import wandb
#wandb.init(project="ceiling_temperature")

# Sensor should be set to Adafruit_DHT.DHT11,
# Adafruit_DHT.DHT22, or Adafruit_DHT.AM2302.
sensor = Adafruit_DHT.DHT22

pins = [17, 4]
path = "data_log.csv"

def get_readings(pin):
	# Try to grab a sensor reading.  Use the read_retry method which will retry up
	# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	# Note that sometimes you won't get a reading and
	# the results will be null (because Linux can't
	# guarantee the timing of calls to read the sensor).
	# If this happens try again!
	if humidity is not None and temperature is not None:
		now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
		return now,pin,temperature,humidity
	else:
		print('Failed to get reading. Try again!')
		return None

# Check if data exists if it does then append else headers
from pathlib import Path

my_file = Path("/home/pi/dht_sensor/data.csv")
if not my_file.is_file():
	with open(my_file, "w") as f:
		f.write("date,pin,temperature,humidity\n")

while True:
	for p in pins:
		data = get_readings(p)

#		d = {}
#		d["time"] = data[0]
#		d["temperature_"+str(data[1])] = data[2]
#		d["humidity_"+str(data[1])] = data[3]
#		wandb.log(d)

		with open(my_file, "a") as f:
			strdata = '{},{},{},{}'.format(*data)
			f.write(strdata+"\n")
		time.sleep(0.1)
	time.sleep(60*30)
#	time.sleep(1)
