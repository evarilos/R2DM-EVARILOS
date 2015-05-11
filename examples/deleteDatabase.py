#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""deleteDatabase.py: Delete a database in the R2DM service."""

__author__ = "Filip Lemic"
__copyright__ = "Copyright 2015, EVARILOS Project"

__version__ = "1.0.0"
__maintainer__ = "Filip Lemic"
__email__ = "lemic@tkn.tu-berlin.de"
__status__ = "Development"

from generateURL import RequestWithMethod
import sys
import urllib2
import json

# The URL where server listens
apiURL = 'http://localhost:5000/'

# The ID of the database
db_id = 'test_db'

req = RequestWithMethod(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id, 'DELETE', headers={"Content-Type": "application/json"})
resp = urllib2.urlopen(req)
response = json.loads(resp.read())
print response	