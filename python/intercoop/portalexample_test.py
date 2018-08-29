# -*- encoding: utf-8 -*-

import unittest
import os
import shutil
from . import userinfo
from . import portalexample
from . import peerinfo
from yamlns import namespace as ns
from .fixtures import (
    myuseryaml,
    somacmeyaml,
    sombogusyaml,
)

header= u"""\
<html>
<head>
<meta encoding='utf-8' />
<title>Portal somillusio: Intercooperación</title>
<link rel="stylesheet" type="text/css" href="/intercoop.css">
</head>
<body>
<div class='head'>somillusio: \xc1rea de usuario
<div class='loginTag'>Validado como myuser</div>
</div>
<h1>Intercooperación</h1>
<ul>
"""

footer = u"""\
</ul>
</body>
</html>
"""

acmePeerHeader = u"""\
<div class='peer'>
<div class='peerlogo'><img src='http://www.linpictures.com/images/indevimgs/acme.jpg' /></div>
<div class='peerheader'><a href='http://somacme.coop/es'>Som Acme, SCCL</a></div>
<div class='peerdescription'>La cooperativa para atrapar correcaminos
</div>
<div class='services'>
"""

acmeService = u"""\
<div class='service'>
<div class='service_header'>Comprar explosivos</div>
<div class='service_description'>Puedes comprar explosivos éticos de la mejor calidad.
</div>
<a class='service_activation_bt' href='activateservice/somacme/explosives'>Activa</a>
</div>
"""

acmeService2 = u"""\
<div class='service'>
<div class='service_header'>Comprar yunques</div>
<div class='service_description'>Yunques garantizados, siempre caen en una cabeza
</div>
<a class='service_activation_bt' href='activateservice/somacme/anvil'>Activa</a>
</div>
"""

bogusPeerHeader = u"""\
<div class='peer'>
<div class='peerlogo'><img src='http://xes.cat/wp-content/uploads/2017/05/logotip-xes.png' /></div>
<div class='peerheader'><a href='https://es.sombogus.coop'>Som Bogus, SCCL</a></div>
<div class='peerdescription'>Productos inútiles pero muy éticos
</div>
<div class='services'>
"""

bogusService = u"""\
<div class='service'>
<div class='service_header'>Contrata</div>
<div class='service_description'>Productos con marcas tipo Panone, Grifons, Pas Natural, Reacciona...
</div>
<a class='service_activation_bt' href='activateservice/sombogus/contract'>Activa</a>
</div>
"""

peerFooter = u"""\
</div>
</div>
"""

acmeExplosivesHeader = u"""\
<html>
<head>
<meta encoding='utf-8' />
<title>somillusio: Activación del servicio 'Comprar explosivos' en 'Som Acme, SCCL'</title>
<link rel="stylesheet" type="text/css" href="/intercoop.css">
</head>
<body>
<div class='head'>somillusio: \xc1rea de usuario
<div class='loginTag'>Validado como myuser</div>
</div>
<h1>Autorización de transferencia de datos personales a <em>Som Acme, SCCL</em></h1>
<div class='privacywarning'>
Para activar el servicio <em>Comprar explosivos</em>
en <em>Som Acme, SCCL</em>,
transferiremos a dicha entidad los siguientes datos:
<div class='transferfields'>
"""


acmeExplosivesFooter = u"""\
</div>
Dicha entidad tratar\xe1 dichos datos seg\xfan su propia
<a href='http://www.wallpapersonly.net/wallpapers/thats-all-folks-1680x1050.jpg' target='_blank'>pol\xedtica de privacidad</a>.
</div>
<a class='privacy_accept_bt' href='/confirmactivateservice/somacme/explosives'>
Acepto
</a>
</body>
</html>
"""

nameField = u"""\
<div class='field'>
<div class='fieldheader'>NIF:</div>
<div class='fieldvalue'>12345678Z</div>
</div>
"""
originField = u"""\
<div class='field'>
<div class='fieldheader'>Entidad de procedencia:</div>
<div class='fieldvalue'>somillusio</div>
</div>
"""

