#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""change_coordinate.py: Change the coordinate (X,Y or Z) in each message."""

__author__ = "Filip Lemic"
__copyright__ = "Copyright 2015, EVARILOS Project"

__version__ = "1.0.0"
__maintainer__ = "Filip Lemic"
__email__ = "lemic@tkn.tu-berlin.de"
__status__ = "Development"

import sys
import urllib2
from generateURL import RequestWithMethod
import json
import raw_data_pb2
from protobuf_json import json2pb

# The URL where server listens
apiURL = 'http://ebp.evarilos.eu:5000/'

# The name of a database
db_id = 'fine_granularity_twist'

# The name of a collection in the database
coll_id = 'macbook_training'

coordinate_file = 'coordinates.txt'

def get_coordinates(coordinate_file):
    f = open(coordinate_file)
    coordinates = {}

    lines = f.read().splitlines()

    for line_num in range(1,len(lines)):
        strings = lines[line_num].split(',')
    
        coordinates[strings[0]] = {}
        coordinates[strings[0]]['point_id'] = strings[0]
        coordinates[strings[0]]['coordinate_x'] = float(strings[2])
        coordinates[strings[0]]['coordinate_y'] = float(strings[3])
        coordinates[strings[0]]['room_label'] = strings[5].strip()
        
    return coordinates

if __name__ == '__main__':

	coordinates = get_coordinates(coordinate_file)

	req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id  + '/collection/' + coll_id + '/message', headers={"Content-Type": "application/json"})
	resp = urllib2.urlopen(req)
	messages = json.loads(resp.read())

	for i in messages.keys():
		data_id = messages[i]['data_id']
		raw_data_collection = raw_data_pb2.RawRFReadingCollection() 
		req = RequestWithMethod(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id  + '/collection/' + coll_id + '/message/' + data_id, 'GET', headers={"Content-Type": "application/json"}, data = 'json')
		response = urllib2.urlopen(req)
		message = json.loads(response.read())

		req = RequestWithMethod(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id + '/collection/' + coll_id + '/message/' + data_id, 'DELETE', headers={"Content-Type": "application/json"})
		resp = urllib2.urlopen(req)
		
		for i in message['raw_measurement']:
		
		# if coord_z == something -> change it
		# if i['receiver_location']['coordinate_z'] == 9.08: 
			i['receiver_location']['coordinate_z'] = 9.53
			i['receiver_location']['coordinate_x'] = coordinates[data_id]['coordinate_x']
			i['receiver_location']['coordinate_y'] = coordinates[data_id]['coordinate_y']
			i['receiver_location']['room_label'] = coordinates[data_id]['room_label']

		json2pb(raw_data_collection, message)
		obj = raw_data_collection.SerializeToString()

		req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id + '/collection/' + coll_id, headers={"Content-Type": "application/x-protobuf"}, data = obj)
		resp = urllib2.urlopen(req)
		print json.loads(resp.read())



	