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
coll_id = 'wifi_beacon_rssi_hospital'

metadata = raw_metadata_pb2.Metadata() 
metadata.data_id ='training'
metadata.metadata_id = '1'
metadata.testbed_id = 'TWIST'
metadata.licence = 'http://opendatacommons.org/licenses/odbl/summary/'
metadata.timestamp_utc = int(time.mktime(datetime.utcnow().timetuple()))
metadata.scenario.receiver_description = 'Receiver is a e MacBook Pro notebook with the AirPort Extreme network interface card (NIC).'
metadata.scenario.sender_description = 'Senders are all WiFi APs in the area, while the APs specifically used for localization purposes have the SSID = tplink. There are four such devices, mounted in the 2nd floor of the TWIST testbed. The wireless APs used used for localization are TL-WDR4300 routers, with the fixed channel allocation scheme set on channel 11 (2462 MHz). The transmission power is set to 20 dBm (100 mW), and the traffic model is IEEE 802.11b.'
metadata.scenario.environment_description = 'TWIST testbed 2nd floor - Small to medium office environment with bricked walls.'
metadata.scenario.experiment_description = 'The testbed environment is divided into the grid area. Cells of the grid are selected according to the building footprint. Cells are the rectangles/squares of the sizes between 2 and 3m. Small offices in the building are divided into 2 cells, bigger offices in 4 cells, while the biggest rooms (mostly laboratories) are divided into 6 cells. Fingerprints are taken in a center of each cell.'
metadata.scenario.type_of_raw_data = 'At different locations the RSSI fingerprints have been taken. Each fingerprint consists of 50 scans of the wireless environment and RSSI values from beacon packets from all visible APs are taken.'
metadata.scenario.interference_description = 'This is an experiment without controlled interference. Measurements were done in a weekend afternoon and the interference level was monitored using a WiSpy 2.4 device.'
obj = metadata.SerializeToString()

req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id + '/collection/' + coll_id, headers={"Content-Type": "application/x-protobuf"}, data = obj)
resp = urllib2.urlopen(req)
print json.loads(resp.read())
