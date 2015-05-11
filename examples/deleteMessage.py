import sys
import urllib2
import json
from generateURL import RequestWithMethod

# This is an example of deleting a message

# The URL where server listens
apiURL = 'http://localhost:5000/'

# The ID of the database
db_id = 'metadata'

# The ID of the collection in the database
coll_id = 'raw_RSSI'

# The ID of the data
data_id = 'raw_RSSI_01'

req = RequestWithMethod(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id + '/collection/' + coll_id + '/message/' + data_id, 'DELETE', headers={"Content-Type": "application/json"})
resp = urllib2.urlopen(req)
response = json.loads(resp.read())
print response	