# -*- encoding: utf-8 -*-

import unittest
import os
import shutil
from . import portalexample
from . import peerdatastorage
from yamlns import namespace as ns


myuseryaml=u"""\
nif: 12345678Z
name: Bunny, Bugs
peerroles:
- member
- worker
innerid: 666
address: Golf Club, 5th hole
city: Murcia
state: Murcia
postalcode: '01022'
country: ES
email:
- bugsbunny@loonietoons.com
phone:
- '555121232'
proxynif:
proxyname:
"""

somacmeyaml=u"""\
intercoopVersion: 1.0
peerVersion: 1
peerid: somacme
name: Som Acme, SCCL
url:
  es: http://somacme.coop/es
logo: http://www.linpictures.com/images/indevimgs/acme.jpg
privacyPolicyUrl:
  es: http://www.wallpapersonly.net/wallpapers/thats-all-folks-1680x1050.jpg
description:
  es: >
    La cooperativa para atrapar correcaminos
targetUrl: http://localhost:5001/intercoop/
services:
  explosives:
    name:
      es: Comprar explosivos
    description:
      es: >
        Puedes comprar explosivos éticos de la mejor calidad.
  anvil:
    name:
      es: Comprar yunques
    description:
      es: >
        Yunques garantizados, siempre caen en una cabeza
    fields:
      innerid:
        es: Número de socio/a
fields:
  nif:
    es: NIF
"""

sombogusyaml=u"""\
intercoopVersion: 1.0
peerVersion: 1
peerid: sombogus
name: Som Bogus, SCCL
url:
  es: https://es.sombogus.coop
logo: http://www.linpictures.com/images/indevimgs/acme.jpg
privacyPolicyUrl: 
    es: http://www.wallpapersonly.net/wallpapers/thats-all-folks-1680x1050.jpg
description:
    es: >
      Productos inútiles pero muy éticos
targetUrl: http://localhost:5002/intercoop/
services:
  contract:
    name:
        es: Contrata 
    description:
        es: >
          Productos con marcas tipo Panone, Grifons, Pas Natural, Reacciona...
    fields:
      name:
        es: Nombre      
"""

header= u"""\
<html>
<head>
<meta encoding='utf-8' />
<title>Example Portal</title>
<link rel="stylesheet" type="text/css" href="/intercoop.css">
</head>
<body>
<h1>Intercooperación</h1>
<ul>
"""

footer = u"""\
</ul>
</body>
</html>
"""

acmePeerHeader = """\
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
<div class='peerlogo'><img src='http://www.linpictures.com/images/indevimgs/acme.jpg' /></div>
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
<title>Activación del servicio 'Comprar explosivos' en 'Som Acme, SCCL'</title>
<link rel="stylesheet" type="text/css" href="/intercoop.css">
</head>
<body>
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
<div class='fieldheader'>nif:</div>
<div class='fieldvalue'>12345678Z</div>
</div>
"""

class Portal_Test(unittest.TestCase):

    def write(self, filename, content, folder=None):
        fullname = os.path.join(folder or self.peerdatadir,filename)
        with open(fullname, 'wb') as f:
            f.write(content.encode('utf-8'))
        
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
            peerdatadir=self.peerdatadir,
            userdatadir=self.userdatadir,
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
        peer = ns.loads(somacmeyaml.encode('utf-8'))
        p = self.setupPortal()
        self.assertMultiLineEqual(
            p.serviceDescription(peer, 'explosives'),
            acmeService)

    def test_peerDescription_singleService(self):
        peer = ns.loads(sombogusyaml.encode('utf-8'))
        p = self.setupPortal()
        self.assertMultiLineEqual(
            p.peerDescription(peer),
            bogusPeerHeader + bogusService + peerFooter)

    def test_peerDescription_manyServices(self):
        peer = ns.loads(somacmeyaml.encode('utf-8'))
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

    def test_requiredFields_justInService_useService(self):
        self.write("sombogus.yaml",sombogusyaml)
        p = self.setupPortal()
        self.assertEqual(
            ['name'],
            p.requiredFields("sombogus","contract")
        )
    
    def test_requiredFields_justInPeer_usePeer(self):
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        self.assertEqual(
            ['nif'],
            p.requiredFields("somacme","explosives")
        )
    
    def test_requiredFields_inServiceAndPeer_useService(self):
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        self.assertEqual(
            ['innerid'],
            p.requiredFields("somacme","anvil")
        )

    def test_requiredFields_noFields(self):
        bogus = ns.loads(sombogusyaml.encode('utf8'))
        del bogus.services.contract.fields
        self.write("sombogus.yaml",bogus.dump().decode('utf8'))
        p = self.setupPortal()
        with self.assertRaises(Exception) as ctx:
            p.requiredFields("sombogus","contract")

        self.assertEqual(str(ctx.exception),
            "Peer 'sombogus' does not specify fields for service 'contract'")

    def test_activateService(self):
        self.setupApp()
        self.write("somacme.yaml",somacmeyaml)
        self.assertMultiLineEqual(
            acmeExplosivesHeader+
            nameField+
            acmeExplosivesFooter, 
            self.client.get("/activateservice/somacme/explosives").data.decode('utf-8'))
    
    def test_fieldTranslation_existTranslationFirstLevel(self):
        self.setupApp()
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        self.assertEqual(
            "La cooperativa para atrapar correcaminos",
            p.fieldTranslation("somacme","description","es"))            

    def test_fieldTranslation_doesntExistFieldFirstLevel(self):
        self.setupApp()
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        with self.assertRaises(Exception) as ctx:
            p.fieldTranslation("somacme","badfield","es")
        self.assertEqual(str(ctx.exception),
            "Invalid field 'badfield'")

    def test_fieldTranslation_doesntExistTranslationFirstLevel(self):
        self.setupApp()
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        with self.assertRaises(Exception) as ctx:
            p.fieldTranslation("somacme","description","fr")
        self.assertEqual(str(ctx.exception),
            "Invalid translation 'fr' for field 'description'")

    def test_fieldTranslation_existTranslationManyLevels(self):
        self.setupApp()
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        self.assertEqual(
            "Yunques garantizados, siempre caen en una cabeza",
            p.fieldTranslation("somacme","services/anvil/description","es"))

# vim: ts=4 sw=4 et
