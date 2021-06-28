from flask import request

def arg(name: str):
    """
    Get request parameter by name
    """

    return request.args.get(name)
