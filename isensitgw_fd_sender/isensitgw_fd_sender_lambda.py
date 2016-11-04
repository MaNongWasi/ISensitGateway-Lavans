import sys

# adding api to path
api_folder = "/home/pi/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)

from isensit_cloud import *
from isensit_sql import *
import datetime

jsonDict = {}
deviceInfoDict = {}
deviceValueDict = {}
row_count = 0
table_name = "fd_sensor_table"

uploader = ISensitCloud()
data = None
count = 0

while True:
    try:
        db = ISensitGWMysql()
        db.connect_to_db()
        data = db.read_first_data(table_name)
        if data is None:
            print("No data left")
        else:
            row_count = data["row_count"]
            deviceValueDict['pm'] = data["pm"]
            deviceValueDict['temp'] = data["temp"]
            deviceValueDict['hum'] = data["hum"]
            deviceValueDict['pm_hour'] = data["pm_hour"]
            deviceValueDict['created_at'] = str(data["created_at"])
            
            jsonDict['gatewayID'] = db.gatewayID
            jsonDict["device"] = deviceInfoDict
            jsonDict["values"] = deviceValueDict
            # data = json.dumps(deviceInfoDict, ensure_ascii=False)
	
	    print datetime.datetime.now()
            print(jsonDict)

    except Exception as e:
        print("Error in Aws Sender, reason: ", str(e))
    else:
        if data is not None:
            print("uploading...")
            db.delete_data(table_name, row_count)
            upload = uploader.post_data(jsonDict)

            if upload:
                print("upload successful, deleting row..")
                db.delete_data(table_name, row_count)

            else:
                print("Data was not uploaded reason: ")
                print(upload)
        db.close_db()
