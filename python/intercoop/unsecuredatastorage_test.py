# -*- encoding: utf-8 -*-

from . import unsecuredatastorage as datastorage
import unittest
import os
import shutil
from yamlns import namespace as ns

class UnsecureDataStorage_Test(unittest.TestCase):

    def setUp(self):
        self.datadir = 'testdata'
        self.cleanUp()
        os.makedirs(self.datadir)

    def cleanUp(self):
        try:
            shutil.rmtree(self.datadir)
        except: pass
        
    def tearDown(self):
        self.cleanUp()

    def test_init_checkDirectory(self):
        with self.assertRaises(Exception) as ctx:
            datastorage.DataStorage('badpath')

        self.assertEqual(str(ctx.exception),
            "Storage folder 'badpath' should exist")

    def test_store(self):
        s = datastorage.DataStorage(self.datadir)
        token = s.store(dato1='valor1')
        stored = ns.load(os.path.join(self.datadir, token+'.yaml'))
        self.assertEqual(stored.dato1, 'valor1')







# vim: ts=4 sw=4 et
