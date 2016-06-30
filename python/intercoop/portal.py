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

template = """\
<html>
<head>
<meta encoding='utf-8' />
<title>{}</title>
</head>
<body>
<h1>Intercooperación</h1>
<ul>
{}</ul>
</body>
</html>
"""




class Portal(Perfume):

    def __init__(self, name, peerdata):
        super(Portal, self).__init__(name)
        self.peerdatastorage = peerdatastorage.PeerDataStorage(peerdata)
        self.name = name


    @route('/', methods=['GET'])
    def index(self):
        response = template.format(
            self.name,
            "".join(
                "<li>%s</li>\n" % (
                    p.name + "\n<ul>\n{}</ul>\n".format(
                        "</br>".join(
                            "<li>%s</li>\n" % s 
                            for s in p.services
                            )
                        )
                     ) if "services" in p else ""
                for p in self.peerdatastorage
                )
            )
        return response


# vim: ts=4 sw=4 et
