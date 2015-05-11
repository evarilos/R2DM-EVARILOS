import sys
import urllib2
import json

# This is an example of getting messages from the collection

# The URL where server listens
apiURL = 'http://localhost:5000/'

# The ID of the database
db_id = 'testDatabase'

# The ID of the collection in the database
coll_id = 'testCollection_new'

# The ID of teh data
data_id = 'Loc1'

req = urllib2.Request(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id  + '/collection/' + coll_id + '/message', headers={"Content-Type": "application/json"})
resp = urllib2.urlopen(req)
messages = json.loads(resp.read())

print "Location label:"
for i in messages.keys():
	print messages[i]['data_id']

print "Metadata label:"
for i in messages.keys():
	print messages[i]['metadata_id']	

print "ID given by the database:"
for i in messages.keys():
	print messages[i]['_id']	