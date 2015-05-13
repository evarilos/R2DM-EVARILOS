#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""change_coordinate.py: Change the metadata_id in each message."""

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
apiURL = 'http://localhost:5000/'

# The name of a database
db_id = 'test_metadata_db'

# The name of a collection in the database
coll_id = 'test_coll'

# The new metadata ID
new_metadata_id = 'test_metadata'

req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id  + '/collection/' + coll_id + '/message', headers={"Content-Type": "application/json"})
resp = urllib2.urlopen(req)
messages = json.loads(resp.read())

for i in messages.keys():
	data_id = str(messages[i]['data_id'])
	raw_data_collection = raw_data_pb2.RawRFReadingCollection() 
	req = RequestWithMethod(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id  + '/collection/' + coll_id + '/message/' + data_id, 'GET', headers={"Content-Type": "application/json"}, data = 'json')
	response = urllib2.urlopen(req)
	message = json.loads(response.read())

	message['metadata_id'] = new_metadata_id	
	json2pb(raw_data_collection, message)
	obj = raw_data_collection.SerializeToString()

	req = RequestWithMethod(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id + '/collection/' + coll_id + '/message/' + data_id, 'PUT', headers={"Content-Type": "application/x-protobuf"}, data = obj)
	resp = urllib2.urlopen(req)
	print json.loads(resp.read())



	