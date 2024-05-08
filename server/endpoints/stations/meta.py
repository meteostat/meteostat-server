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
cache_time = 60 * 60 * 24

"""
Endpoint configuration
"""
# Query parameters
parameters = [
    ('id', str, None),
    ('wmo', str, None),
    ('icao', str, None)
]


@app.route('/stations/meta')
def stations_meta():
    """
    Return station meta data in JSON format
    """

    # Get query parameters
    args = utils.get_parameters(parameters)

    # Check if required parameters are set
    if args['id'] or args['wmo'] or args['icao']:

        try:

            # Get data from DB
            query = utils.db_query('''
        		SELECT
        			`stations`.`id` AS `id`,
        			`stations`.`name` AS `name`,
        			`stations`.`name_alt` AS `name_alt`,
        			`stations`.`country` AS `country`,
        			`stations`.`region` AS `region`,
        			`stations`.`national_id` AS `national_id`,
        			CAST(`stations`.`wmo` AS CHAR(5)) AS `wmo`,
        			`stations`.`icao` AS `icao`,
        			`stations`.`latitude` AS `latitude`,
        			`stations`.`longitude` AS `longitude`,
        			`stations`.`altitude` AS `altitude`,
        			`stations`.`tz` as `timezone`,
        			MIN(`inventory_model`.`start`) AS 'model_start',
        			MAX(`inventory_model`.`end`) AS 'model_end',
        			MIN(`inventory_hourly`.`start`) AS 'hourly_start',
        			MAX(`inventory_hourly`.`end`) AS 'hourly_end',
        			MIN(`inventory_daily`.`start`) AS 'daily_start',
        			MAX(`inventory_daily`.`end`) AS 'daily_end',
        			YEAR(MIN(`inventory_monthly`.`start`)) AS 'monthly_start',
        			YEAR(MAX(`inventory_monthly`.`end`)) AS 'monthly_end',
        			YEAR(MIN(`inventory_normals`.`start`)) AS 'normals_start',
        			YEAR(MAX(`inventory_normals`.`end`)) AS 'normals_end'
        		FROM `stations`
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
        		LEFT JOIN (
        			SELECT
        					`station`,
        					`start`,
        					`end`
        			FROM `inventory`
        			WHERE
        					`mode` = 'N'
        		)
        		AS
        			`inventory_normals`
        		ON
        			`stations`.`id` = `inventory_normals`.`station`
        		WHERE
                    `stations`.`id` = :id OR
                    `stations`.`wmo` = :wmo OR
                    `stations`.`icao` = :icao
        		GROUP BY
        			`stations`.`id`
        		LIMIT
        			1
            ''', {
                'id': args['id'],
                'wmo': args['wmo'],
                'icao': args['icao']
            })

            if query.rowcount > 0:

                # Fetch result
                data = query.fetchone()

                # Create dict of names
                try:
                    names = json.loads(data['name_alt'])
                except BaseException:
                    names = {}
                names['en'] = data['name']

                # Create JSON output
                output = json.dumps({
                    'id': data['id'],
                    'name': names,
                    'country': data['country'],
                    'region': data['region'],
                    'identifier': {
                        'national': data['national_id'],
                        'wmo': data['wmo'],
                        'icao': data['icao']
                    },
                    'location': {
                        'latitude': data['latitude'],
                        'longitude': data['longitude'],
                        'elevation': data['altitude']
                    },
                    'timezone': data['timezone'],
                    'inventory': {
                        'model': {
                            'start': data['model_start'].strftime('%Y-%m-%d') if data['model_start'] is not None else None,
                            'end': data['model_end'].strftime('%Y-%m-%d') if data['model_end'] is not None else None
                        },
                        'hourly': {
                            'start': data['hourly_start'].strftime('%Y-%m-%d') if data['hourly_start'] is not None else None,
                            'end': data['hourly_end'].strftime('%Y-%m-%d') if data['hourly_end'] is not None else None
                        },
                        'daily': {
                            'start': data['daily_start'].strftime('%Y-%m-%d') if data['daily_start'] is not None else None,
                            'end': data['daily_end'].strftime('%Y-%m-%d') if data['daily_end'] is not None else None
                        },
                        'monthly': {
                            'start': data['monthly_start'],
                            'end': data['monthly_end']
                        },
                        'normals': {
                            'start': data['normals_start'],
                            'end': data['normals_end']
                        }
                    }
                })

            else:

                output = 'null'

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
