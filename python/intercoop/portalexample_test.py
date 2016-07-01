# -*- encoding: utf-8 -*-

import unittest
import os
import shutil
from . import portalexample
from . import peerdatastorage
from yamlns import namespace as ns

somacmeyaml=u"""\
intercoopVersion: 1.0
peerVersion: 1
peerid: somacme
name: Som Acme, SCCL
logo: http://www.linpictures.com/images/indevimgs/acme.jpg
url:
  es: http://somacme.coop/es
description:
  es: >
    La cooperativa para atrapar correcaminos
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
logo: http://www.linpictures.com/images/indevimgs/acme.jpg
url:
  es: https://es.sombogus.coop
description:
    es: >
      Productos inútiles pero muy éticos
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
<link rel="stylesheet" type="text/css" href="intercoop.css">
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
<title>Activación servicio explosives</title>
<link rel="stylesheet" type="text/css" href="intercoop.css">
</head>
<body>
<h1>Campos que se enviarán al servicio explosives</h1>
"""

acmeExplosivesFooter = u"""\
</div>
</body>
</html>
"""

nameField = u"""\
<div class='field'>
<div class='fieldheader'>Nombre:</div>
<div class='fieldvalue'>Bunny, Bugs</div>
"""

class Portal_Test(unittest.TestCase):

    def write(self, filename, content):
        fullname = os.path.join(self.datadir,filename)
        with open(fullname, 'wb') as f:
            f.write(content.encode('utf-8'))
        
    def setUp(self):
        self.maxDiff=None
        self.datadir="peerdatadir"
        self.cleanUp()
        os.system("mkdir -p "+self.datadir)

        portal = self.setupPortal()
        app = portal.app
        app.config['TESTING'] = True
        self.client = app.test_client()

    def setupPortal(self):
        return portalexample.Portal("Example Portal", peerdatadir=self.datadir)

    def tearDown(self):
        self.cleanUp()

    def cleanUp(self):
        try:
            shutil.rmtree(self.datadir)
        except: pass    

    def test_index_whenEmpty(self):
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

    def test_activateService(self):
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        self.assertMultiLineEqual(
            acmeExplosivesHeader+
            nameField+
            acmeExplosivesFooter, 
            self.client.get("/activateservice/somacme/explosives").data.decode('utf-8'))
    
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

# vim: ts=4 sw=4 et
