import sys
import urllib2
import raw_rssi_pb2
from wifiFingerprint import wifiFingerprint
from datetime import datetime
import time
import json
from generateURL import RequestWithMethod

# This is an example of replacing the message using PUT

# The URL where server listens
apiURL = 'http://localhost:5000/'

# The ID of the database
db_id = 'testDatabase'

# The ID of the collection in the database
coll_id = 'testCollection_new'

# The ID of teh data
data_id = 'Loc2'

NUMBER_OF_SCANS = 1

if __name__ == '__main__':
    
    raw_rssi_collection = raw_rssi_pb2.RawRSSIReadingCollection() 
    raw_rssi_collection.receiver_id = 'MacBook'
    raw_rssi_collection.metadata_id = 1
    raw_rssi_collection.data_id = "Loc1"
    raw_rssi_collection.location.coordinate_x = 1
    raw_rssi_collection.location.coordinate_y = 1
    raw_rssi_collection.location.coordinate_z = 1
    raw_rssi_collection.location.room_label = 'FT423'
    
    for scans in range(1, NUMBER_OF_SCANS + 1):
        fpf = wifiFingerprint()
        fpf.scan(1)
        fp = fpf.getFingerprint()
        for key in fp.keys():
            raw_rssi_reading = raw_rssi_collection.rawRSSI.add()
            x = datetime.utcnow()
            raw_rssi_reading.timestamp_utc = timestamp_utc = int(time.mktime(x.timetuple()))
            raw_rssi_reading.run_nr = scans
            raw_rssi_reading.sender_bssid = key
            raw_rssi_reading.sender_ssid = fp[key]['ssid']
            raw_rssi_reading.rssi = int(fp[key]['rssi'][0])
            raw_rssi_reading.channel = fp[key]['channel']

    obj = raw_rssi_collection.SerializeToString()

    req = RequestWithMethod(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id + '/collection/' + coll_id + '/message/' + data_id, 'PUT', headers={"Content-Type": "application/x-protobuf"}, data = obj)
    resp = urllib2.urlopen(req)
    print json.loads(resp.read())