"""
Meteostat JSON API Server

The code is licensed under the MIT license.
"""

from datetime import datetime
import json
from flask import abort
from server import app, utils


"""
Meteostat configuration
"""
cache_time = 60 * 60 * 24 * 14

"""
Endpoint configuration
"""
# Query parameters
parameters = [
    ('lat', float, None),
    ('lon', float, None),
    ('limit', int, 10),
    ('radius', int, 100000),
]


@app.route('/stations/nearby')
def stations_nearby():
    """
    Return station meta data in JSON format
    """

    # Get query parameters
    args = utils.get_parameters(parameters)

    # Check if required parameters are set
    if 'lat' in args and 'lon' in args:

        try:

            # Get data from DB
            query = utils.db_query('''
                SELECT
                  `stations`.`id` AS `id`,
                  `stations`.`name` AS `name`,
                  `stations`.`name_alt` AS `name_alt`,
                  ROUND(
                    ( 6371000 * acos( cos( radians(:lat) ) *
                    cos( radians( `latitude` ) ) *
                    cos( radians( `longitude` ) - radians(:lon) ) +
                    sin( radians(:lat) ) *
                    sin( radians( `latitude` ) ) ) )
                  , 1) AS `distance`
                FROM
                  `stations`
                LEFT JOIN (
                  SELECT
                      `station`,
                      `start`,
                      `end`
                  FROM `inventory`
                  WHERE
                      `mode` = 'P'
                )
                AS
                  `inventory_model`
                ON
                  `stations`.`id` = `inventory_model`.`station`
                LEFT JOIN (
                  SELECT
                      `station`,
                      `start`,
                      `end`
                  FROM `inventory`
                  WHERE
                      `mode` = 'H'
                )
                AS
                  `inventory_hourly`
                ON
                  `stations`.`id` = `inventory_hourly`.`station`
                LEFT JOIN (
                  SELECT
                      `station`,
                      `start`,
                      `end`
                  FROM `inventory`
                  WHERE
                      `mode` = 'D'
                )
                AS
                  `inventory_daily`
                ON
                  `stations`.`id` = `inventory_daily`.`station`
                LEFT JOIN (
                  SELECT
                      `station`,
                      `start`,
                      `end`
                  FROM `inventory`
                  WHERE
                      `mode` = 'M'
                )
                AS
                  `inventory_monthly`
                ON
                  `stations`.`id` = `inventory_monthly`.`station`
                WHERE
                  `stations`.`latitude` IS NOT NULL AND
                  ABS(`stations`.`latitude`) <= 90 AND
                  `stations`.`longitude` IS NOT NULL AND
                  ABS(`stations`.`longitude`) <= 180 AND
                  (
                    `inventory_hourly`.`start` IS NOT NULL OR
                    `inventory_daily`.`start` IS NOT NULL OR
                    `inventory_monthly`.`start` IS NOT NULL
                  )
                GROUP BY
                    `stations`.`id`
                HAVING
                  `distance` <= :radius
                ORDER BY
                  `distance`
                LIMIT
                  :limit
            ''', {
                'lat': args['lat'],
                'lon': args['lon'],
                'radius': args['radius'],
                'limit': args['limit']
            })

            if query.rowcount > 0:

                # Fetch results
                results = query.fetchall()

                # Output list
                output = []

                # Go through stations
                for data in results:
                    
                    data = data._mapping

                    # Create dict of names
                    try:
                        names = json.loads(data['name_alt'])
                    except BaseException:
                        names = {}
                    names['en'] = data['name']

                    # Create JSON output
                    output.append({
                        'id': data['id'],
                        'name': names,
                        'distance': data['distance']
                    })

                # Stringify output
                output = json.dumps(output)

            else:

                output = '[]'

            # Inject meta data
            meta = {}
            meta['generated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Generate output string
            output = f'''{{"meta":{json.dumps(meta)},"data":{output}}}'''

            # Return
            return utils.send_response(output, cache_time)


        except BaseException:

            # Bad request
            abort(400)

    else:

        # Bad request
        abort(400)
