#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""getMessageList.py: Get a list of all messages in a collection in the R2DM service."""

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

# The URL where server listens
apiURL = 'http://localhost:5000/'

# The ID of the database
db_id = 'test_db'

# The ID of the collection in the database
coll_id = 'test_coll'

req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id  + '/collection/' + coll_id + '/message', headers={"Content-Type": "application/json"})
resp = urllib2.urlopen(req)
messages = json.loads(resp.read())

print messages
