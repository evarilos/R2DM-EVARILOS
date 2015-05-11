#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""replaceMessage.py: Replaces a message in a collection in the R2DM service using HTTP PUT method."""

__author__ = "Filip Lemic"
__copyright__ = "Copyright 2015, EVARILOS Project"

__version__ = "1.0.0"
__maintainer__ = "Filip Lemic"
__email__ = "lemic@tkn.tu-berlin.de"
__status__ = "Development"

import sys
import urllib2
import raw_data_pb2
from wifiFingerprint import wifiFingerprint
from datetime import datetime
import time
import json
from generateURL import RequestWithMethod

# The URL where server listens
apiURL = 'http://localhost:5000/'

# The ID of the database
db_id = 'test_db'

# The ID of the collection in the database
coll_id = 'test_coll'

# The ID of the data
data_id = 'test_data'

NUMBER_OF_SCANS = 1

if __name__ == '__main__':
    
    raw_data_collection = raw_data_pb2.RawRFReadingCollection() 
    raw_data_collection.metadata_id = "1"
    raw_data_collection.data_id = "1"
    raw_data_collection.meas_number = NUMBER_OF_SCANS

    for scans in range(1, NUMBER_OF_SCANS + 1):
        fpf = wifiFingerprint()
        fpf.scan(1)
        fp = fpf.getFingerprint()
        for key in fp.keys():
            raw_data_reading = raw_data_collection.raw_measurement.add()
            x = datetime.utcnow()
            raw_data_reading.timestamp_utc = timestamp_utc = int(time.mktime(x.timetuple()))
            raw_data_reading.receiver_id = 'MacBook'
            raw_data_reading.receiver_location.coordinate_x = 1
            raw_data_reading.receiver_location.coordinate_y = 1
            raw_data_reading.receiver_location.coordinate_z = 1
            raw_data_reading.receiver_location.room_label = 'test'
            raw_data_reading.run_nr = scans
            raw_data_reading.sender_bssid = key
            raw_data_reading.sender_id = fp[key]['ssid']
            raw_data_reading.rssi = int(fp[key]['rssi'][0])
            raw_data_reading.channel = fp[key]['channel']

    obj = raw_data_collection.SerializeToString()

    req = RequestWithMethod(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id + '/collection/' + coll_id + '/message/' + data_id, 'PUT', headers={"Content-Type": "application/x-protobuf"}, data = obj)
    resp = urllib2.urlopen(req)
    print json.loads(resp.read())