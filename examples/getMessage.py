#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""getMessage.py: Get a message from a collection in the R2DM service."""

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
from generateURL import RequestWithMethod

# The URL where server listens
apiURL = 'http://localhost:5000/'

# The ID of the database
db_id = 'test_db'

# The ID of the collection in the database
coll_id = 'test_coll'

# The ID of the data
data_id = 'test_data'

## Getting message as a protobuffer string
raw_data_collection = raw_data_pb2.RawRFReadingCollection() 
req = RequestWithMethod(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id  + '/collection/' + coll_id + '/message/' + data_id, 'GET', headers={"Content-Type": "application/json"}, data = 'protobuf')
response = urllib2.urlopen(req)
message = response.read()
raw_data_collection.ParseFromString(message)
print raw_data_collection

## Getting message as a json object
req = RequestWithMethod(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id  + '/collection/' + coll_id + '/message/' + data_id, 'GET', headers={"Content-Type": "application/json"}, data = 'json')
response = urllib2.urlopen(req)
message = response.read()
print message