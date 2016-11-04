
import sys

# adding api to path
api_folder = "/home/pi/ISensitGateway/isensitgwapi/"
if api_folder not in sys.path:
    sys.path.insert(0, api_folder)

from isensit_sql import *

tables = ["beacon_table", "acc_beacon_table", "noise_sensor_table", "fd_sensor_table"];
print "1. Beacons"
print "2. Acc Beacons"
print "3. Noise Sensort"
print "4. Find Dust Sensor"
no = raw_input("Please choose the table need to be export: ")

while int(no) > len(tables):
    no = raw_input("Please choose the table need to be export: ")

table_name = tables[int(no) - 1]
print "Table chosen: ", table_name

filename = raw_input("Enter the name of the file: ")

db = ISensitGWMysql()
try:
    db.connect_to_db()
    data = db.read_all_data(table_name)
except Exception as e:
    print("Error in Aws Sender, reason: ", str(e))
else:
    if data is not None:
        print("uploading...", len(data))
        f = open(filename+".txt", "w")
        for d in data:
#           print d
            f.write(''.join('{}: {} '.format(key, val) for key, val in d.items()))
            f.write("\n")
        f.close()
        print "Data output Complete"
    else:
        print "No data found"
    db.close_db()

