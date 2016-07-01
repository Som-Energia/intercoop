# -*- encoding: utf-8 -*-

from . import userinfo

import unittest
import shutil
import os

from yamlns import namespace as ns

useryaml = """\
name: de los Palotes, Perico
nif: 12345678Z
"""

class UserInfo_Test(unittest.TestCase):

    def setUp(self):
        self.datadir = 'userinfotestdir'
        self.cleanUp()
        os.makedirs(self.datadir)
        self.write('myuser.yaml', useryaml)

    def write(self, filename, content):
        filename = os.path.join(self.datadir, filename)
        with open(filename, 'wb') as f:
            f.write(content.encode('utf8'))


    def cleanUp(self):
        try: shutil.rmtree(self.datadir)
        except: pass

    def tearDown(self):
        self.cleanUp()

    def test_getFields_allFields(self):
        storage = userinfo.UserInfo(self.datadir)
        data = storage.getFields('myuser', [
            'name',
            'nif',
            ])

        self.assertEqual(data, ns.loads(useryaml))

    def test_getFields_filtering(self):
        storage = userinfo.UserInfo(self.datadir)
        data = storage.getFields('myuser', [
            'nif',
            ])

        self.assertEqual(data, ns(
            nif = '12345678Z',
            ))

    def test_getFields_baduser(self):
        storage = userinfo.UserInfo(self.datadir)
        with self.assertRaises(userinfo.BadUser) as ctx:
            storage.getFields('baduser', ['nif',])
        self.assertEqual(str(ctx.exception),
            "User not found 'baduser'")

    def test_getFields_badfield(self):
        storage = userinfo.UserInfo(self.datadir)
        with self.assertRaises(userinfo.BadField) as ctx:
            storage.getFields('myuser', ['badfield',])
        self.assertEqual(str(ctx.exception),
            "Unrecognized user field 'badfield'")



# vim: ts=4 sw=4 et
