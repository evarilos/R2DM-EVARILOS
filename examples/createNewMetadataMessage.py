#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""createMetadataMessage.py: Creates an example metadata message in the R2DM service."""

__author__ = "Filip Lemic"
__copyright__ = "Copyright 2015, EVARILOS Project"

__version__ = "1.0.0"
__maintainer__ = "Filip Lemic"
__email__ = "lemic@tkn.tu-berlin.de"
__status__ = "Development"

import raw_metadata_pb2
from datetime import datetime
import urllib2
import json
import time
import sys

apiURL = 'http://ebp.evarilos.eu:5000/'
db_id = 'metadata'
coll_id = 'wifi_beacon_rssi_wilabt1'

metadata = raw_metadata_pb2.Metadata() 
metadata.data_id ='runtime'
metadata.metadata_id = '13'
metadata.testbed_id = 'w-iLab.t 1'
metadata.licence = 'http://opendatacommons.org/licenses/odbl/summary/'
metadata.timestamp_utc = int(time.mktime(datetime.utcnow().timetuple()))
metadata.scenario.receiver_description = 'Receiver is a WiFi-enabled Linux device.'
metadata.scenario.sender_description = 'Senders are all WiFi APs in the area of interest.'
metadata.scenario.environment_description = 'w-iLab.t 1 testbed - office environment with ply-wooden walls.'
metadata.scenario.experiment_description = 'Fingerprints are taken at uniformly distributed locations in the testbed environment.'
metadata.scenario.type_of_raw_data = 'At different locations the RSSI fingerprints have been taken. Each fingerprint consists of 20 scans of the wireless environment and RSSI values from beacon packets from all visible APs are taken.'
metadata.scenario.interference_description = 'This is an experiment without controlled interference. Measurements were done on a weekend afternoon.'
obj = metadata.SerializeToString()

req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id + '/collection/' + coll_id, headers={"Content-Type": "application/x-protobuf"}, data = obj)
resp = urllib2.urlopen(req)
print json.loads(resp.read())
