# -*- encoding: utf-8 -*-

import unittest
import os
import shutil
from yamlns import namespace as ns
from . import crypto
from . import apiexample
from . import packaging
from . import remoteuserinfo

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
    service="contract"
    def setUp(self):
        self.keyfile = 'testkey.pem'
        self.pubfile = 'testkey-public.pem'
        self.key = crypto.loadKey(self.keyfile)
        self.pub = crypto.loadKey(self.pubfile)
        self.keyring = KeyRingMock(dict(
            testpeer=self.pub,
            ))

        self.datadir='apiexamplestorage'
        try: os.makedirs(self.datadir)
        except: pass
        self.storage = remoteuserinfo.RemoteUserInfo(self.datadir)
        self.api = apiexample.IntercoopApi('testapi', self.storage, self.keyring)
        app = self.api.app
        app.config['TESTING'] = True
        self.client = app.test_client()

    def cleanUp(self):
        try:
            shutil.rmtree(self.datadir)
        except: pass
        
    def tearDown(self):
        self.cleanUp()


    def test__protocolVersion_get(self):
        r = self.client.get('/protocolVersion')
        self.assertEqual(
            ns.loads(r.data),
            ns(protocolVersion=packaging.protocolVersion),
            )

    def test__activateService_post__ok(self):
        data = ns.loads(self.yaml)
        package = packaging.generate(self.key, data)

        r = self.client.post('/activateService', data=package)

        data = ns.loads(r.data)
        self.assertEqual(r.status_code, 200)
        self.assertRegex(data.uuid, '^[0-9a-f\-]+$')

    def test__activateService_post__withContinuationUrl(self):
        data = ns.loads(self.yaml)
        package = packaging.generate(self.key, data)
        # TODO: Use the constructor param instead
        self.api.continuationUrlTmpl='/activateService?uuid={uuid}'

        r = self.client.post('/activateService', data=package)

        data = ns.loads(r.data)
        self.assertEqual(r.status_code, 200)
        self.assertRegex(data.uuid, '^[0-9a-f\-]+$')
        self.assertEqual(data.continuationUrl,
            '/activateService?uuid='+data.uuid)

    def test__activateService_post__badPeer(self):
        data = ns.loads(self.yaml)
        data.originpeer = 'badpeer'
        package = packaging.generate(self.key, data)

        r = self.client.post('activateService', data=package)

        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.headers.get('Content-Type'), 'application/yaml')
        self.assertEqual(ns.loads(r.data), ns(
            error = 'BadPeer',
            message = "The entity 'badpeer' is not a recognized one",
            arguments = ['badpeer'],
            ))

    def test__activateService_post__badSignature(self):
        data = ns.loads(self.yaml)
        package = ns.loads(packaging.generate(self.key, data))
        package.payload = crypto.encode(self.yaml+'\n')
        package = package.dump()

        r = self.client.post('/activateService', data=package)

        self.assertEqual(ns.loads(r.data), ns(
            error = 'BadSignature',
            message = "Signature verification failed, untrusted content",
            arguments = [],
            ))
        self.assertEqual(r.status_code, 403)

    def test__activateService_post__missingField(self):
        data = ns.loads(self.yaml)
        del data.originpeer
        package = packaging.generate(self.key, data)

        r = self.client.post('/activateService', data=package)

        self.assertEqual(ns.loads(r.data), ns(
            error = 'MissingField',
            message = "Required field 'originpeer' missing on the payload",
            arguments = ['originpeer']
            ))
        self.assertEqual(r.status_code, 400)

    def test__activateService_get(self):
        values = ns.loads(self.yaml)
        uuid = self.storage.store(values)

        data = ns(uuid=uuid)

        r = self.client.get('/activateService/{}'.format(uuid))

        self.assertEqual(ns.loads(r.data), values)
        self.assertEqual(r.status_code, 200)

    def test__activateService_get__notFound(self):
        uuid = '01020304-0506-0708-090a-0b0c0d0e0f10'
        data = ns(uuid=uuid)

        r = self.client.get('/activateService/{}'.format(uuid))

        self.assertEqual(ns.loads(r.data), ns(
            error = 'NoSuchUuid',
            message = "No personal data available for uuid "
                "'01020304-0506-0708-090a-0b0c0d0e0f10'",
            arguments=[uuid],
            ))
        self.assertEqual(r.status_code, 404)



# vim: ts=4 sw=4 et
