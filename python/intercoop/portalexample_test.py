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


class Portal_Test(unittest.TestCase):
    descriptions=(u"""\
<li>Som Acme, SCCL
<ul>
<li>explosives</li>
</ul>
</li>
<li>Som Bogus, SCCL
<ul>
<li>contract</li>
</ul>
</li>
"""
    )

    def write(self, filename, content):
        fullname = os.path.join(self.datadir,filename)
        with open(fullname, 'wb') as f:
            f.write(content.encode('utf-8'))
        
    def setUp(self):
        self.maxDiff=None
        self.datadir="peerdata"
        self.cleanUp()
        os.system("mkdir -p "+self.datadir)

        app = portalexample.Portal("Example Portal", peerdata=self.datadir).app
        app.config['TESTING'] = True
        self.client = app.test_client()

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
        p = portalexample.Portal("Example Portal", peerdata=self.datadir)
        self.assertMultiLineEqual(
            p.serviceDescription(peer, 'explosives'),
            acmeService)

    def test_peerDescription_withSingleService(self):
        peer = ns.loads(somacmeyaml.encode('utf-8'))
        p = portalexample.Portal("Example Portal", peerdata=self.datadir)
        self.assertMultiLineEqual(
            p.peerDescription(peer),
            acmePeerHeader + acmeService + peerFooter)

    def test_index_onePeer(self):
        self.write('somacme.yaml',somacmeyaml)
        self.assertMultiLineEqual(
            header+
            acmePeerHeader+
            acmeService+
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
            peerFooter+
            bogusPeerHeader+
            bogusService+
            peerFooter+
            footer,
            self.client.get("/").data.decode('utf-8')
            )


# vim: ts=4 sw=4 et
