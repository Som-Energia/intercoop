# -*- encoding: utf-8 -*-
import unittest
from . import peerdatastorage
from yamlns import namespace as ns

"""
# TODO's

- [x] Hacer el setUp
- [x] Get cuando funciona
- [ ] Get cuando no está
- [ ] Proteger contra peerid's maliciosos (../../) limitando a letras numeros y signos de separacion validos
- [ ] Iterador
- [ ] Accesores mas semanticos
"""

somacmeyaml=u"""\
intercoopVersion: 1.0
peerVersion: 1
peerid: somacme
name: Som Acme, SCCL
"""


class PeerDataStorage_Test(unittest.TestCase):
    
    def setUp(self):
        import os
        self.peerdatadir = "peerdata"
        self.cleanUp()
        os.system("mkdir -p "+self.peerdatadir)
        with open(os.path.join(self.peerdatadir, 'somacme.yaml'),'w') as f:
            f.write(somacmeyaml)

    def tearDown(self):
        self.cleanUp()

    def cleanUp(self):
        import shutil
        try:
            shutil.rmtree(self.peerdatadir)
        except: pass


    def test_get(self):
        s = peerdatastorage.PeerDataStorage(self.peerdatadir)
        peerData = s.get("somacme")
        self.assertEqual(peerData,ns.loads(somacmeyaml)) # TODO: proper value

# vim: ts=4 sw=4 et
