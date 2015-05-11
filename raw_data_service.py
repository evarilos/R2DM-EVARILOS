import protobuf_json
from flask import Flask, jsonify
from flask import Response
from flask import abort
from flask import make_response
from flask import request
from pymongo import Connection
from functools import wraps
from flask import url_for
import raw_data_pb2
import raw_metadata_pb2
import json
import urllib2
import pymongo
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

def crossdomain(origin=None, methods=None, headers=None,
                max_age=201600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

app = Flask(__name__)

#######################################################################################################
# Home - Hello World! I'm alive!!!!!
#######################################################################################################
@app.route("/")
@crossdomain(origin='*')
def hello():
    response = {'EVARILOS welcomes you!': 'This is a prototype of the webservices for the EVARILOS project',
                'Databases': url_for("databases", _external = True)}
    return json.dumps(response)


#######################################################################################################
# Task 1: Get the list of all databases [GET]
#######################################################################################################
@app.route('/evarilos/raw_data/v1.0/database', methods = ['GET'])
@crossdomain(origin='*')
def databases():

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 27017)
    except:
        return json.dumps("Unable to connect to the database!")
      
    db_names = connection.database_names() 
    db_list = {}
    for iter_id in db_names:
        if iter_id != 'local':
            if iter_id != 'admin':
                db_list[iter_id] = url_for("database", db_id = iter_id, _external = True)
    return json.dumps(db_list)


#######################################################################################################
# Task 2: Get the list of all collections in the database [GET]
#######################################################################################################
@app.route('/evarilos/raw_data/v1.0/database/<db_id>/collection', methods = ['GET'])
@crossdomain(origin='*')
def database(db_id):

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 27017)
    except:
        return json.dumps("Unable to connect to the database!")
    
    db_names = connection.database_names()
    if db_id in db_names:
        db = connection[db_id]
    else:
        return json.dumps("No such database!")

    coll_names = db.collection_names()
    coll_list = {}
    for iter_id in coll_names:
        if iter_id != 'system.indexes':
            coll_list[iter_id] = url_for("collection", db_id = db_id, coll_id = iter_id, _external = True)
    return json.dumps(coll_list)


#######################################################################################################
# Task 3: Get the list of messages description from the collection [GET]
#######################################################################################################
@app.route('/evarilos/raw_data/v1.0/database/<db_id>/collection/<coll_id>/message', methods = ['GET'])
@crossdomain(origin='*')
def collection(db_id, coll_id):

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 27017)
    except:
        return json.dumps("Unable to connect to the database!")
      

    db_names = connection.database_names()
    if db_id in db_names:
        db = connection[db_id]
    else:
        return json.dumps("No such database!")  
    
    coll_names = db.collection_names()
    if coll_id in coll_names:
        collection = db[coll_id]
    else:
        return json.dumps("No such collection in the database!")
    
    try:
        message_collection = collection.find({})
    except:
        return json.dumps("Unable to read data from the collection!")
    
    message_collection_list = {}
    message_collection_list_full = list(message_collection)
    
    for i in range(0,len(message_collection_list_full)):
        message_collection_list[i] = {}
        message_collection_list[i]['_id'] = str(message_collection_list_full[i]['_id'])
        message_collection_list[i]['data_id'] = message_collection_list_full[i]['data_id']
        message_collection_list[i]['metadata_id'] = message_collection_list_full[i]['metadata_id']
        message_collection_list[i]['URI'] = url_for("message", db_id = db_id, coll_id = coll_id, data_id = message_collection_list_full[i]['data_id'], _external = True)

    return json.dumps(message_collection_list)


#######################################################################################################
# Task 4: Get the message from the collection [GET]
#######################################################################################################
@app.route('/evarilos/raw_data/v1.0/database/<db_id>/collection/<coll_id>/message/<data_id>', methods = ['GET'])
@crossdomain(origin='*')
def message(db_id, coll_id, data_id): 

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 27017)
    except:
        return json.dumps("Unable to connect to the database!")
      
    db = connection[db_id]   
    collection = db[coll_id]
    
    try:
        message_collection = collection.find_one({'data_id':data_id})
    except:
        return json.dumps("Unable to read data from the collection!")
    
    if message_collection is None:
        return json.dumps("No data with this ID in the collection!")
    
    message_collection['_id'] = str(message_collection['_id'])

    if request.data == 'protobuf':
        try:
            pb_message = protobuf_json.json2pb(raw_data_pb2.RawRFReadingCollection(), message_collection)
            pb_message = protobuf_json.json2pb(raw_metadata_pb2.Metadata(), message_collection)
        except:
            return json.dumps("Unable to read message from the collection!")
        pb_message_string = pb_message.SerializeToString()
        return pb_message_string
    else:
        return json.dumps(message_collection)


