# -*- encoding: utf-8 -*-
import unittest
from . import peerdatastorage
from yamlns import namespace as ns

"""
# TODO's

- [x] Hacer el setUp
- [x] Get cuando funciona
- [x] Get cuando no está
- [ ] Constructor error when no such folder
- [ ] Proteger contra peerid's maliciosos (../../) limitando a letras numeros y signos de separacion validos
- [ ] Own exception types (not just plain Exception)
- [x] Iterador
- [ ] Accesores mas semanticos
"""

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
class PeerDataStorage_Test(unittest.TestCase):
    
    def setUp(self):
        import os
        self.peerdatadir = "peerdata"
        self.cleanUp()
        os.system("mkdir -p "+self.peerdatadir)
        with open(os.path.join(self.peerdatadir, 'somacme.yaml'),'w') as f:
            f.write(somacmeyaml)
        with open(os.path.join(self.peerdatadir, 'sombogus.yaml'),'w') as f:
            f.write(sombogusyaml)
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
        self.assertEqual(peerData,ns.loads(somacmeyaml))

    def test_badpeer(self):
        s = peerdatastorage.PeerDataStorage(self.peerdatadir)
        with self.assertRaises(Exception) as ctx:
            peerData = s.get("badpeer")

        self.assertEqual(str(ctx.exception),
            "Not such peer 'badpeer'")
 
    def test_iterator(self):
        s = peerdatastorage.PeerDataStorage(self.peerdatadir)
        peerDataList = list(e for e in s)
        try:
            self.assertCountEqual(peerDataList,[
                    ns.loads(somacmeyaml),
                    ns.loads(sombogusyaml),
                ]
            )
        except AttributeError:
            self.assertItemsEqual(peerDataList,[
                    ns.loads(somacmeyaml),
                    ns.loads(sombogusyaml),
                ]
            )


# vim: ts=4 sw=4 et
