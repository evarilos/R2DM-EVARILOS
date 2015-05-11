import sys
import urllib2
import json
import raw_rssi_pb2
from generateURL import RequestWithMethod

# This is an example of getting a message

# The URL where server listens
apiURL = 'http://localhost:5000/'

# The ID of the database
db_id = 'testDatabase'

# The ID of the collection in the database
coll_id = 'testCollection_new'

# The ID of th2 data
data_id = 'Loc1'

## Getting message as a protobuffer string
raw_rssi_collection = raw_rssi_pb2.RawRSSIReadingCollection() 
req = RequestWithMethod(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id  + '/collection/' + coll_id + '/message/' + data_id, 'GET', headers={"Content-Type": "application/json"}, data = 'protobuf')
response = urllib2.urlopen(req)
message = response.read()
raw_rssi_collection.ParseFromString(message)
print raw_rssi_collection

## Getting message as a json object
raw_rssi_collection = raw_rssi_pb2.RawRSSIReadingCollection() 
req = RequestWithMethod(apiURL + 'evarilos/raw_data/v1.0/database/' + db_id  + '/collection/' + coll_id + '/message/' + data_id, 'GET', headers={"Content-Type": "application/json"}, data = 'json')
response = urllib2.urlopen(req)
message = response.read()
print raw_rssi_collection