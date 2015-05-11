import sys
import urllib2
import json

# This is an example of creating a new empty database for raw data.

# The URL where server listens
apiURL = 'http://localhost:5000/'

# Database name (or database ID)
db_id = 'raw_RSSI'

req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database', headers={"Content-Type": "application/json"}, data = db_id)
resp = urllib2.urlopen(req)
response = json.loads(resp.read())
print response	