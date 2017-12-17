# -*- encoding: utf-8 -*-

from flask import (
    make_response,
    request,
    Response,
    redirect,
    )

from . import crypto
from . import apiclient
from . import translation
from . import packaging
from . import catalog
from .perfume import Perfume, route
from yamlns import namespace as ns


template = u"""\
<html>
<head>
<meta encoding='utf-8' />
<title>Portal {company}: Intercooperación</title>
<link rel="stylesheet" type="text/css" href="/intercoop.css">
</head>
<body>
<div class='head'>{company}: Área de usuario
<div class='loginTag'>Validado como {login}</div>
</div>
<h1>Intercooperación</h1>
<ul>
{content}</ul>
</body>
</html>
"""

peerTmpl = u"""\
<div class='peer'>
<div class='peerlogo'><img src='{peer.logo}' /></div>
<div class='peerheader'><a href='{peer.url}'>{peer.name}</a></div>
<div class='peerdescription'>{peer.description}</div>
<div class='services'>
{services}\
</div>
</div>
"""

serviceTmpl = u"""\
<div class='service'>
<div class='service_header'>{service.name}</div>
<div class='service_description'>{service.description}</div>
<a class='service_activation_bt' href='activateservice/{peer.peerid}/{serviceid}'>Activa</a>
</div>
"""

templateActivateService = u"""\
<html>
<head>
<meta encoding='utf-8' />
<title>{company}: Activación del servicio '{service.name}' en '{peer.name}'</title>
<link rel="stylesheet" type="text/css" href="/intercoop.css">
</head>
<body>
<div class='head'>{company}: Área de usuario
<div class='loginTag'>Validado como {login}</div>
</div>
<h1>Autorización de transferencia de datos personales a <em>{peer.name}</em></h1>
<div class='privacywarning'>
Para activar el servicio <em>{service.name}</em>
en <em>{peer.name}</em>,
transferiremos a dicha entidad los siguientes datos:
<div class='transferfields'>
{fields}\
</div>
Dicha entidad tratará dichos datos según su propia
<a href='{peer.privacyPolicyUrl}' target='_blank'>política de privacidad</a>.
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

body {
    max-width: 80ex;
    margin-left: auto;
    margin-right: auto;
    margin-top: 3x;
    padding: 4ex;
}

h1 {
    color: #352;
}

.loginTag {
    padding: 1ex 2px;
    position: absolute;
    right: 2ex;
    top: 0;
    left: 2ex;
    text-align: right;
}

.head {
    padding: 1ex 15px;
    background-color: #152;
    color: white;
    position: fixed;
    right: 0;
    top: 0;
    left: 0;
    text-align: left;
}

.peer {
    clear: right;
    margin: 3ex 1ex;
    font-family: sans;
    max-width: 70ex;
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


.service_activation_bt,
.privacy_accept_bt {
    display: block;
    width: 20ex;
    text-decoration: none;
    padding: 1ex;
    background: #586;
    color: white;
    font-weight: bold;
    margin: 2ex 2ex 2ex auto;
    text-shadow: 2px 2px 2px black;
    border: 1pt solid #aaa;
    border-radius: 4px;
    text-align: center;
}

.service_activation_bt:active,
.privacy_accept_bt:active {
    border: 1pt solid #eee;
}
.service_activation_bt:hover,
.privacy_accept_bt:hover {
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
    padding: 1ex;
}

.transferfields .fieldvalue ul {
    padding-left: 0ex;
    list-style-type: none;
}

"""

