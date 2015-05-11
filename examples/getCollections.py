import sys
import urllib2
import json

# This is an example of geting the list of collections in the database

# The URL where server listens
apiURL = 'http://localhost:5000/'

# The ID of the database
db_id = 'testDatabase'

req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id  + '/collection', headers={"Content-Type": "application/json"})
resp = urllib2.urlopen(req)
collections = json.loads(resp.read())
print collections.keys()