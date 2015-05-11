#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""deleteMessage.py: Delete a message from a collection in the R2DM service."""

__author__ = "Filip Lemic"
__copyright__ = "Copyright 2015, EVARILOS Project"

__version__ = "1.0.0"
__maintainer__ = "Filip Lemic"
__email__ = "lemic@tkn.tu-berlin.de"
__status__ = "Development"

import sys
import urllib2
import json
from generateURL import RequestWithMethod

# The URL where server listens
apiURL = 'http://localhost:5000/'

# The ID of the database
db_id = 'test_db'

# The ID of the collection in the database
coll_id = 'test_coll'

# The ID of the data
data_id = 'test_data'

req = RequestWithMethod(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id + '/collection/' + coll_id + '/message/' + data_id, 'DELETE', headers={"Content-Type": "application/json"})
resp = urllib2.urlopen(req)
response = json.loads(resp.read())
print response	