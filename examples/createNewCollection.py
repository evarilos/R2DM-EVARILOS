#!/usr/bin/env python

"""createNewCollection.py: Creates new collection in the R2DM service."""

__author__ = "Filip Lemic"
__copyright__ = "Copyright 2014, EVARILOS Project"

__version__ = "1.0.0"
__maintainer__ = "Filip Lemic"
__email__ = "lemic@tkn.tu-berlin.de"
__status__ = "Development"

import sys
import urllib2
import json

# This is an example of creating a new empty database for raw data.

# The URL where server listens
apiURL = 'http://localhost:5000/'

# The ID of the database
db_id = 'test_db'

# The ID of the collection in the database
coll_id = 'test_coll'

req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id  + '/collection', headers={"Content-Type": "application/json"}, data = coll_id)
resp = urllib2.urlopen(req)
response = json.loads(resp.read())
print response	