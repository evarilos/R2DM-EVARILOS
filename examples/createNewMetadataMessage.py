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

apiURL = 'http://localhost:5000/'
db_id = 'test_db_metadata'
coll_id = 'test_coll'

metadata = raw_metadata_pb2.Metadata() 
metadata.data_id ='test'
metadata.metadata_id = 'test'
metadata.timestamp_utc = int(time.mktime(datetime.utcnow().timetuple()))
metadata.scenario.receiver_description = 'test'
metadata.scenario.sender_description = 'test'
metadata.scenario.environment_description = 'test'
metadata.scenario.experiment_description = 'test'
metadata.scenario.type_of_raw_data = 'test'
metadata.scenario.interference_description = 'test'
obj = metadata.SerializeToString()

req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id + '/collection/' + coll_id, headers={"Content-Type": "application/x-protobuf"}, data = obj)
resp = urllib2.urlopen(req)
print json.loads(resp.read())
