"""
Meteostat JSON API Server

API endpoint for retrieving hourly point data in JSON format.

The code is licensed under the MIT license.
"""

from server import app, utils
from flask import Response, abort
from datetime import datetime
import json
from meteostat import Point, Hourly

Point.radius = None

@app.route('/point/hourly')
def point_hourly():
    """
    Return hourly point data in JSON format
    """

    # Get query parameters
    lat = float(utils.arg('lat')) if utils.arg('lat') else None
    lon = float(utils.arg('lon')) if utils.arg('lon') else None
    alt = float(utils.arg('alt')) if utils.arg('alt') else None
    start = str(utils.arg('start')) if utils.arg('start') else None
    end = str(utils.arg('end')) if utils.arg('end') else None
    timezone = str(utils.arg('tz')) if utils.arg('timezone') else None
    model = bool(utils.arg('model')) if utils.arg('model') else True
    freq = str(utils.arg('freq')) if utils.arg('freq') else None
    units = str(utils.arg('units')) if utils.arg('units') else None

    # Check if required parameters are set
    if lat and lon and len(start) == 10 and len(end) == 10:

        # Convert start & end date strings to datetime
        start = datetime.strptime(start, '%Y-%m-%d')
        end = datetime.strptime(f'{end} 23:59:59', '%Y-%m-%d %H:%M:%S')

        # Get number of days between start and end date
        date_diff = (end - start).days

        # Check date range
        if date_diff < 0 or date_diff  > 30:
            abort(401)

        # Create a point
        location = Point(lat, lon, alt)

        # Get data
        data = Hourly(location, start, end)
        data = data.fetch()

        # DateTime Index to String
        data.index = data.index.strftime('%Y-%m-%d %H:%M:%S')

        # Inject meta data
        result = f'''{{
            "meta": {{
                "stations": {location.stations.to_list()}
            }},
            "data": {data.reset_index().to_json(orient="records")}
        }}'''

        # Return
        return Response(result, mimetype='application/json')
