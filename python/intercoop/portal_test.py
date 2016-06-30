# -*- encoding: utf-8 -*-

import unittest
import os
import shutil
from . import portal
from . import peerdatastorage
from yamlns import namespace as ns

header= u"""\
<html>
<head>
<meta encoding='utf-8' />
<title>Example Portal</title>
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

descripcionAcme = u"""\
<div class='service'>
<a href='activateservice/somacme/explosives'>
<div class='service_header'>Comprar explosivos</div>
<div class='service_description>Puedes comprar explosivos éticos de la mejor calidad.
</div>
</a>
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

    somacmeyaml=u"""\
    intercoopVersion: 1.0
    peerVersion: 1
    peerid: somacme
    name: Som Acme, SCCL
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
    services:
      contract:
        es: Contrata 
    """

    def write(self, filename, content):
        fullname = os.path.join(self.datadir,filename)
        with open(fullname, 'wb') as f:
            f.write(content.encode('utf-8'))
        
    def setUp(self):
        self.maxDiff=None
        self.datadir="peerdata"
        self.cleanUp()
        os.system("mkdir -p "+self.datadir)

        app = portal.Portal("Example Portal", peerdata=self.datadir).app
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

    def test_index_many(self):
        self.write('somacme.yaml',self.somacmeyaml)
        self.write('sombogus.yaml',self.sombogusyaml)
        self.assertMultiLineEqual(
            header+self.descriptions+footer,
            self.client.get("/").data.decode('utf-8')
            )

    def test_serviceDescription(self):
        peer = ns.loads(self.somacmeyaml.encode('utf-8'))
        p = portal.Portal("Example Portal", peerdata=self.datadir)
        self.assertMultiLineEqual(
            p.serviceDescription(peer, 'explosives'),
            descripcionAcme)



# vim: ts=4 sw=4 et
