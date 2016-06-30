# -*- encoding: utf-8 -*-

import unittest
from . import portal
from . import peerdatastorage

class Portal_Test(unittest.TestCase):
    index_html=(u"""\
<html>
<head>
<meta encoding='utf-8' />
<title>Example Portal</title>
</head>
<body>
<h1>Intercooperación</h1>
<ul>
<li>Som Acme, SCCL
<ul>
<li>contract</li>
</ul>
</li>
<li>Som Bogus, SCCL
<ul>
<li>contract</li>
</ul>
</li>
</ul>
</body>
</html>
"""
    )
    datadir="peerdata"

    somacmeyaml=u"""\
    intercoopVersion: 1.0
    peerVersion: 1
    peerid: somacme
    name: Som Acme, SCCL
    services:
      contract:
        es: Contrata explosivos éticos
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

    def writeFile(self, filename, content):
        import os
        with open(os.path.join(self.datadir,filename),'wb') as f:
            f.write(content.encode('utf-8'))
        
    def setUp(self):
        import os
        self.cleanUp()
        self.maxDiff=None
        os.system("mkdir -p "+self.datadir)
        self.writeFile('somacme.yaml',self.somacmeyaml)
        self.writeFile('sombogus.yaml',self.sombogusyaml)

        app = portal.Portal("Example Portal", peerdata=self.datadir).app
        app.config['TESTING'] = True
        self.client = app.test_client()

    def tearDown(self):
        self.cleanUp()

    def cleanUp(self):
        import shutil
        try:
            shutil.rmtree(self.datadir)
        except: pass    

    def test_index(self):
        self.assertMultiLineEqual(
            self.index_html,
            self.client.get("/").data.decode('utf-8')
            )


# vim: ts=4 sw=4 et
