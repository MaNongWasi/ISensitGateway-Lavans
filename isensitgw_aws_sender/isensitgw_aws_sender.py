#from __future__ import print_function # Python 2/3 compatibility
import time
from decimal import *
import sys
import datetime

# adding api to path
api_folder = "/home/pi/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)

from isensit_sql import *
from isensit_dynamo import *
import datetime

deviceInfoDict = {}
deviceValueDict = {}
row_count = 0

data = None
count = 0
table_name = "acc_beacon_table"
device = "Acc"

def half_hour():
    currenttime = datetime.datetime.now()
    return currenttime.minute == 00 or currenttime.minute == 30


def working():
    currenttime = datetime.datetime.now()
    currentdate = currenttime.strftime("%Y-%m-%d")
    start_t = datetime.datetime.strptime(currentdate + start_time, "%Y-%m-%d %H:%M:%S")
    end_t = datetime.datetime.strptime(currentdate + end_time, "%Y-%m-%d %H:%M:%S")
    today = currenttime.weekday()
    return currenttime > start_t and currenttime < end_t and today < 5


#while True:
def upload_data():
    try:
    	db.connect_to_db()
    	data = db.read_distinct_acc_beacon_data()
    	print(data)
    	if data is None:
            print("No data left")
    	else:
	    total_total = 0
	    bad_total = 0
	    for beacon_id in data:
	        id = beacon_id.values()[0]
	        if id is not None:
	            d = db.read_last_acc_beacon_data(table_name, id)
		    print(d)
                    row_count = d["row_count"]
                    deviceInfoDict['ID'] = str(d["beacon_id"])
                    deviceInfoDict['sensor'] = device
		    deviceValueDict['accx'] = Decimal(d['beacon_accx']).quantize(Decimal("0.001"))
             	    deviceValueDict['accy'] = Decimal(d['beacon_accy']).quantize(Decimal("0.001"))
            	    deviceValueDict['accz'] = Decimal(d['beacon_accz']).quantize(Decimal("0.001"))
		    deviceValueDict['rssi'] = d['beacon_rssi']
		    deviceValueDict['total_lift'] = d['total_lift']
            	    deviceValueDict['bad_lift'] = d['bad_lift']
	  	    deviceValueDict['upload_at'] = str(datetime.datetime.now())
		    created_at = str(d['created_at'])
#            	    deviceValueDict['created_at'] = str(d["created_at"])

                    dydb.insert_data(created_at, deviceInfoDict, deviceValueDict)
                    dydb.insert_user_data(str(d["beacon_id"]), deviceInfoDict, deviceValueDict, created_at)
		
	            total_total = total_total + d['total_lift']
		    bad_total = bad_total + d['bad_lift']

##		     db.delete_data(table_name, row_count)
		    db.delete_acc_beacon_data(table_name, id, row_count)
       	 	    print("upload successful, deleting row..")
	
            deviceValueDict['bad_lift'] =  bad_total
            deviceValueDict['total_lift'] = total_total
	
            dydb.insert_to_next_table(deviceInfoDict, deviceValueDict)
	   	
    except Exception as e:
        print("Error in Aws Sender, reason: ", str(e))
    else:
#        if data is not None:
#            print("uploading...")
#            upload = uploader.post_data(jsonDict)

#            if upload:
#                print("upload successful, deleting row..")
#                db.delete_data(table_name, row_count)

#            else:
#                print("Data was not uploaded reason: ")
#                print(upload)
        db.close_db()


try:
    db = ISensitGWMysql()
    start_time = db.config_data.get_start_time()
    end_time = db.config_data.get_end_time()
#    print(db.config_data.get_dynamodb_table_person())
    dydb = ISensitDynamodb(db.gatewayID, db.config_data.get_dynamodb_table(), db.config_data.get_dynamodb_table_save(), db.config_data.get_dynamodb_table_person(), device)
except Exception as e:
    print("Error in ISensitDynamodb, reason: ", str(e))

while True:
    if working():
	if half_hour():
            upload_data()
	else:
	    print("not half hour")
	    time.sleep(60)
    else:
        print("not working hour")

