#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""get_rooms.py: Send X and Y coordinates and get the room label (for TWIST testbed, 2nd floor)."""

__author__ = "Filip Lemic"
__copyright__ = "Copyright 2015, EVARILOS Project"

__version__ = "1.0.0"
__maintainer__ = "Filip Lemic"
__email__ = "lemic@tkn.tu-berlin.de"
__status__ = "Development"


from flask import Flask
from flask import make_response
from flask import request, current_app
import json
from functools import update_wrapper
from datetime import timedelta

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
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
    return json.dumps("TWIST Testbed, 2nd floor: Send the coordinate - get the room label!")

@app.route('/getRoomLabel/<coord_x>/<coord_y>', methods = ['GET'])
@crossdomain(origin='*')
def get_room(coord_x, coord_y):
    try:
        coord_x = float(coord_x)
        coord_y = float(coord_y)
    except:
        return 'Wrong data format!'

    if coord_x >= 0     and coord_x < 3.25   and coord_y >= 0    and coord_y < 6.72:
        return  'FT222'
    if coord_x >= 3.25  and coord_x < 9.42   and coord_y >= 0    and coord_y < 6.72:
        return 'FT223'
    if coord_x >= 9.42  and coord_x < 15.67  and coord_y >= 0    and coord_y < 6.72:
        return 'FT224'
    if coord_x >= 15.67 and coord_x < 21.16  and coord_y >= 0    and coord_y < 6.72:
        return 'FT225'
    if coord_x >= 21.16 and coord_x <= 30.87 and coord_y >= 0    and coord_y < 6.72:
        return 'FT226'
    if coord_x >= 0     and coord_x < 25.19  and coord_y >= 6.72 and coord_y < 8.89:
        return 'hollway_2nd'
    if coord_x >= 25.19 and coord_x <= 30.87 and coord_y >= 6.72 and coord_y <= 15.56:
        return 'stairs_2nd'
    if coord_x > 0      and coord_x < 3.21   and coord_y >= 8.89 and coord_y <= 15.56:
        return 'FT236'
    if coord_x >= 3.31  and coord_x < 6.42   and coord_y >= 8.89 and coord_y <= 15.56:
        return 'FT235'
    if coord_x >= 6.42  and coord_x < 12.65  and coord_y >= 8.89 and coord_y <= 15.56:
        return 'FT234' 
    if coord_x >= 12.65 and coord_x < 15.93  and coord_y >= 8.89 and coord_y <= 15.56:
        return 'FT233'
    if coord_x >= 15.93 and coord_x < 19.12  and coord_y >= 8.89 and coord_y <= 15.56:
        return 'FT232'
    if coord_x >= 19.12 and coord_x < 22.12  and coord_y >= 8.89 and coord_y <= 15.56:
        return 'FT231'
    if coord_x >= 22.12 and coord_x < 25.19  and coord_y >= 8.89 and coord_y <= 15.56:
        return 'FT230'
    return 'no_room'

if __name__ == '__main__':
	app.run(host = '0.0.0.0', debug = True, port = 5001)

