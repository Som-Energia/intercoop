import unittest
from . import portal
from . import peerdatastorage

class Portal_Test(unittest.TestCase):
    index_html="""<html>
            <head></head>
            <body>Lista de peers
            <ul>
                <li>Som Acme, SCCL</li></br><li>Som Bogus, SCCL</li>
            </ul>
            </body>
            </html>
            """
    datadir="peerdata"

    somacmeyaml=u"""\
    intercoopVersion: 1.0
    peerVersion: 1
    peerid: somacme
    name: Som Acme, SCCL
    """

    sombogusyaml=u"""\
    intercoopVersion: 1.0
    peerVersion: 1
    peerid: sombogus
    name: Som Bogus, SCCL
    """
    def setUp(self):
        import os
        self.cleanUp()
        os.system("mkdir -p "+self.datadir)
        with open(os.path.join(self.datadir, 'somacme.yaml'),'w') as f:
            f.write(self.somacmeyaml)
        with open(os.path.join(self.datadir, 'sombogus.yaml'),'w') as f:
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
        self.assertEqual(self.index_html,self.client.get("/").data.decode('utf-8'))
