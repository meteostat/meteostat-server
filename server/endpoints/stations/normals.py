"""
Meteostat JSON API Server

The code is licensed under the MIT license.
"""

from datetime import datetime
import json
from flask import abort
from meteostat import Normals, units
from server import app, utils


"""
Meteostat configuration
"""
cache_time = 60 * 60 * 24 * 30
Normals.max_age = cache_time
Normals.autoclean = False

"""
Endpoint configuration
"""
# Query parameters
parameters = [
    ('station', str, None),
    ('start', int, None),
    ('end', int, None),
    ('units', str, None)
]


@app.route('/stations/normals')
def stations_normals():
    """
    Return station normals data in JSON format
    """

    # Get query parameters
    args = utils.get_parameters(parameters)

    # Check if required parameters are set
    if args['station']:

        try:

            # Get data
            if args['start'] and args['end']:

                # Get number of years between start and end year
                year_diff = args['end'] - args['start']

                # Check date range
                if year_diff < 0:
                    # Bad request
                    abort(400)

                data = Normals(args['station'], args['start'], args['end'])

            else:

                data = Normals(args['station'])

            # Check if any data
            if data.count() > 0:

                # Normalize data
                data = data.normalize()

                # Unit conversion
                if args['units'] == 'imperial':
                    data = data.convert(units.imperial)
                elif args['units'] == 'scientific':
                    data = data.convert(units.scientific)

                # Fetch DataFrame
                data = data.fetch()

                # To JSON
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
