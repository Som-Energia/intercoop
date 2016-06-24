# -*- encoding: utf-8 -*-

import unittest
import intercoop
from . import crypto
import os
from yamlns import namespace as ns

class KeyRingMock(object):
    def __init__(self, keys):
        self.keys = keys
    def get(self, key):
        return self.keys[key]

class IntercoopMessage_Test(unittest.TestCase):

    yaml=u"""\
intercoopVersion: '1.0'
originpeer: testpeer
origincode: 666
name: Perico de los Palotes
address: Percebe, 13
city: Villarriba del Alcornoque
state: Albacete
postalcode: '01001'
country: ES
"""
    def setUp(self):
        self.maxDiff = None
        self.keyfile = 'testkey.pem'
        self.pubfile = 'testkey-public.pem'

        if not os.access(self.keyfile, os.F_OK):
            intercoop.generateKeyPair(self.keyfile, self.pubfile)

        self.key = crypto.loadKeyPair(self.keyfile)
        self.public = crypto.loadKeyPair(self.pubfile)
        self.values = ns.loads(self.yaml)
        self.encodedPayload1 = crypto.encode(self.yaml)
        self.signedPayload1 = crypto.sign(self.key, self.yaml)
        self.keyring = KeyRingMock(dict(
            testpeer=self.public,
            ))

    def test_produce(self):
        g = intercoop.Generator(ownKeyPair = self.key)
        message = g.produce(self.values)
        self.assertEqual(
            dict(ns.loads(message)),
            dict(
                intercoopVersion = '1.0',
                signature = self.signedPayload1,
                payload = self.encodedPayload1,
            ))

    def setupMessage(self,
            values=None,
            yaml=None,
            signedyaml=None,
            payload=None,
            ):
        values = ns(values or self.values)
        yaml = yaml or values.dump()
        return ns(
            intercoopVersion = '1.0',
            signature = crypto.sign(self.key, signedyaml or yaml),
            payload = payload or crypto.encode(yaml),
            ).dump()

    def assertParseRaises(self, parser, message, exception, errorMessage):
        with self.assertRaises(exception) as ctx:
            parser.parse(message)
        self.assertEqual(ctx.exception.args[0], errorMessage)


    def test_parse(self):
        message = self.setupMessage()

        g = intercoop.Parser(keyring = self.keyring)
        values = g.parse(message)
        self.assertEqual(
            dict(self.values),
            dict(values),
            )

    def test_parse_withUnrecognizedPeer(self):
        g = intercoop.Parser(keyring = self.keyring)
        message = self.setupMessage(
            values=ns(self.values, originpeer='badpeer')
            )
        self.assertParseRaises(g,message,
            intercoop.BadPeer,
            "The entity 'badpeer' is not a recognized one")

    def test_parse_withInvalidSignature(self):
        g = intercoop.Parser(keyring = self.keyring)
        message = self.setupMessage(
            signedyaml = self.yaml + "\n",
            )
        self.assertParseRaises(g, message,
            intercoop.BadSignature,
            "Signature verification failed, untrusted content")


unittest.TestCase.__str__ = unittest.TestCase.id



if __name__ == "__main__":
    import sys
    unittest.main()


# vim: ts=4 sw=4 et