class Portal_Test(unittest.TestCase):

    def write(self, filename, content, folder=None):
        fullname = os.path.join(folder or self.peerdatadir,filename)
        with open(fullname, 'wb') as f:
            try:
                f.write(content.encode('utf-8'))
            except UnicodeDecodeError:
                f.write(content)


    def setUp(self):
        self.maxDiff=None
        self.peerid= 'somillusio'
        self.keyfile = 'testkey.pem'
        self.peerdatadir='peerdatadir'
        self.userdatadir='userdatadir'
        self.cleanUp()
        os.system("mkdir -p "+self.peerdatadir)
        os.system("mkdir -p "+self.userdatadir)
        self.write('myuser.yaml', myuseryaml, self.userdatadir)

    def setupPortal(self):
        return portalexample.Portal("Example Portal",
            peerid = self.peerid,
            keyfile=self.keyfile,
            peers = peerinfo.PeerInfo(self.peerdatadir),
            users = userinfo.UserInfo(self.userdatadir),
            )

    def setupApp(self):
        self.portal = self.setupPortal()
        self.app =  self.portal.app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()


    def tearDown(self):
        self.cleanUp()

    def cleanUp(self):
        try: shutil.rmtree(self.peerdatadir)
        except: pass
        try: shutil.rmtree(self.userdatadir)
        except: pass

    def test_index_whenEmpty(self):
        self.setupApp()
        self.assertMultiLineEqual(
            header+footer,
            self.client.get("/").data.decode('utf-8')
            )

    def test_serviceDescription(self):
        peer = ns.loads(somacmeyaml)
        p = self.setupPortal()
        self.assertMultiLineEqual(
            p.serviceDescription(peer, 'explosives'),
            acmeService)

    def test_peerDescription_singleService(self):
        peer = ns.loads(sombogusyaml)
        p = self.setupPortal()
        self.assertMultiLineEqual(
            p.peerDescription(peer),
            bogusPeerHeader + bogusService + peerFooter)

    def test_peerDescription_manyServices(self):
        peer = ns.loads(somacmeyaml)
        p = self.setupPortal()
        self.assertMultiLineEqual(
            p.peerDescription(peer),
            acmePeerHeader + acmeService + acmeService2 + peerFooter)

    def test_index_onePeer(self):
        self.setupApp()
        self.write('somacme.yaml',somacmeyaml)
        self.assertMultiLineEqual(
            header+
            acmePeerHeader+
            acmeService+
            acmeService2+
            peerFooter+
            footer,
            self.client.get("/").data.decode('utf-8')
            )

    def test_index_many(self):
        self.setupApp()
        self.write('somacme.yaml',somacmeyaml)
        self.write('sombogus.yaml',sombogusyaml)
        self.assertMultiLineEqual(
            header+
            acmePeerHeader+
            acmeService+
            acmeService2+
            peerFooter+
            bogusPeerHeader+
            bogusService+
            peerFooter+
            footer,
            self.client.get("/").data.decode('utf-8')
            )

    def test_renderField(self):
        p = self.setupPortal()
        self.assertMultiLineEqual(
            p.renderField(field="Nombre", value="Bunny, Bugs"),
            "<div class='field'>\n"
            "<div class='fieldheader'>Nombre:</div>\n"
            "<div class='fieldvalue'>Bunny, Bugs</div>\n"
            "</div>\n"
            )

    def test_renderField_list(self):
        p = self.setupPortal()
        self.assertMultiLineEqual(
            p.renderField(field=u"Teléfono", value=["5550000", "5554455"]),
            "<div class='field'>\n"
            u"<div class='fieldheader'>Teléfono:</div>\n"
            "<div class='fieldvalue'>\n"
                "<ul>\n"
                "<li>5550000</li>\n"
                "<li>5554455</li>\n"
                "</ul>\n"
            "</div>\n"
            "</div>\n"
            )

    def test_renderField_none(self):
        p = self.setupPortal()
        self.assertMultiLineEqual(
            p.renderField(field=u"Attribute label", value=None),
            "<div class='field'>\n"
            "<div class='fieldheader'>Attribute label:</div>\n"
            "<div class='fieldvalue'>---</div>\n"
            "</div>\n"
            )

    def test_activateService(self):
        self.setupApp()
        self.write("somacme.yaml",somacmeyaml)
        self.assertMultiLineEqual(
            acmeExplosivesHeader+
            originField+
            nameField+
            acmeExplosivesFooter,
            self.client.get("/activateservice/somacme/explosives").data.decode('utf-8'))



# vim: ts=4 sw=4 et
