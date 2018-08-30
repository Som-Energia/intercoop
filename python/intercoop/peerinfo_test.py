# -*- encoding: utf-8 -*-
import unittest
from . import peerinfo
from yamlns import namespace as ns
import os

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

class PeerInfo_Test(unittest.TestCase):
    
    def setUp(self):
        import os
        self.peerdatadir = "peerdata"
        self.cleanUp()

        os.makedirs(self.peerdatadir)
        self.write('somacme.yaml', somacmeyaml)
        self.write('sombogus.yaml', sombogusyaml)
        

    def tearDown(self):
        self.cleanUp()

    def cleanUp(self):
        import shutil
        try:
            shutil.rmtree(self.peerdatadir)
        except: pass

    def write(self, filename, content):
        with open(os.path.join(self.peerdatadir, filename),'w') as f:
            f.write(content)


    def test_get(self):
        self.write('somacme.yaml', somacmeyaml)

        s = peerinfo.PeerInfo(self.peerdatadir)
        peerData = s.get("somacme")
        self.assertEqual(peerData,ns.loads(somacmeyaml))

    def test_get_badpeer(self):
        s = peerinfo.PeerInfo(self.peerdatadir)
        with self.assertRaises(Exception) as ctx:
            peerData = s.get("badpeer")

        self.assertEqual(format(ctx.exception),
            "Not such peer 'badpeer'")
 
    def test_get_invalidpeer(self):
        s = peerinfo.PeerInfo(self.peerdatadir)
        with self.assertRaises(Exception) as ctx:
            peerData = s.get("../../etc/passwd")

        self.assertEqual(format(ctx.exception),
            "Invalid peer '../../etc/passwd'")
 
    def test_iter(self):
        s = peerinfo.PeerInfo(self.peerdatadir)
        self.assertEqual(list(s),[
                ns.loads(somacmeyaml),
                ns.loads(sombogusyaml),
            ]
        )


# vim: ts=4 sw=4 et
