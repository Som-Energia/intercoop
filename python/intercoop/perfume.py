# -*- encoding: utf-8 -*-

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

def route(regex, methods=None):
    'Decorates your function with a route as "function.route = ..."'
    def decorator(func):
        func.perfume_route = regex
        func.perfume_methods = methods
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
            try : method.perfume_route
            except AttributeError: continue
            self.app.route(
                method.perfume_route,
                methods=method.perfume_methods,
                )(method)

    def run(self):
        self.app.run()



# vim: ts=4 sw=4 et
