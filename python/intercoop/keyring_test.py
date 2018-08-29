#!/usr/bin/env python

import unittest
from . import peerinfo
from . import keyring
from . import crypto
from yamlns import namespace as ns
import os


somacmeyaml=u"""\
intercoopVersion: 1.0
peerVersion: 1
peerid: somacme
name: Som Acme, SCCL
publickey: |  # should be the same content than 
  -----BEGIN PUBLIC KEY-----
  MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6NNjLFEswRPwzTbuD1Oa
  H9eIVR3U/8iBxQR9jgExqCEI/4oBjBk/eZmYOVdygkZgTeU0TxD5NFd5Zd0Cewz3
  kTkUHJ9YLHSb2SClE6pYlocRYlrvPxEa0XIF+ujRcpKUk5UpEcFNzmNS0s7cUpB+
  UufeEUSyiETeMlu0pqhIXQZSQlgxBt3Fb4vUv8E2Jp1jb4b8A7iygN7oPE7800NX
  VqoCLTnoc3IPDTPugoxfH59rY7LZH0yCCFl5gIAmM1J+w6YFdfjSSwZyE4w/0aF8
  Y4CXTEOoo8f0vTnpN96or4ObdI1ZMwU8b7rpxEHmP2exAul9FnoEZytVtteAYpIt
  QwIDAQAB
  -----END PUBLIC KEY-----
"""

sombogusyaml=u"""\
intercoopVersion: 1.0
peerVersion: 1
peerid: sombogus
name: Som Bogus, SCCL
"""

class KeyRing_Test(unittest.TestCase):
    
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
        ring = keyring.KeyRing(s)
        key = ring.get("somacme")
        private = crypto.loadKey('testkey.pem')
        self.assertMultiLineEqual(
            crypto.exportString(private.publickey()),
            crypto.exportString(key.publickey()),
        )
        signature = crypto.sign(private, 'text')
        self.assertTrue(crypto.isAuthentic(key, 'text', signature))

    def test_get_badpeer(self):
        s = peerinfo.PeerInfo(self.peerdatadir)
        ring = keyring.KeyRing(s)
        with self.assertRaises(Exception) as ctx:
            key = ring.get("badpeer")

        self.assertEqual(format(ctx.exception),
            "Not such peer 'badpeer'")
 
    def test_get_invalidpeer(self):
        s = peerinfo.PeerInfo(self.peerdatadir)
        ring = keyring.KeyRing(s)
        with self.assertRaises(Exception) as ctx:
            key = ring.get("../../etc/passwd")

        self.assertEqual(format(ctx.exception),
            "Invalid peer '../../etc/passwd'")

    def test_get_noPublicKeyInYaml(self):
        # TODO: Some other exception should be raised
        self.write('sombogus.yaml', sombogusyaml)

        s = peerinfo.PeerInfo(self.peerdatadir)
        ring = keyring.KeyRing(s)
        with self.assertRaises(AttributeError) as ctx:
            key = ring.get("sombogus")
        self.assertEqual(format(ctx.exception),
            "publickey")

    def test_get_invalidKeyFormat(self):
        # TODO: Some other exception should be raised
        self.write('sombogus.yaml', sombogusyaml+
            "publickey: caca\n"
        )

        s = peerinfo.PeerInfo(self.peerdatadir)
        ring = keyring.KeyRing(s)
        with self.assertRaises(Exception) as ctx:
            key = ring.get("sombogus")
        self.assertEqual(format(ctx.exception),
            "RSA key format is not supported")


# vim: ts=4 sw=4 et
