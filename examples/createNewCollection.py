import sys
import urllib2
import json

# This is an example of creating a new empty database for raw data.

# The URL where server listens
apiURL = 'http://localhost:5000/'

# The ID of the database
db_id = 'RSSI_fingerprints'

# The ID of the collection in the database
coll_id = 'RSSI_fingerprinting_TWIST_big_01'

req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id  + '/collection', headers={"Content-Type": "application/json"}, data = coll_id)
resp = urllib2.urlopen(req)
response = json.loads(resp.read())
print response	