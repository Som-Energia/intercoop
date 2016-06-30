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

"""
# TODO:

- Solve translations
- No service description
- No service name
- No such service
- Include peer.info optionally
- route activateservice/<peer>/<service>
"""



template = u"""\
<html>
<head>
<meta encoding='utf-8' />
<title>{}</title>
<link rel="stylesheet" type="text/css" href="intercoop.css">
</head>
<body>
<h1>Intercooperación</h1>
<ul>
{}</ul>
</body>
</html>
"""

peerTmpl = u"""\
<div class='peer'>
<div class='peerlogo'><img src='{peer.logo}' /></div>
<div class='peerheader'><a href='{peer.url.es}'>{peer.name}</a></div>
<div class='peerdescription'>{peer.description.es}</div>
<div class='services'>
{services}\
</div>
</div>
"""

serviceTmpl = u"""\
<div class='service'>
<div class='service_header'>{service.name.es}</div>
<div class='service_description'>{service.description.es}</div>
<a class='service_activation_bt' href='activateservice/{peer.peerid}/{serviceid}'>Activa</a>
</div>
"""

css = """\
.peer {
    clear: right;
    margin: 3ex 1ex;
    font-family: sans;
    width: 70ex;
    margin-left: auto;
    margin-right: auto;
}

.peer .peerlogo {
    float: right;
}

.peerdescription {
    padding: 3ex;
}

.peerheader {
    font-weight: bold;
}

.service {
    clear: right;
    border: 2pt solid #ddd;
    background: #eee;
}

.service_header {
    font-weight: bold;
    display: block;
    border-bottom: 1pt solid #ddd;
}


.service_activation_bt {
    display: block;
    position: relative;
    width: 20ex;
    text-decoration: none;
    padding: 1ex;
    background: #586;
    color: white;
    font-weight: bold;
    margin: 2ex 2ex 2ex 45ex;
    text-shadow: 1pt 1pt 1pt black;
    border: 1pt solid #aaa;
    border-radius: 1ex;
    text-align: center;
}

.service_activation_bt:active {
    border: 1pt solid #eee;
}
.service_activation_bt:hover {
    border: 1pt solid #333;
    background: #687;
}
"""




class Portal(Perfume):

    def __init__(self, name, peerdata):
        super(Portal, self).__init__(name)
        self.peers = peerdatastorage.PeerDataStorage(peerdata)
        self.name = name

    @route('/intercoop.css', methods=['GET'])
    def css(self):
        return css

    def serviceDescription(self, peer, service):
        return serviceTmpl.format(
            peer = peer,
            serviceid = service,
            service = peer.services[service],
            )

    def peerDescription(self, peer):
        return peerTmpl.format(
            peer=peer,
            services = "".join(
                self.serviceDescription(peer, service)
                for service in peer.services
                ),
            )

    @route('/', methods=['GET'])
    def index(self):
        response = template.format(
            self.name,
            "".join(
                self.peerDescription(peer)
                for peer in self.peers
                )
            )
        return response


# vim: ts=4 sw=4 et
