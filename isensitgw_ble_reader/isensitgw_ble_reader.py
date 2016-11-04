#!/usr/bin/python
import sys
# adding api to path
api_folder = "/home/pi/ISensitGateway/isensitgwapi/" 
if api_folder not in sys.path:
    sys.path.insert(0, api_folder) 
from isensit_device_adapter import * 
from lib.blescan import * 
import bluetooth._bluetooth as bluez 
from isensit_sql import * 
import time 
import threading 
import datetime 

dev_id = 0 
rssi = 0
cal_pitch = 0 
total_lift = 0 
bad_lift = 0
row_count = 0 
table_name = "acc_beacon_table" 
total_count = 0
small_count = 0
middle_count = 0 
large_count = 0

def get_lift(beacon_id, degreex, degreey, degreez, total, rssi, accx, accy, accz):
#    db.connect_to_db()
    old_json = db.read_last_acc_beacon_data(table_name, int(beacon_id.strip('\0')))
    if old_json is None:
	old_degree = 0
	state = 0
	row_count = 0
        total_lift = 0
        bad_lift = 0
        last_degreez = 0
	small_count = 0
	middle_count = 0
	large_count = 0
        print ("--")
    else:
        old_degree = old_json["beacon_accz"]
        state = old_json["state"]
        row_count = old_json["row_count"]
        total_lift = old_json['total_lift']
        bad_lift = old_json['bad_lift']
	small_count = old_json['small_count']
	middle_count = old_json['middle_count']
	large_count = old_json['large_count']
#        old_json = db.read_last_acc_beacon_data(table_name, int(beacon_id.strip('\0')))
    
    print (bad_lift, total_lift)
    print ("++")
#    print "old degree ", old_degree
    print "state ", state
    print "row_count ", row_count

    if old_degree is None:
	old_degree = 0
    if state is None:
	state = 0
    if row_count is None:
	row_count = 0


    if degreez < 25 and degreez > -40:
	print "straight ", small_count
	small_count = small_count + 1
	middle_count = 0
	large_count = 0
	if small_count >4 and state != 0:
	    state = 0
            small_count = 0
	
    if degreez >= 25:
        small_count = 0
        middle_count = middle_count + 1
	print "middle count ", middle_count, " large_count ", large_count
        if middle_count > 4 and state ==0 :
   	    state = 1
            middle_count = 0
	    total_lift = total_lift + 1
		
    if degreez > 80:
	small_count = 0
	large_count = large_count + 1
	print "large count ", large_count
	if large_count > 4 and state != 2:
	    state = 2
            large_count = 0
	    bad_lift = bad_lift + 1 	    

    if degreez <= 80: 
	large_count =0

    currentt = datetime.datetime.now()
    db.insert_acc_beacon_data(int(beacon_id.strip('\0')), accx, accy, accz, rssi, bad_lift, total_lift, state, currentt, small_count, middle_count, large_count)
#    if row_count > 0:
#        db.delete_data(table_name, row_count)
    db.close_db()
#    print currenttime
    print "id ", beacon_id
    print "total_lift ", total_lift
    print "bad_lift ", bad_lift
    
def get_degree(r, total):
    	id = r["device_info"]["ID"][0]
        accx = float(r["values"]["ACCX"][0])
        accy = float(r["values"]["ACCY"][0])
        accz = float(r["values"]["ACCZ"][0])
        rssi = r["values"]["RSSI"][0]

#	db.connect_to_db()
	cal_pitch = db.read_cal_val(id)
#	db.close_db()
	print id, " ", cal_pitch
	if cal_pitch is None:
	    cal_pitch = 20

        degreex = getDegree(accx, accy, accz, cal_pitch, accx)
        degreey = getDegree(accy, accx, accz, cal_pitch, accx)
        degreez = getDegree(accz, accx, accy, cal_pitch, accx)
	print datetime.datetime.now(), ": ", degreez
	get_lift(id, degreex, degreey, degreez, total, rssi, accx, accy, accz) 

sock = hci_start_scan(dev_id) 
try:
    # initialize database reader
    db = ISensitGWMysql()
#    db.connect_to_db()
    start_time = db.config_data.get_start_time()
    end_time = db.config_data.get_end_time()
   # print(sleeptime)
except Exception as e:
    print("Error in initializing db, reason: ", str(e))
    running = False
    exit(-1)

while True:
    returnedList = parse_events(sock)
    if returnedList is not None:
        if returnedList is not False:
            db.connect_to_db()
            get_degree(returnedList, total_count)
