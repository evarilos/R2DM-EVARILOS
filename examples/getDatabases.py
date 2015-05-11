#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""getDatabases.py: Get a list of databases in the R2DM service."""

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

req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database', headers={"Content-Type": "application/json"})
resp = urllib2.urlopen(req)
databases = json.loads(resp.read())
print databases.keys()