"""
Meteostat JSON API Server

The code is licensed under the MIT license.
"""

from datetime import datetime
import json
from flask import abort
from meteostat import Monthly, units
from server import app, utils


"""
Meteostat configuration
"""
Monthly.autoclean = False

"""
Endpoint configuration
"""
# Query parameters
parameters = [
    ('station', str, None),
    ('start', str, None),
    ('end', str, None),
    ('model', bool, True),
    ('freq', str, None),
    ('units', str, None)
]

# Maximum number of days per request
max_days = 365 * 10


@app.route('/stations/monthly')
def stations_monthly():
    """
    Return monthly station data in JSON format
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
            if date_diff < 0:
                # Bad request
                abort(400)

            # Caching
            Monthly.max_age = 60 * 60 * 24 * 7

            # Get data
            data = Monthly(args['station'], start, end, model=args['model'])

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
