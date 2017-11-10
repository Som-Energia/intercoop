# -*- encoding: utf-8 -*-

import unittest
from . import packaging
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
            crypto.generateKey(self.keyfile, self.pubfile)

        self.key = crypto.loadKey(self.keyfile)
        self.public = crypto.loadKey(self.pubfile)
        self.values = ns.loads(self.yaml)
        self.encodedPayload1 = crypto.encode(self.yaml)
        self.signedPayload1 = crypto.sign(self.key, self.yaml)
        self.keyring = KeyRingMock(dict(
            testpeer=self.public,
            ))

    def test_generate(self):
        message = packaging.generate(self.key, self.values)
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
            intercoopVersion = version or packaging.protocolVersion,
            signature = crypto.sign(self.key, signedyaml or yaml),
            payload = payload or crypto.encode(yaml),
            )

        for field in removedFromMessage:
            del messageValues[field]
        return messageValues.dump()

    def assertParseRaises(self, message, exception, errorMessage):
        with self.assertRaises(exception) as ctx:
            packaging.parse(self.keyring, message)
        self.assertEqual(ctx.exception.args[0], errorMessage)


    def test_parse(self):
        message = self.setupMessage()

        values = packaging.parse(self.keyring, message)
        self.assertEqual(
            dict(self.values),
            dict(values),
            )

    def test_parse_invalidSignature(self):
        message = self.setupMessage(
            signedyaml = self.yaml + "\n",
            )
        self.assertParseRaises(message,
            packaging.BadSignature,
            "Signature verification failed, untrusted content")

    def test_parse_unrecognizedPeer(self):
        message = self.setupMessage(
            values=ns(self.values, originpeer='badpeer')
            )
        self.assertParseRaises(message,
            packaging.BadPeer,
            "The entity 'badpeer' is not a recognized one")

    def test_parse_missingPeerField(self):
        values= ns(self.values)
        del values.originpeer
        message = self.setupMessage(values=values)
        self.assertParseRaises(message,
            packaging.MissingField,
            "Required field 'originpeer' missing on the payload")

    def test_parse_badYaml(self):
        message = self.setupMessage(yaml='\t')
        self.assertParseRaises(message,
            packaging.BadFormat,
            "Error while parsing message as YAML:\n"
            "while scanning for the next token\n"
            "found character '\\t' that cannot start any token\n"
            "  in \"<file>\", line 1, column 1"
            )

    def test_parse_missingPayload(self):
        message = self.setupMessage(
            removedFromMessage=['payload']
            )
        self.assertParseRaises(message,
            packaging.BadMessage,
            "Malformed message: missing payload"
            )

    def test_parse_missingSignature(self):
        message = self.setupMessage(
            removedFromMessage=['signature']
            )
        self.assertParseRaises(message,
            packaging.BadMessage,
            "Malformed message: missing signature"
            )

    def test_parse_wrongVersion(self):
        message = self.setupMessage(
            version='0.0',
            )
        self.assertParseRaises(message,
            packaging.WrongVersion,
            "Wrong protocol version, expected 1.0, received 0.0"
            )

    def test_parse_missingVersion(self):
        message = self.setupMessage(
            removedFromMessage=['intercoopVersion']
            )
        self.assertParseRaises(message,
            packaging.BadMessage,
            "Malformed message: missing intercoopVersion"
            )

    def test_parse_badContainerYaml(self):
        self.assertParseRaises('\t',
            packaging.BadMessage,
            "Malformed message: Bad message YAML format\n"
            "while scanning for the next token\n"
            "found character '\\t' that cannot start any token\n"
            "  in \"<file>\", line 1, column 1"
            )

    def test_parse_payloadIsNotUtf8(self):
        message = self.setupMessage(
            payload = "SAFASLDFKJASLK==",
            )
        self.assertParseRaises(message,
            packaging.BadMessage,
            'Malformed message: Payload is not base64 coded UTF8'
            )

    def test_parse_badPayloadBase64(self):
        message = self.setupMessage(
            payload = "SO",
            )
        self.assertParseRaises(message,
            packaging.BadMessage,
            'Malformed message: Payload is invalid Base64: Incorrect padding'
            )


unittest.TestCase.__str__ = unittest.TestCase.id


if __name__ == "__main__":
    import sys
    unittest.main()


# vim: ts=4 sw=4 et
