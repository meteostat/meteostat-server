"""
Meteostat JSON API Server

The code is licensed under the MIT license.
"""

from datetime import datetime
import json
from flask import Response, abort
from meteostat import Point, Daily
from server import app, utils


"""
Meteostat configuration
"""
Point.radius = 120000
Daily.max_age = 60 * 60 * 48
Daily.threads = 4

"""
Endpoint configuration
"""
# Query parameters
parameters = [
    ('lat', float, None),
    ('lon', float, None),
    ('alt', int, None),
    ('start', str, None),
    ('end', str, None),
    ('model', bool, True),
    ('freq', str, None),
    ('units', str, None)
]

# Maximum number of days per request
max_days = 365 * 10


@app.route('/point/daily')
def point_daily():
    """
    Return daily point data in JSON format
    """

    # Get query parameters
    args = utils.get_parameters(parameters)

    # Check if required parameters are set
    if args['lat'] and args['lon'] and len(
            args['start']) == 10 and len(args['end']) == 10:

        # Convert start & end date strings to datetime
        start = datetime.strptime(args['start'], '%Y-%m-%d')
        end = datetime.strptime(f'{args["end"]} 23:59:59', '%Y-%m-%d %H:%M:%S')

        # Get number of days between start and end date
        date_diff = (end - start).days

        # Check date range
        if date_diff < 0 or date_diff > max_days:
            # Bad request
            abort(400)

        # Create a point
        location = Point(args['lat'], args['lon'], args['alt'])

        # Get data
        data = Daily(location, start, end, model=args['model'])

        # Check if any data
        if data.count() > 0:

            # Fetch DataFrame
            data = data.fetch()

            # DateTime Index to String
            data.index = data.index.strftime('%Y-%m-%d')
            data.index.rename('date', inplace=True)
            data = data.reset_index().to_json(orient="records")

        else:

            # No data
            data = '[]'

        # Inject meta data
        meta = {}
        meta['generated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        meta['stations'] = location.stations.to_list()

        # Generate output string
        output = f'''{{"meta":{json.dumps(meta)},"data":{data}}}'''

        # Return
        return Response(output, mimetype='application/json')

    else:

        # Bad request
        abort(400)
