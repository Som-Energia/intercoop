# -*- encoding: utf-8 -*-

import unittest
import intercoop
import os
from yamlns import namespace as ns


class Crypto_Test(unittest.TestCase):

    plain = "this is the content\n"
    base64 = "dGhpcyBpcyB0aGUgY29udGVudAo="
    signed = (
        "AxmEUIQBd82wC4-9Jm337gWbvMapcLMVvE3Ord9wvnFmvuMUW7qzO-uI8IacrW"
        "6uPWM-93g9Y6q2YjfeQCZl_JB7lJorY5PLgSXhvu0-TcCPFkaIEAh7-4TllQx_"
        "-hwoN1Q3REOy-pB12iJZf9XrrOejfGG83kqXmXElSeS5RAWKwt2FcJFLIZIRZ9"
        "CDHRvX31428YURv-HlmpklwBE_t6WSJmc-b4dCcTDKih-eJ3OteDvMcsN_0H76"
        "uzEZTbJf3GwH8m5lCjNkWKVufBP_J2aQ-LvtgKiuyZI6lP9TcffVda9k4vdM2z"
        "oPDtGTAxZQz68suevbGbAM_fYnBge2FA=="
        )

    def setUp(self):
        self.maxDiff = None
        self.keyfile = 'testkey.pem'
        if not os.access(self.keyfile, os.F_OK):
            self.key = intercoop.generateKeyPair(self.keyfile)
        self.key = intercoop.loadKeyPair(self.keyfile)

    def test_encode_unicode(self):
        encoded = intercoop.encode(self.plain)
        self.assertMultiLineEqual(self.base64, encoded)

    def test_decode_unicode(self):
        decoded = intercoop.decode(self.base64)
        self.assertMultiLineEqual(self.plain, decoded)

    def test_sign(self):
        signature = intercoop.sign(self.key, self.plain)
        self.assertMultiLineEqual(signature, self.signed)

    def test_isAuthentic_whenOk(self):
        result = intercoop.isAuthentic(self.key, self.plain, self.signed)
        self.assertTrue(result)

    def test_isAuthentic_whenPayloadChanged(self):
        badPayload = "this is NOT the content\n"
        result = intercoop.isAuthentic(self.key, badPayload, self.signed)
        self.assertFalse(result)

class CryptoUnicode_Test(Crypto_Test):

    plain = u"ñáéíóúç\n"
    base64 = u"w7HDocOpw63Ds8O6w6cK"
    signed = (
        "H-4O0KH70jaYshXHcmROBZW09wCpsHb_gbaCrmnxbm3pdV3XYDRwLkY_YmPTab"
        "TizhImcwMCFO-MI4d9dQprS-tbb28hx5xlxZhHhYusSoTkDqMgjjPLBD_WjNvh"
        "aLc2FnRtYwiq4Mk6_OC94wD_zWlrMmAhPE7mQvLROSj1f9s-2HF3gtpfz2qfVo"
        "rwfQR5NfuMVbsuNSEBlgVSUytjShmGLwNIjAQHLVZCrGe5T3oSieHVD1rq2W5n"
        "TC_veaatz7M8UZ5UeqfcS-bzISA0mvOVfeuNZ4UkEgGMGtz7SMCps6qVIyN3UN"
        "iyWKxUpB0Pswa4Xj-iXSk1Po3GnfQWJQ=="
        )


class IntercoopMessage_Test(unittest.TestCase):

    payload1=u"""\
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
        if not os.access(self.keyfile, os.F_OK):
            self.key = intercoop.generateKeyPair(self.keyfile)
        self.key = intercoop.loadKeyPair(self.keyfile)

        self.values = ns.loads(self.payload1)
        self.encodedPayload1 = intercoop.encode(self.payload1)
        self.signedPayload1 = intercoop.sign(self.key, self.payload1)

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

    def test_parse(self):
        message = ns(
            intercoopVersion = '1.0',
            signature = self.signedPayload1,
            payload = self.encodedPayload1,
            ).dump()

        g = intercoop.Parser(ownKeyPair = self.key)
        values = g.parse(message)
        self.assertEqual(
            dict(self.values),
            dict(values),
            )

    class KeyRingMock(object):
        def __init__(self, keys):
            self.keys = keys
        def get(self, key):
            return self.keys[key]

    def test_parse_withInvalidSignature(self):
        message = ns(
            intercoopVersion = '1.0',
            signature = intercoop.sign(self.key, self.payload1+"\n"),
            payload = self.encodedPayload1,
            ).dump()

        g = intercoop.Parser(ownKeyPair = self.key)
        with self.assertRaises(intercoop.BadSignature) as ctx:
            g.parse(message)
        self.assertEqual(ctx.exception.args[0],
            "Signature didn't match the content, content modified")
            

unittest.TestCase.__str__ = unittest.TestCase.id



if __name__ == "__main__":
    import sys
    unittest.main()


# vim: ts=4 sw=4 et
