#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""changeMessage.py: Changes the message in a collection in the R2DM service."""

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

# The URL where server listens
apiURL = 'http://localhost:5000/'

# The ID of the database
db_id = 'test_db'

# The ID of the collection in the database
coll_id = 'test_coll'

# The ID of the data
data_id = 'test_data_01'

obj = json.dumps({"metadata_id": 'test_metadata_01'})

req = RequestWithMethod(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id + '/collection/' + coll_id + '/message/' + data_id, 'PATCH', headers={"Content-Type": "application/json"}, data = obj)
resp = urllib2.urlopen(req)
print json.loads(resp.read())