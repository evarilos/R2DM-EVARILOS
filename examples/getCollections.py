#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""getCollections.py: get a list of all collections in a database in the R2DM service."""

__author__ = "Filip Lemic"
__copyright__ = "Copyright 2015, EVARILOS Project"

__version__ = "1.0.0"
__maintainer__ = "Filip Lemic"
__email__ = "lemic@tkn.tu-berlin.de"
__status__ = "Development"

import sys
import urllib2
import json

# The URL where server listens
apiURL = 'http://localhost:5000/'

# The ID of the database
db_id = 'test_db'

req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id  + '/collection', headers={"Content-Type": "application/json"})
resp = urllib2.urlopen(req)
collections = json.loads(resp.read())
print collections.keys()