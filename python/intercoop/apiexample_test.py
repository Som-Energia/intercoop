# -*- encoding: utf-8 -*-

import unittest
import os
from yamlns import namespace as ns
from . import crypto
from . import apiexample
from . import packaging

class KeyRingMock(object):
    def __init__(self, keys):
        self.keys = keys
    def get(self, key):
        return self.keys[key]

class ExampleApi_Test(unittest.TestCase):

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
        self.keyfile = 'testkey.pem'
        self.pubfile = 'testkey-public.pem'
        if not os.access(self.keyfile, os.F_OK):
            crypto.generateKey(self.keyfile, self.pubfile)
        self.key = crypto.loadKey(self.keyfile)
        self.public = crypto.loadKey(self.pubfile)

        apiexample.app.config['TESTING'] = True
        self.client = apiexample.app.test_client()
        apiexample.keyring = KeyRingMock(dict(
            testpeer=self.public,
            ))


    def test_protocolVersion(self):
        r = self.client.get('/intercoop/protocolVersion')
        self.assertEqual(
            r.data.decode('utf8'),
            packaging.protocolVersion,
            )

    def test_peermember_post(self):
        g = packaging.Generator(self.key)

        r = self.client.post('/intercoop/peermember',
            data=g.produce(ns.loads(self.yaml)),
            )
        self.assertRegex(
            r.data.decode('utf8'),
            '[0-9a-f\-]+'
            )




# vim: ts=4 sw=4 et
