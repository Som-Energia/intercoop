# -*- encoding: utf-8 -*-

import unittest
from . import apiclient
from . import packaging
from . import crypto
import requests_mock
from yamlns import namespace as ns

class ApiClient_Test(unittest.TestCase):

    yaml=u"""\
        originpeer: somillusio
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
        self.key = crypto.loadKey(self.keyfile)
        self.personalData = ns.loads(self.yaml)
        self.apiurl = "https://api.somacme.coop/intercoop"
        self.service = "contract"
        self.uuid = '01020304-0506-0708-090a-0b0c0d0e0f10'
        self.continuationUrl = 'https://somacme.coop/contract?token={}'.format(
            self.uuid)

        self.client = apiclient.ApiClient(
            apiurl=self.apiurl,
            key=self.key,
        )

    def respondToPost(self, status, text=None, mimetype='application/yaml'):
        text = text or ns(
            continuationUrl = self.continuationUrl
            ).dump()
        m = requests_mock.mock()
        m.post(
            self.apiurl+'/activateService',
            status_code = status,
            text = text,
            headers = {'content-type': mimetype},
            )
        return m

    def test_activateService_receivesUrl(self):
        with self.respondToPost(200) as m:
            url=self.client.activateService(
                service=self.service,
                personalData=self.personalData,
                )
        self.assertEqual(url,self.continuationUrl)

    def test_activateService_sendsPackage(self):

        with self.respondToPost(200) as m:
            url=self.client.activateService(
                service=self.service,
                personalData=self.personalData,
                )

        self.assertEqual([
            (h.method, h.url, h.text)
            for h in m.request_history], [
            ('POST', 'https://api.somacme.coop/intercoop/activateService',

                u"intercoopVersion: '1.0'\n"
                u"payload: b3JpZ2lucGVlcjogc29taWxsdXNpbwpvcmlnaW5jb2RlOiA2NjYKbmFtZTogUGVyaWNvIGRlIGxvcyBQYWxvdGVzCmFkZHJlc3M6IFBlcmNlYmUsIDEzCmNpdHk6IFZpbGxhcnJpYmEgZGVsIEFsY29ybm9xdWUKc3RhdGU6IEFsYmFjZXRlCnBvc3RhbGNvZGU6ICcwMTAwMScKY291bnRyeTogRVMK\n"
                u"signature: 2PXEJSmGwaIZY4XgWZYcmh8qexmGe-Ve7p45kLmtia5wO4CXrbx3BiCeFMvbi9eiGazOg-Cy9ktdR3SEYuZlwlkPpQ-C2QrVY2c6o1PKNNLFJoJIYkfnIDwTdtlY5qsxbC-kKbWO2WtnhCeBnBNKOwz9-lbIlrLYo470MjuTLheVmoXuyTHp1hOjHDDn2e38kJT-miNtr4knDn-uMYCXdAx3eIGTBOTQ8wGFz55JR_jluZKIN8wEgJQWAHVMY1FbtsutESRqJ_TMLbCbqe0llxWppxgF20XyzleSxTV6v_I2GZyfEWlYlFnOkk5TEjqkk5vZOFGXra2J3Cabzn9QFQ==\n"
                )
            ])

    def test_activateService_nonYamlResponseMime(self):
        with self.respondToPost(200, text='lala', mimetype='text/html') as m:
            with self.assertRaises(apiclient.BackendError) as ctx:
                self.client.activateService(
                    service=self.service,
                    personalData=self.personalData,
                    )
            self.assertEqual(format(ctx.exception.arguments[0]),
                "Wrong mime type received: text/html")

    def test_activateService_badYaml(self):
        with self.respondToPost(200, text='\tlala', mimetype='application/yaml') as m:
            with self.assertRaises(apiclient.BackendError) as ctx:
                self.client.activateService(
                    service=self.service,
                    personalData=self.personalData,
                    )
            self.assertIn(
                "Bad yaml response",
                format(ctx.exception.arguments[0]))

    def test_activateService_notADict(self):
        with self.respondToPost(200, text='lala', mimetype='application/yaml') as m:
            with self.assertRaises(apiclient.BackendError) as ctx:
                self.client.activateService(
                    service=self.service,
                    personalData=self.personalData,
                    )
            self.assertEqual(format(ctx.exception.arguments[0]),
                "Wrong content format")

    def test_activateService_noContinuationUrl(self):
        with self.respondToPost(200, text='{}', mimetype='application/yaml') as m:
            with self.assertRaises(apiclient.BackendError) as ctx:
                self.client.activateService(
                    service=self.service,
                    personalData=self.personalData,
                    )
            self.assertEqual(format(ctx.exception.arguments[0]),
                "Wrong content format")

    def test_activateService_missingField(self):
        error = ns(
            error = 'MissingField',
            message = "Required field 'originpeer' missing on the payload",
            arguments = ['originpeer']
        )

        data = ns(self.personalData)
        del data.originpeer

        with self.respondToPost(403,error.dump()) as m:
            with self.assertRaises(packaging.MissingField) as ctx:
                url=self.client.activateService(
                    service=self.service,
                    personalData=self.personalData,
                    )

        self.assertEqual(format(ctx.exception),
            "Required field 'originpeer' missing on the payload",
            )





# vim: ts=4 sw=4 et
