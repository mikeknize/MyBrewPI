import os
import glob
import time
import ConfigParser
import subprocess
import RPi.GPIO as io 
import json
from pprint import pprint

io.setmode(io.BCM) 
config = ConfigParser.RawConfigParser()
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
power_pin = 15
io.setup(power_pin, io.OUT)
io.output(power_pin, False)
req_temp = 99
cur_temp = 0
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
	catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out,err = catdata.communicate()
	out_decode = out.decode('utf-8')
	lines = out_decode.split('\n')
	return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_f

# def update_temp(r_temp, c_temp):
# 	config.read('temp.ini')
# 	if config.has_section('Temperature'):
# 		r_temp = int(config.get('Temperature', 'req_temp'))
# 		print("ftemp {0}".format(r_temp))
# 	else:
# 		config.add_section('Temperature')
# 	config.set('Temperature', 'req_temp', r_temp)
# 	print("temp {0}".format(r_temp))
# 	config.set('Temperature', 'cur_temp', c_temp)
# 	with open('temp.ini', 'wb') as configfile:
# 		config.write(configfile)
# 	return r_temp
def update_temp(r_temp, c_temp):
	with open('temp_data.json', 'r') as data_file:    
		data = json.load(data_file)
		req_temp = int(data["req"])
		data["cur"] = c_temp
		print(int(data["high"]) < int(c_temp))
		if "high" in data and (int(data["high"]) < int(c_temp)):
			print("set high")
			data["high"] = c_temp
		elif "high" in data is False:
			data["high"] = c_temp
		print("ftemp {0}".format(req_temp))
		data_file.close()
	with open('temp_data.json', 'w') as data_file:
		json.dump(data, data_file)
		data_file.close()
		
	pprint(data)
	return req_temp

while True:
	cur_temp = c_temp = read_temp()
	req_temp = update_temp(req_temp, c_temp)
	print(c_temp)
	print(req_temp)
	if c_temp > (req_temp + .5):
		time.sleep(10);
		print("POWER ON")
		io.output(power_pin, True)
	elif c_temp <= (req_temp - .5):
		time.sleep(10);
		print("POWER OFF")
		io.output(power_pin, False)
	time.sleep(30)
