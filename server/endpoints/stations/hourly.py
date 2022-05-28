"""
Meteostat JSON API Server

The code is licensed under the MIT license.
"""

from datetime import datetime
import json
from flask import abort
from meteostat import Hourly, units
from server import app, utils


"""
Meteostat configuration
"""
Hourly.autoclean = False

"""
Endpoint configuration
"""
# Query parameters
parameters = [
    ('station', str, None),
    ('start', str, None),
    ('end', str, None),
    ('tz', str, None),
    ('model', bool, True),
    ('freq', str, None),
    ('units', str, None)
]

# Maximum number of days per request
max_days = 30


@app.route('/stations/hourly')
def stations_hourly():
    """
    Return hourly station data in JSON format
    """

    # Get query parameters
    args = utils.get_parameters(parameters)

    # Check if required parameters are set
    if args['station'] and len(args['start']) == 10 and len(args['end']) == 10:

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

            if now_diff < 3:
                cache_time = 60 * 60
            elif now_diff < 30:
                cache_time = 60 * 60 * 24
            else:
                cache_time = 60 * 60 * 24 * 3

            Hourly.max_age = cache_time

            # Get data
            data = Hourly(args['station'], start, end, timezone=args['tz'], model=args['model'])

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
