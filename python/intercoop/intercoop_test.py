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
            intercoop.generateKey(self.keyfile, self.pubfile)

        self.key = crypto.loadKey(self.keyfile)
        self.public = crypto.loadKey(self.pubfile)
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
            removedFromMessage=[],
            version=None,
            ):
        values = ns(values or self.values)
        yaml = yaml or values.dump()
        messageValues =  ns(
            intercoopVersion = version or intercoop.protocolVersion,
            signature = crypto.sign(self.key, signedyaml or yaml),
            payload = payload or crypto.encode(yaml),
            )

        for field in removedFromMessage:
            del messageValues[field]
        return messageValues.dump()

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

    def test_parse_unrecognizedPeer(self):
        g = intercoop.Parser(keyring = self.keyring)
        message = self.setupMessage(
            values=ns(self.values, originpeer='badpeer')
            )
        self.assertParseRaises(g,message,
            intercoop.BadPeer,
            "The entity 'badpeer' is not a recognized one")

    def test_parse_invalidSignature(self):
        g = intercoop.Parser(keyring = self.keyring)
        message = self.setupMessage(
            signedyaml = self.yaml + "\n",
            )
        self.assertParseRaises(g, message,
            intercoop.BadSignature,
            "Signature verification failed, untrusted content")

    def test_parse_missingPeerField(self):
        g = intercoop.Parser(keyring = self.keyring)
        values= ns(self.values)
        del values.originpeer
        message = self.setupMessage(values=values)
        self.assertParseRaises(g, message,
            intercoop.MissingField,
            "Required field 'originpeer' missing on the payload")

    def test_parse_badYaml(self):
        g = intercoop.Parser(keyring = self.keyring)
        message = self.setupMessage(yaml='\t')
        self.assertParseRaises(g, message,
            intercoop.BadFormat,
            "Error while parsing message as YAML:\n"
            "while scanning for the next token\n"
            "found character '\\t' that cannot start any token\n"
            "  in \"<file>\", line 1, column 1"
            )

    def test_parse_missingPayload(self):
        g = intercoop.Parser(keyring = self.keyring)
        message = self.setupMessage(
            removedFromMessage=['payload']
            )
        self.assertParseRaises(g, message,
            intercoop.BadMessage,
            "Malformed message: missing payload"
            )

    def test_parse_missingSignature(self):
        g = intercoop.Parser(keyring = self.keyring)
        message = self.setupMessage(
            removedFromMessage=['signature']
            )
        self.assertParseRaises(g, message,
            intercoop.BadMessage,
            "Malformed message: missing signature"
            )

    def test_parse_missingVersion(self):
        g = intercoop.Parser(keyring = self.keyring)
        message = self.setupMessage(
            removedFromMessage=['intercoopVersion']
            )
        self.assertParseRaises(g, message,
            intercoop.BadMessage,
            "Malformed message: missing intercoopVersion"
            )

    def test_parse_wrongVersion(self):
        g = intercoop.Parser(keyring = self.keyring)
        message = self.setupMessage(
            version='0.0',
            )
        self.assertParseRaises(g, message,
            intercoop.WrongVersion,
            "Wrong protocol version, expected 1.0, received 0.0"
            )

    def test_parse_badContainerYaml(self):
        g = intercoop.Parser(keyring = self.keyring)
        self.assertParseRaises(g, '\t',
            intercoop.BadMessage,
            "Malformed message: Bad message YAML format\n"
            "while scanning for the next token\n"
            "found character '\\t' that cannot start any token\n"
            "  in \"<file>\", line 1, column 1"
            )

    def test_parse_badContainerUnicode(self):
        g = intercoop.Parser(keyring = self.keyring)
        message = self.setupMessage(
            payload = "SAFASLDFKJASLK==",
            )
        self.assertParseRaises(g, message,
            intercoop.BadMessage,
            'Malformed message: Payload is not base64 coded UTF8'
            )

    def test_parse_badPayloadBase64(self):
        g = intercoop.Parser(keyring = self.keyring)
        message = self.setupMessage(
            payload = "SO",
            )
        self.assertParseRaises(g, message,
            intercoop.BadMessage,
            'Malformed message: Payload is invalid Base64: Incorrect padding'
            )


unittest.TestCase.__str__ = unittest.TestCase.id


if __name__ == "__main__":
    import sys
    unittest.main()


# vim: ts=4 sw=4 et
