import sys
import urllib2
import json

# This is an example of geting the list of the databases 

# The URL where server listens
apiURL = 'http://localhost:5000/'

req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database', headers={"Content-Type": "application/json"})
resp = urllib2.urlopen(req)
databases = json.loads(resp.read())
print databases.keys()