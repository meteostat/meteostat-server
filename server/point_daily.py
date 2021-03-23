"""
Meteostat JSON API Server

API endpoint for retrieving daily point data in JSON format.

The code is licensed under the MIT license.
"""

from server import app
from flask import request
from datetime import datetime
import json
from meteostat import Point, Daily

@app.route('/point/daily')
def point_daily():
    lat = float(request.args.get('lat'))
    lon = float(request.args.get('lon'))
    alt = float(request.args.get('alt'))
    start = datetime.strptime(request.args.get('start'), '%Y-%m-%d')
    end = datetime.strptime(request.args.get('end'), '%Y-%m-%d')

    point = Point(lat, lon, alt)

    data = Daily(point, start, end)
    df = data.fetch()

    result = df.to_json(orient="records")

    return result