#######################################################################################################
# Task 5: Add a message into the collection [POST]
#######################################################################################################
@app.route('/evarilos/raw_data/v1.0/database/<db_id>/collection/<coll_id>', methods = ['POST'])
@crossdomain(origin='*')
def store_message(db_id, coll_id):

    detect_message = 0
    try:
        raw_data_collection = raw_data_pb2.RawRFReadingCollection()
        raw_data_collection.ParseFromString(request.data)
        detect_message = 1
    except:
        try:
            raw_metadata = raw_metadata_pb2.Metadata()
            raw_metadata.ParseFromString(request.data)
            detect_message = 2
        except:
            return json.dumps('Message is not well formated!')
    
    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 27017)
    except:
        return json.dumps("Unable to connect to the database!")

    db_names = connection.database_names()
    if db_id in db_names:
        db = connection[db_id]
    else:
        return json.dumps("No such database!")  
    
    coll_names = db.collection_names()
    if coll_id in coll_names:
        collection = db[coll_id]
    else:
        return json.dumps("No such collection in the database!")
    
    if detect_message == 1:
        try:
            collection.insert(protobuf_json.pb2json(raw_data_collection))
        except:
            return json.dumps("Unable to store data into the database!")
    else :
        try:
            collection.insert(protobuf_json.pb2json(raw_metadata))
        except:
            return json.dumps("Unable to store data into the database!")

    return json.dumps('Data stored!')

#######################################################################################################
# Task 6: Creating a new collection in the database [POST]
#######################################################################################################
@app.route('/evarilos/raw_data/v1.0/database/<db_id>/collection', methods = ['POST'])
@crossdomain(origin='*')
def create_collection(db_id):
    
    coll_id = request.data

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 27017)
    except:
        return json.dumps("Unable to connect to the database!")

    db_names = connection.database_names()
    if db_id in db_names:
        db = connection[db_id]
    else:
        return json.dumps("No such database!")  
    
    coll_names = db.collection_names()
    if coll_id in coll_names:
        return json.dumps("Collection already exists!")
    
    try:
        db.create_collection(coll_id)
    except:
        return json.dumps("Unable to create a collection")

    return json.dumps('Collection successfully created!')

#######################################################################################################
# Task 7: Creating a new database [POST]
#######################################################################################################
@app.route('/evarilos/raw_data/v1.0/database', methods = ['POST'])
@crossdomain(origin='*')
def create_database():
    
    db_id = request.data

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 27017)
    except:
        return json.dumps("Unable to connect to the database!")

    db_names = connection.database_names()
    if db_id in db_names:
        return json.dumps("Database already exists!")  
    
    try:
        db = connection[db_id]
        coll = db.create_collection('test_tmp')
    except:
        return json.dumps("Unable to create new database")

    db.test_tmp.drop()
    return json.dumps('Database successfully created!')


#######################################################################################################
# Task 8: Delete the database [DELETE]
#######################################################################################################
@app.route('/evarilos/raw_data/v1.0/database/<db_id>', methods = ['DELETE'])
# @basic_auth.required
@crossdomain(origin='*')
def delete_database(db_id):

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 27017)
    except:
        return json.dumps("Unable to connect to the database!")


    db_names = connection.database_names()
    if db_id not in db_names:
        return json.dumps("Database doesn't exist!")  
    
    try:
        connection.drop_database(db_id)
    except:
        return json.dumps("Unable to delete the database")

    return json.dumps('Database successfully deleted!')


#######################################################################################################
# Task 9: Delete the collection from the database [DELETE]
#######################################################################################################
@app.route('/evarilos/raw_data/v1.0/database/<db_id>/collection/<coll_id>', methods = ['DELETE'])
@crossdomain(origin='*')
def delete_collection(db_id, coll_id):

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 27017)
    except:
        return json.dumps("Unable to connect to the database!")


    db_names = connection.database_names()
    if db_id not in db_names:
        return json.dumps("Database doesn't exist!")  
    
    db = connection[db_id]
    coll_names = db.collection_names()
    if coll_id not in coll_names:
        return json.dumps("Collection doesn't exist!")  

    try:
        db.drop_collection(coll_id)
    except:
        return json.dumps("Unable to delete the collection")

    return json.dumps('Collection successfully deleted!')


#######################################################################################################
# Task 10: Delete the mesage from the collection [DELETE]
#######################################################################################################
@app.route('/evarilos/raw_data/v1.0/database/<db_id>/collection/<coll_id>/message/<data_id>', methods = ['DELETE'])
@crossdomain(origin='*')
def delete_message(db_id, coll_id, data_id):

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 27017)
    except:
        return json.dumps("Unable to connect to the database!")

    db_names = connection.database_names()
    if db_id not in db_names:
        return json.dumps("Database doesn't exist!")  
    
    db = connection[db_id]
    coll_names = db.collection_names()
    if coll_id not in coll_names:
        return json.dumps("Collection doesn't exist!")  

    collection = db[coll_id]
    try:
        collection.remove({"data_id": data_id})
    except:
        return json.dumps("Unable to delete the message")

    return json.dumps('Message successfully deleted!')

