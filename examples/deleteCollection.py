import sys
import urllib2
import json
from generateURL import RequestWithMethod

# This is an example of deleting a collection

# The URL where server listens
apiURL = 'http://localhost:5000/'

# The ID of the database
db_id = 'RSSI_fingerprints'

# The ID of the collection in the database
coll_id = 'RSSI_fingerprinting_TWIST_big_01'

req = RequestWithMethod(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id + '/collection/' + coll_id, 'DELETE', headers={"Content-Type": "application/json"})
resp = urllib2.urlopen(req)
response = json.loads(resp.read())
print response	