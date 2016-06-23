# -*- encoding: utf-8 -*-

import unittest
import intercoop
import os
from yamlns import namespace as ns

"""
TODO:
- base64 strings
- Unsafe yamls
- Review take yaml's as unicode
- Parser takes key from dictionary and chooses acoording the peer code
- Error handling: bad peer code
- Error handling: message is not valid yaml
- Error handling: payload does not decode as valid yaml
- Error handling: message has not the required fields
- Error handling: payload has not the required fields
"""

class Crypto_Test(unittest.TestCase):

    payload1 = "this is the content\n"
    encodedPayload1 = "dGhpcyBpcyB0aGUgY29udGVudAo="
    signedPayload1 = (
        "AxmEUIQBd82wC4+9Jm337gWbvMapcLMVvE3Ord9wvnFmvuMUW7qzO+uI8IacrW"
        "6uPWM+93g9Y6q2YjfeQCZl/JB7lJorY5PLgSXhvu0+TcCPFkaIEAh7+4TllQx/"
        "+hwoN1Q3REOy+pB12iJZf9XrrOejfGG83kqXmXElSeS5RAWKwt2FcJFLIZIRZ9"
        "CDHRvX31428YURv+HlmpklwBE/t6WSJmc+b4dCcTDKih+eJ3OteDvMcsN/0H76"
        "uzEZTbJf3GwH8m5lCjNkWKVufBP/J2aQ+LvtgKiuyZI6lP9TcffVda9k4vdM2z"
        "oPDtGTAxZQz68suevbGbAM/fYnBge2FA=="
        )

    def setUp(self):
        self.maxDiff = None
        self.keyfile = 'testkey.pem'
        if not os.access(self.keyfile, os.F_OK):
            self.key = intercoop.generateKeyPair(self.keyfile)
        self.key = intercoop.loadKeyPair(self.keyfile)

    def test_encode(self):
        encoded = intercoop.encode(self.payload1)
        self.assertMultiLineEqual(self.encodedPayload1, encoded)

    def test_decode(self):
        decoded = intercoop.decode(self.encodedPayload1)
        self.assertMultiLineEqual(self.payload1, decoded)

    def test_sign(self):
        signature = intercoop.sign(self.key, self.payload1)
        self.assertMultiLineEqual(signature, self.signedPayload1)

    def test_isAuthentic_whenOk(self):
        result = intercoop.isAuthentic(self.key, self.payload1, self.signedPayload1)
        self.assertTrue(result)

    def test_isAuthentic_whenPayloadChanged(self):
        badPayload ="this is NOT the content\n"
        result = intercoop.isAuthentic(self.key, badPayload, self.signedPayload1)
        self.assertFalse(result)


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
    values = ns.loads(payload1)
    encodedPayload1 = intercoop.encode(payload1)

    def setUp(self):
        self.maxDiff = None
        self.keyfile = 'testkey.pem'
        if not os.access(self.keyfile, os.F_OK):
            self.key = intercoop.generateKeyPair(self.keyfile)
        self.key = intercoop.loadKeyPair(self.keyfile)
        self.signedPayload1 = intercoop.sign(self.key, self.payload1)

    def test_produce(self):
        g = intercoop.Generator(ownKeyPair = self.key)
        message = unicode(g.produce(self.values))
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
            




if __name__ == "__main__":
    import sys
    unittest.TestCase.__str__ = unittest.TestCase.id
    unittest.main()


# vim: ts=4 sw=4 et
