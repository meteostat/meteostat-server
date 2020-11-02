"""
Official Meteostat JSON API

API endpoint for retrieving hourly station data
in JSON format

The code is licensed under the MIT license.
"""

from api import app, version
from flask import request
import pandas as pd
import json
from datetime import datetime

@app.route('/v' + version + '/stations/hourly')
def stations_hourly():
    start = datetime.strptime(request.args.get('start'), '%Y-%m-%d')
    end = datetime.strptime(request.args.get('end'), '%Y-%m-%d')

    columns = [
        'date',
        'tavg',
        'tmin',
        'tmax',
        'prcp',
        'snow',
        'wdir',
        'wspd',
        'wpgt',
        'pres',
        'tsun'
    ]

    parse_dates = { 'time': [0] }

    df = pd.read_csv('https://bulk.meteostat.net/daily/10637.csv.gz', compression = 'gzip', names = columns, parse_dates = parse_dates)
    df = df[(df['time'] >= start) & (df['time'] <= end)]

    df['time'] = df['time'].dt.strftime('%Y-%m-%d')

    result = df.to_json(orient="records")
    parsed = json.loads(result)

    return json.dumps(parsed, indent=4)
