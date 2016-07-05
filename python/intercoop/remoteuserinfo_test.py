# -*- encoding: utf-8 -*-

from . import remoteuserinfo
from . import packaging
import unittest
import os
import shutil
from yamlns import namespace as ns

class RemoteUserInfo_Test(unittest.TestCase):

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

    def test_init_badDirectory(self):
        with self.assertRaises(Exception) as ctx:
            remoteuserinfo.RemoteUserInfo('badpath')

        self.assertEqual(str(ctx.exception),
            "Storage folder 'badpath' should exist")

    def test_tokenfile(self):
        s = remoteuserinfo.RemoteUserInfo(self.datadir)
        token = (
            '01020304-0506-0708-090a-0b0c0d0e0f10'
            )
        self.assertEqual(s._tokenfile(token),
            os.path.join(self.datadir, token+'.yaml'))

    def test_tokenfile_badtoken(self):
        s = remoteuserinfo.RemoteUserInfo(self.datadir)
        token = '../../etc/passwd'

        with self.assertRaises(Exception) as ctx:
            s._tokenfile(token)

        self.assertEqual(str(ctx.exception),
            "Bad token '{}'".format(token))

    def test_store(self):
        s = remoteuserinfo.RemoteUserInfo(self.datadir)
        token = s.store(dato1='valor1')
        stored = ns.load(s._tokenfile(token))
        self.assertEqual(stored.dato1, 'valor1')

    def test_retrieve(self):
        s = remoteuserinfo.RemoteUserInfo(self.datadir)
        token = s.store(dato1='valor1')
        stored = s.retrieve(token)
        self.assertEqual(stored.dato1, 'valor1')

    def test_retrieve_nonExisting(self):
        s = remoteuserinfo.RemoteUserInfo(self.datadir)
        token = '01020304-0506-0708-090a-0b0c0d0e0f10'
        with self.assertRaises(packaging.NoSuchUuid) as ctx:
            s.retrieve(token)
        self.assertEqual(str(ctx.exception),
            "No personal data available for uuid "
            "'01020304-0506-0708-090a-0b0c0d0e0f10'")

    def test_store_usingNs(self):
        s = remoteuserinfo.RemoteUserInfo(self.datadir)
        token = s.store(ns(dato1='valor1'))
        stored = ns.load(s._tokenfile(token))
        self.assertEqual(stored.dato1, 'valor1')

    def test_store_overwritingNsValues(self):
        s = remoteuserinfo.RemoteUserInfo(self.datadir)
        token = s.store(ns(dato1='valor1'), dato1='valor2')
        stored = ns.load(s._tokenfile(token))
        self.assertEqual(stored.dato1, 'valor2')






# vim: ts=4 sw=4 et
