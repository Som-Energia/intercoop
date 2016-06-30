# -*- encoding: utf-8 -*-


from flask import (
	make_response,
	request,
    Response
	)

from . import apiclient
from . import peerdatastorage
from .perfume import Perfume, route
from yamlns import namespace as ns
class Portal(Perfume):
    @route('/', methods=['GET'])
    def index(self):
        response = """<html>
            <head></head>
            <body>Lista de peers
            <ul>
                """
        response+="</br>".join(
            "<li>%s</li>" % 
                (p.name + "<ul>{}</ul>".format(
                    "</br>".join("<li>%s</li>" % s 
                            for s in p.services
                    )
                )
             ) if "services" in p else ""
            for p in self.peerdatastorage
        )
        response+="""
            </ul>
            </body>
            </html>
            """
        return response
    def __init__(self, name, datadir):
        super(Portal, self).__init__(name)
        self.peerdatastorage = peerdatastorage.PeerDataStorage(datadir)

