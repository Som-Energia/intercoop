# -*- encoding: utf-8 -*-
import unittest
from . import peerdatastorage
from yamlns import namespace as ns

"""
    - Hacer el setUp
    - Get cuando funciona
    - Get cuando no está
    - Iterador
"""
class PeerDataStorage_Test(unittest.TestCase):
    
    def setUp(self):
        import os
        self.peerdatadir = ("peerdatas")
        os.system("mkdir -p "+self.peerdatadir)

    def test_get(self):
        s = peerdatastorage.PeerDataStorage(self.peerdatadir)
        peerData = s.get("somacme")
        self.assertEqual(peerData,ns())

# vim: ts=4 sw=4 et
