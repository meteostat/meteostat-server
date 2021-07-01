"""
Meteostat JSON API Server

The code is licensed under the MIT license.
"""

from datetime import datetime
import json
from flask import abort
from meteostat import Point, Hourly, units
from server import app, utils


"""
Meteostat configuration
"""
cache_time = 60 * 60 * 3
Point.radius = 120000
Hourly.max_age = cache_time
Hourly.threads = 4
Hourly.autoclean = False

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
    ('tz', str, None),
    ('model', bool, True),
    ('freq', str, None),
    ('units', str, None)
]

# Maximum number of days per request
max_days = 30


@app.route('/point/hourly')
def point_hourly():
    """
    Return hourly point data in JSON format
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
        data = Hourly(location, start, end, timezone=args['tz'], model=args['model'])

        # Check if any data
        if data.count() > 0:

            # Normalize data
            data = data.normalize()

            # Aggregate
            if args['freq']:
                data = data.aggregate(args['freq'])

            # Unit conversion
            if args['units'] == 'imperial':
                data = data.convert(units.imperial)
            elif args['units'] == 'scientific':
                data = data.convert(units.scientific)

            # Fetch DataFrame
            data = data.fetch()

            # Convert to integer
            data['tsun'] = data['tsun'].astype('Int64')
            data['coco'] = data['coco'].astype('Int64')

            # DateTime Index to String
            data.index = data.index.strftime('%Y-%m-%d %H:%M:%S')
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
        return utils.send_response(output, cache_time)

    else:

        # Bad request
        abort(400)