class Portal(Perfume):

    def __init__(self, name, peerid, keyfile, users=None, peers=None, peerdatadir=None, userdatadir=None):
        super(Portal, self).__init__(name)
        self.name = name
        self.peerid = peerid
        self.key = crypto.loadKey(keyfile)
        self.users = users
        self.catalog = catalog.IntercoopCatalog(
            keyfile = keyfile,
            peers = peers,
            users = users,
            )

    @route('/intercoop.css', methods=['GET'])
    def css(self):
        r = make_response(css)
        r.mimetype='text/css'
        return r

    def serviceDescription(self, peer, service):
        _ = self._translator()
        data = _(peer.services[service])
        return serviceTmpl.format(
            peer = peer,
            serviceid = service,
            service = data,
            )

    def peerDescription(self, peer):
        _ = self._translator()
        peer = _(peer)
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
            login=self._user(),
            company=self.peerid,
            content="".join(
                self.peerDescription(peer)
                for peer in self.catalog
                )
            )
        return response

    def renderField(self, field, value):
        if type(value) == list:
            value = "\n<ul>\n"+''.join(
                u"<li>{}</li>\n".format(item)
                for item in value
                ) + "</ul>\n"
        if value is None:
            value = '---'

        return fieldTmpl.format(
            value=value,
            field=field,
            )

    def _user(self):
        # Simulates a logged in user
        return 'myuser' # TODO: take it from login info

    def _translator(self):
        lang = self.users.language(self._user())
        return translation.Translator(lang)
        
    @route('/activateservice/<peer>/<service>', methods=['GET'])
    def activateService(self, peer, service):
        fields = self.catalog.requiredFields(peer, service)
        queriedFields = list(fields)
        if 'lang' not in fields:
            queriedFields.append('lang')
        values = self.catalog.fieldValues(self._user(),queriedFields)
        lang = values['lang']
        labels = self.catalog.fieldLabels(fields, lang)
        peerData = self.catalog.peerInfo(peer,lang)
        serviceData = peerData.services[service]
        response = templateActivateService.format(
            login=self._user(),
            company=self.peerid,
            peerid=peer,
            peer=peerData,
            serviceid=service,
            service=serviceData,
            fields="".join(
                self.renderField(
                    field = labels[field],
                    value = values[field],
                    )
                for field in fields
                )
            )
        return response

    @route('/confirmactivateservice/<peer>/<service>', methods=['GET'])
    def confirmActivateService(self, peer, service):
        # TODO: Not under test!!
        # TODO: augment personal data keys with source ones
        # TODO: handle errors
        try:
            continuationUrl = self.catalog.activate(peer, service, self._user())
        except Exception as e:
            print(type(e).__name__, e) 
            # TODO: Log the error
            return "Error comunicando con la entidad"
        return redirect(continuationUrl, 302)


    # ID related functions, not for intercoop

    def qrcode(self, format='svg'):
        fields = [
            'originpeer',
            'name',
            'nif',
            'innerid',
            ]
        data = self.catalog.fieldValues(self._user(), fields)
        signed = packaging.Generator(self.key).produce(data)
        print (signed)
        import qrcode
        import qrcode.image.svg

        qr = qrcode.QRCode(image_factory=qrcode.image.svg.SvgImage)
        qr.add_data(signed)
        im = qr.make_image()
        import io
        output = io.BytesIO()
        im.save(output)
        return output.getvalue()

    @route('/personalid', methods=['GET'])
    def personalid(self):
        svg = self.qrcode()
        r = make_response(svg)
        r.mimetype='image/svg+xml'
        return r

    @route('/personalid/validate', methods=['GET'])
    def validatePersonalId(self):
        return """\
<form action='' method='post' enctype="multipart/form-data">
<input type='file' name="qrcapture" size="80"> 
<input type='submit' value='Upload'>
</form>
"""
        
        
    @route('/personalid/validate', methods=['POST'])
    def validatePersonalId_post(self):

        from werkzeug import secure_filename
        import os
        capture = request.files['qrcapture']
        if capture.filename == '': return
        filename = os.path.join('.', secure_filename(capture.filename))
        capture.save(filename)

        import qrtools
        qr = qrtools.QR()
        qr.decode(filename)

        p = packaging.Parser({self.peerid: self.key})
        try:
            result = p.parse(qr.data).dump()
        except Exception as e:
            print(e)
            return "El carnet es invalido"
        r = make_response(p.parse(qr.data).dump())
        r.mimetype='text/plain'
        return r



# vim: ts=4 sw=4 et
