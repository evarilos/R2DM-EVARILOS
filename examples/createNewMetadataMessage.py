#!/usr/bin/python
# -*- coding: utf-8 -*-

from generateURL import RequestWithMethod
from flask import jsonify
import raw_metadata_pb2
from datetime import datetime
import urllib
import urllib2
import json
import time
import sys

apiURL = 'http://localhost:5000/'
db_id = 'metadata'
coll_id = 'raw_RSSI'

metadata = raw_metadata_pb2.Metadata() 
metadata.data_id ='raw_RSSI_06'
metadata.metadata_id = 'RSSI_online_TWIST_with_Jamming_IEEE802154_01'
metadata.timestamp_utc = int(time.mktime(datetime.utcnow().timetuple()))
metadata.scenario.receiver_description = 'Receiver is a e MacBook Pro notebook with the AirPort Extreme network interface card (NIC).'
metadata.scenario.sender_description = 'Senders are all Wi-Fi APs in the area, while the APs specifically used further localization purposes have the SSID = CREW. There is four such devices, mounted on the corners of the 2nd floor of the TWIST testbed. The wireless APs used used for localization are TL-WDR4300 routers, with the fixed channel allocation scheme set on channel 11 (2462 MHz). The transmission power is set to 20 dBm (100 mW), and the traffic model is IEEE 802.11b.'
metadata.scenario.environment_description = 'TWIST testbed 2nd floor - Small to medium office environment with bricked walls.'
metadata.scenario.experiment_description = 'This mesurements are a runtime (online) survey for fingerprint based indoor localization. The testbed environment is divided into the grid area. Cells of the grid are selected according to the building footprints. Cells are the rectangles/squares of the sizes between 2.5 and 3.5 m. Small offices in the building are divided into 2 cells, bigger offices in 4 cells, while the biggest rooms (mostly laboratories) are divided into 6 cells. Fingerprints are taken on a randomly distributed positions in the testbed area.'
metadata.scenario.type_of_raw_data = 'At each location the RSSI fingerprint has been taken. Each fingerprint consists of 40 scans of the wireless environment and RSSI values from beacon packets from all visible APs are taken.'
metadata.scenario.interference_description = 'This is an experiment with controlled interference. The additional interference is created using a IEEE 802.15.4 carrier jammer application with the transmission power of 0 dBm (1 mW) on the channel 22 (2460 MHz). Meaurements were done in a weekend aferenoon and the uncontrolled interference level was monitored using WiSpy 2.4 tool.'
obj = metadata.SerializeToString()

req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id + '/collection/' + coll_id, headers={"Content-Type": "application/x-protobuf"}, data = obj)
resp = urllib2.urlopen(req)
print json.loads(resp.read())
