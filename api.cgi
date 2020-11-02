#!/usr/bin/python
from wsgiref.handlers import CGIHandler
from api import app

CGIHandler().run(app)
