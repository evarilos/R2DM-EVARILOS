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
db_id = 'metadata'
coll_id = 'test_coll'

metadata = raw_metadata_pb2.Metadata() 
metadata.data_id ='test_data'
metadata.metadata_id = 'dummy'  # has to be the same as the metadata_id in the dataset that is described with this metadata message
metadata.testbed_id = 'dummy'
metadata.licence = 'dummy'
metadata.timestamp_utc = int(time.mktime(datetime.utcnow().timetuple()))
metadata.scenario.receiver_description = 'dummy'
metadata.scenario.sender_description = 'dummy'
metadata.scenario.environment_description = 'dummy'
metadata.scenario.experiment_description = 'dummy'
metadata.scenario.type_of_raw_data = 'dummy'
metadata.scenario.interference_description = 'dummy'
obj = metadata.SerializeToString()

req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id + '/collection/' + coll_id, headers={"Content-Type": "application/x-protobuf"}, data = obj)
resp = urllib2.urlopen(req)
print json.loads(resp.read())