#######################################################################################################
# Task 11: Replace the message [PUT]
#######################################################################################################
@app.route('/evarilos/raw_data/v1.0/database/<db_id>/collection/<coll_id>/message/<data_id>', methods = ['PUT'])
@crossdomain(origin='*')
def replace_message(db_id, coll_id, data_id):

    raw_data_collection = raw_data_pb2.RawRFReadingCollection()
    raw_metadata = raw_metadata_pb2.Metadata()

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 27017)
    except:
        return json.dumps("Unable to connect to the database!")

    detect_message = 0
    try:
        raw_data_collection.ParseFromString(request.data)
        detect_message = 1
    except:
        try:
            raw_metadata.ParseFromString(request.data)
            detect_message = 2
        except:
            return json.dumps('Message is not well defined!')
    
    db_names = connection.database_names()
    if db_id not in db_names:
        return json.dumps("Database doesn't exist!")  
    
    db = connection[db_id]
    coll_names = db.collection_names()
    if coll_id not in coll_names:
        return json.dumps("Collection doesn't exist!")  

    collection = db[coll_id]
    
    try:
        message_collection = collection.find_one({'data_id':data_id})
    except:
        return json.dumps("Unable to read data from the collection!")
    

    if message_collection is None:
        return json.dumps("No data with this ID in the collection!")

    message_collection['_id'] = str(message_collection['_id'])
    message_backup = message_collection

    try:
        collection.remove({'data_id':data_id})
    except:
        collection.insert(message_backup)
        return json.dumps("Unable to read data from the database!")

    if detect_message == 1:
        try:
            collection.insert(protobuf_json.pb2json(raw_data_collection))
        except:
            collection.insert(message_backup)
            return json.dumps("Unable to store data into the collection!")
    else:
        try:
            collection.insert(protobuf_json.pb2json(raw_metadata))
        except:
            collection.insert(message_backup)
            return json.dumps("Unable to store data into the collection!")

    return json.dumps('Message successfully replaced!')


#######################################################################################################
# Task 12: Change the message parameters [PATCH]
#######################################################################################################
@app.route('/evarilos/raw_data/v1.0/database/<db_id>/collection/<coll_id>/message/<data_id>', methods = ['PATCH'])
@crossdomain(origin='*')
def change_message(db_id, coll_id, data_id):

    new_message_parameters = json.loads(request.data)
        
    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 27017)
    except:
        return json.dumps("Unable to connect to the database!")

    db_names = connection.database_names()
    if db_id not in db_names:
        return json.dumps("Database doesn't exist!")  
    
    db = connection[db_id]
    coll_names = db.collection_names()
    if coll_id not in coll_names:
        return json.dumps("Collection doesn't exist!")  

    collection = db[coll_id]
    try:
        message_collection = collection.find_one({'data_id':data_id})
    except:
        return json.dumps("Unable to read data from the collection!")

    if message_collection is None:
        return json.dumps("No data with this ID in the collection!")

    message_collection['_id'] = str(message_collection['_id'])
    message_backup = message_collection

    for key in new_message_parameters.keys():   
        message_collection[key] = new_message_parameters[key]

    try:
        collection.remove({'data_id': data_id})
        collection.insert(message_collection)
    except:
        collection.insert(message_backup)
        return json.dumps("Unable to store data into the database!")


    return json.dumps('Message successfully replaced!')


#######################################################################################################
# Task 13: Change the collection name [PATCH]
#######################################################################################################
@app.route('/evarilos/raw_data/v1.0/database/<db_id>/collection/<coll_id>', methods = ['PATCH'])
@crossdomain(origin='*')
def change_collection(db_id, coll_id):

    new_name = request.data

    # Connect to the database MongoDB
    try:
        connection = Connection('localhost', 27017)
    except:
        return json.dumps("Unable to connect to the database!")

    db_names = connection.database_names()
    if db_id not in db_names:
        return json.dumps("Database doesn't exist!")  
    
    db = connection[db_id]
    coll_names = db.collection_names()
    if coll_id not in coll_names:
        return json.dumps("Collection doesn't exist!")  
    if new_name in coll_names:
        return json.dumps("New name already exist!")

    collection = db[coll_id]
    try:
        collection.rename(new_name)
    except:
        return json.dumps("Unable to change the name of the collection!")
    return json.dumps("Collection's name changed!")
#######################################################################################################
# Task 14: Change the database name [PATCH]
#######################################################################################################

#######################################################################################################
# Additional help functions
#######################################################################################################

# Error handler
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404) 

# Creating the URIs
def make_public_task(function):
    new_function = {}
    for field in function:
        if field == 'id':
            new_function['uri'] = url_for('get_function', function_id = function['id'], _external = True)
        else:
            new_function[field] = function[field]
    return new_function

# Enabling DELETE, PUT, etc.
class RequestWithMethod(urllib2.Request):
    """Workaround for using DELETE with urllib2"""
    def __init__(self, url, method, data=None, headers={}, origin_req_host=None, unverifiable=False):
        self._method = method
        urllib2.Request.__init__(self, url, data, headers, origin_req_host, unverifiable)

    def get_method(self):
        if self._method:
            return self._method
        else:
            return urllib2.Request.get_method(self) 

#######################################################################################################
# Start the server on port 5000
#######################################################################################################


if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True, port = 5000)
