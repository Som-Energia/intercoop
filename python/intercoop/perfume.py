# -*- coding: utf-8 -*-

"""
This is a modified copy of https://github.com/hoh/perfume/

Several changes were made:
- uses prefixed attributes because app is a Flask and has a 'route' method
- added the method parameter to the decorator

TODO: Make a pull request against https://github.com/hoh/perfume/
"""

from flask import (
	Flask,
	)

def route(regex, **kwds):
    'Decorates your function with a route as "function.perfume_route = ..."'
    def decorator(func):
        func.perfume_route = regex
        func.perfume_args = kwds
        return func
    return decorator


class Perfume(object):

    def __init__(self, name, debug=False):
        ''
        self.app = Flask(name)
        self.app.debug = debug
        self._load()

    def _load(self):
        "Updates the app's routes with all methods."
        for name in dir(self):
            method = self.__getattribute__(name)
            try:
                route = method.perfume_route
                args = method.perfume_args
            except AttributeError:
                continue

            self.app.route(route, **args)(method)

    def run(self, *args, **kwds):
        self.app.run(*args, **kwds)



# vim: ts=4 sw=4 et
