# -*- encoding: utf-8 -*-
import unittest
from . import portal
from . import peerdatastorage

class Portal_Test(unittest.TestCase):
    index_html=("""<html>
            <head></head>
            <body>Lista de peers
            <ul>
                <li>Som Acme, SCCL"""
            """<ul>"""
            """<li>contract</li>"""
            """</ul></li>"""
            """</br><li>Som Bogus, SCCL<ul>"""
            """<li>contract</li>"""
            """</ul>"""
            """</li>
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
    def setUp(self):
        import os
        import codecs
        self.cleanUp()
        self.maxDiff=None
        os.system("mkdir -p "+self.datadir)
        with codecs.open(os.path.join(self.datadir, 'somacme.yaml'),'w','utf-8') as f:
            f.write(self.somacmeyaml)
        with codecs.open(os.path.join(self.datadir, 'sombogus.yaml'),'w','utf-8') as f:
            f.write(self.sombogusyaml)
        app = portal.Portal("testportal",self.datadir).app
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
        self.assertMultiLineEqual(self.index_html,self.client.get("/").data.decode('utf-8'))
