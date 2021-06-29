"""
Meteostat JSON API Server

API endpoint for retrieving hourly weather station data in JSON format.

The code is licensed under the MIT license.
"""

from server import app
from flask import request
from datetime import datetime
import json
from meteostat import Hourly

@app.route('/stations/hourly')
def stations_hourly():
    station = str(request.args.get('station'))
    start = datetime.strptime(request.args.get('start'), '%Y-%m-%d')
    end = datetime.strptime(f'{request.args.get("end")} 23:59:59', '%Y-%m-%d %H:%M:%S')

    data = Hourly(station, start, end).normalize()
    df = data.fetch()

    result = df.to_json(orient="records")

    return result