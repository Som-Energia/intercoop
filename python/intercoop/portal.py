# -*- encoding: utf-8 -*-


from flask import (
	make_response,
	request,
    Response
	)

from . import apiclient
from .perfume import Perfume, route
from yamlns import namespace as ns
class Portal(Perfume):
    @route('/', methods=['GET'])
    def index(self):
        return """<html>
            <head></head>
            <body>Lista de peers</body>
            </html>
            """
    def __init__(self, name):
        super(Portal, self).__init__(name)

