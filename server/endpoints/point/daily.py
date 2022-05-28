"""
Meteostat JSON API Server

The code is licensed under the MIT license.
"""

from datetime import datetime
import json
from flask import abort
from meteostat import Point, Daily, units
from server import app, utils


"""
Meteostat configuration
"""
Point.radius = 120000
Daily.threads = 4
Daily.autoclean = False

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

        try:

            # Convert start & end date strings to datetime
            start = datetime.strptime(args['start'], '%Y-%m-%d')
            end = datetime.strptime(f'{args["end"]} 23:59:59', '%Y-%m-%d %H:%M:%S')

            # Get number of days between start and end date
            date_diff = (end - start).days

            # Check date range
            if date_diff < 0 or date_diff > max_days:
                # Bad request
                abort(400)

            # Caching
            now_diff = (datetime.now() - end).days

            if now_diff < 30:
                cache_time = 60 * 60 * 24
            else:
                cache_time = 60 * 60 * 24 * 3

            Daily.max_age = cache_time

            # Create a point
            location = Point(args['lat'], args['lon'], args['alt'])

            # Get data
            data = Daily(location, start, end, model=args['model'])

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
            return utils.send_response(output, cache_time)

        except BaseException:

            # Bad request
            abort(400)

    else:

        # Bad request
        abort(400)
