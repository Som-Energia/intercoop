# -*- encoding: utf-8 -*-

from flask import (
    make_response,
    request,
    Response
    )

from . import crypto
from . import apiclient
from . import peerdatastorage
from . import userinfo
from .perfume import Perfume, route
from yamlns import namespace as ns

"""
# TODO:

Roadmap:

- [ ] route activateservice/<peer>/<service>
    - [x] fields = portal.requiredFields(peer, service)
        - [x] when service fields, use them
        - [x] when no service fields, use global peer fields
        - [x] when no fields anywhere, raise
    - [+] data = portal.userInfo(userid, fields)
        - [+] all fields
        - [+] filtering
        - [+] no such user
        - [+] no such field
    - [ ] translations = portal.fieldTranslation(fields)
        - [+] One level, translation and field exist
        - [ ] Peer doesn't exist
        - [ ] One level, field exists but translation no
        - [ ] One level, field doesn't exist
        - [ ] Many level, translation and field exist
        - [ ] Many level, field exists but translation no
        - [ ] Many level, field doesn't exist
    - [ ] fieldhtml = portal.renderField(fieldLabel, value)
    - [ ] innerhtml = portal.renderUserData(data)
- [ ] route confirmactivateservice/<peer>/<service>

Postponed:

- [ ] activateservice: special display for list fields
- [ ] activateservice: special display for None fields
- [ ] bad peer in required fields
- [ ] bad service in required fields
- [ ] Solve translations
- [ ] Should different types in field be rendered differently
- [ ] No service description
- [ ] No service name
- [ ] No such service
- [ ] Include peer.info optionally
- [ ] require login
"""



template = u"""\
<html>
<head>
<meta encoding='utf-8' />
<title>{}</title>
<link rel="stylesheet" type="text/css" href="/intercoop.css">
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

templateActivateService = u"""\
<html>
<head>
<meta encoding='utf-8' />
<title>Activación del servicio '{service.name.es}' en '{peer.name}'</title>
<link rel="stylesheet" type="text/css" href="/intercoop.css">
</head>
<body>
<h1>Autorización de transferencia de datos personales a <em>{peer.name}</em></h1>
<div class='privacywarning'>
Para activar el servicio <em>{service.name.es}</em>
en <em>{peer.name}</em>,
transferiremos a dicha entidad los siguientes datos:
<div class='transferfields'>
{fields}\
</div>
Dicha entidad tratará dichos datos según su propia
<a href='{peer.privacyPolicyUrl.es}' target='_blank'>política de privacidad</a>.
</div>
<a class='privacy_accept_bt' href='/confirmactivateservice/{peerid}/{serviceid}'>
Acepto
</a>
</body>
</html>
"""

fieldTmpl = u"""\
<div class='field'>
<div class='fieldheader'>{field}:</div>
<div class='fieldvalue'>{value}</div>
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


.service_activation_bt, .privacy_accept_bt {
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

.service_activation_bt:active, .privacy_accept_bt:active {
    border: 1pt solid #eee;
}
.service_activation_bt:hover, .privacy_accept_bt:hover {
    border: 1pt solid #333;
    background: #687;
}

.transferfields {
    margin: 1ex;
    box-shadow: 2px 4px 5px #444;
    padding: 1ex;
}
.transferfields .field {
    display: table-row;
}
.transferfields .fieldvalue,
.transferfields .fieldheader {
    display: table-cell;
}
.transferfields .fieldheader {
    font-weight: bold;
    border-bottom: solid 1pt #eee;
}

"""


class Portal(Perfume):

    def __init__(self, name, peerid, peerdatadir, userdatadir, keyfile):
        super(Portal, self).__init__(name)
        self.name = name
        self.peerid = peerid
        self.key = crypto.loadKey(keyfile)
        self.peers = peerdatastorage.PeerDataStorage(peerdatadir)
        self.users = userinfo.UserInfo(userdatadir)

    @route('/intercoop.css', methods=['GET'])
    def css(self):
        r = make_response(css)
        r.mimetype='text/css'
        return r

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

    def renderField(self, value, field):
        return fieldTmpl.format(
            value=value,
            field=field,
            )

    def requiredFields(self, peer, service):
        peerData = self.peers.get(peer)
        serviceData = peerData.services[service]

        if 'fields' in serviceData:
            return list(serviceData.fields)

        if 'fields' in peerData:
            return list(peerData.fields)

        raise Exception("Peer '{}' does not specify fields for service '{}'"
            .format(peer, service))

    def fieldTranslation(self, peername, field, isocode):
        peerData = self.peers.get(peername)
        try:
            serviceData = peerData[field]
        except KeyError:
            raise Exception("Invalid field '{}'".format(field))
        return serviceData[isocode].rstrip()

    @route('/activateservice/<peer>/<service>', methods=['GET'])
    def activateService(self, peer, service):
        # TODO: done twice, also in requiredFields
        peerData = self.peers.get(peer)
        serviceData = peerData.services[service]
        fields = self.requiredFields(peer, service)
        data = self.users.getFields('myuser', fields) # TODO: Real user
        response = templateActivateService.format(
            peerid=peer,
            peer=peerData,
            serviceid=service,
            service=serviceData,
            fields="".join(
                self.renderField(
                    field = field, # TODO: Translate the field
                    value = value,
                    )
                for field, value in data.items()
                )
            )
        return response

    @route('/confirmactivateservice/<peer>/<service>', methods=['GET'])
    def confirmActivateService(self, peer, service):
        # TODO: Not under test!!
        peerData = self.peers.get(peer)
        serviceData = peerData.services[service]
        fields = self.requiredFields(peer, service)
        data = self.users.getFields('myuser', fields) # TODO: Real user
        api = apiclient.ApiClient(peerData.targetUrl, self.key)
        # TODO: augment personal data keys with source ones
        # TODO: handle errors
        try:
            continuationUri = api.activateService(service, data)
        except:
            # TODO: Log the error
            return "Error comunicando con la entidad"
        return redirect(continuationUri, 302)

# vim: ts=4 sw=4 et
