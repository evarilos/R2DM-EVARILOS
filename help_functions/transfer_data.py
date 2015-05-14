#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""transfer_data.py: Transfer data from one collection to another."""

__author__ = "Filip Lemic"
__copyright__ = "Copyright 2015, EVARILOS Project"

__version__ = "1.0.0"
__maintainer__ = "Filip Lemic"
__email__ = "lemic@tkn.tu-berlin.de"
__status__ = "Development"

import sys
import urllib2
import json
import raw_data_pb2
from protobuf_json import json2pb
from generateURL import RequestWithMethod

# The URL where server listens
apiURL = 'http://localhost:5000/'

# The name of a database
db_id = 'test_db'

# The names of collections from which the data should be transfer 
coll_id = ['test_coll_1','test_coll_2']

# The name of a collection to which the data should be transfer 
coll_id_new = 'test_coll'

iteration = 0
for coll in coll_id:

	req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id  + '/collection/' + coll + '/message', headers={"Content-Type": "application/json"})
	resp = urllib2.urlopen(req)
	messages = json.loads(resp.read())

	for i in messages.keys():
		iteration = iteration + 1

		## Getting message as a json object
		data_id = str(messages[i]['data_id'])
		req = RequestWithMethod(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id  + '/collection/' + coll + '/message/' + data_id, 'GET', headers={"Content-Type": "application/json"}, data = 'json')
		response = urllib2.urlopen(req)
		message = json.loads(response.read())
		message['data_id'] = str(iteration)
		raw_data = raw_data_pb2.RawRFReadingCollection() 
		json2pb(raw_data, message)
		try:
			obj = raw_data.SerializeToString()
			req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id + '/collection/' + coll_id_new, headers={"Content-Type": "application/x-protobuf"}, data = obj)
			resp = urllib2.urlopen(req)
			print json.loads(resp.read())
		except:
			print "Error"
