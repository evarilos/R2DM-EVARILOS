import sys
import urllib2
import json
from generateURL import RequestWithMethod

# This is an example of deleting a database

# The URL where server listens
apiURL = 'http://localhost:5000/'

# The ID of the database
db_id = 'metadata'

req = RequestWithMethod(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id, 'DELETE', headers={"Content-Type": "application/json"})
resp = urllib2.urlopen(req)
response = json.loads(resp.read())
print response	