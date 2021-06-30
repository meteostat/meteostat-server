"""
Meteostat JSON API Server

The code is licensed under the MIT license.
"""

from flask import request

def get_parameters(parameters: list):
    """
    Get request parameters
    """

    args = {}

    for parameter in parameters:
        value = request.args.get(parameter[0])
        args[parameter[0]] = parameter[1](value) if value else parameter[2]

    return args
