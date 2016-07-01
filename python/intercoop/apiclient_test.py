# -*- encoding: utf-8 -*-

import unittest
from . import apiclient
from . import packaging
from . import crypto
import requests_mock
from yamlns import namespace as ns

class ApiClient_Test(unittest.TestCase):

    yaml=u"""\
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


    def respondToPost(self, status, text=None):
        text = text or ns(
            continuationUrl = self.continuationUrl
            ).dump()
        m = requests_mock.mock()
        m.post(
            self.apiurl+'/activateService',
            text = text,
            status_code = status,
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

                u"signature: Deo3k7Y9hH9yd3rEmVtLzIMe1ZiqdXGI57FzwVAM4oPDYXHouZS0cAv3f4rqvZ3YDeayoGwFEe8Bh3lr0Z2BSTcsfRLJXXSWDUcJASkxCapXPMF-63_cNXJ5EGyxeFIDlqtXCWGEXUiJgY8n3zh4bgna-QJLVUXAcKQiRVgzlmVS2JnluTp3GjV5g8H5QBIp5TLSfWKkX_wpH7Mmq_Kslo-i3MJoIMnkw_Mi7sKn4kP_GFfpm0RGILTFhYxCL4WkgYqjHW8e8zhu8zBxEhcu4_oQvhLlAsL2l_OUKbZPArdsUm1gZEBVq-bVsGyZDo06pfWI4LUHfCVAGGkXrD6QiQ==\n"
                u"payload: b3JpZ2luY29kZTogNjY2Cm5hbWU6IFBlcmljbyBkZSBsb3MgUGFsb3RlcwphZGRyZXNzOiBQZXJjZWJlLCAxMwpjaXR5OiBWaWxsYXJyaWJhIGRlbCBBbGNvcm5vcXVlCnN0YXRlOiBBbGJhY2V0ZQpwb3N0YWxjb2RlOiAnMDEwMDEnCmNvdW50cnk6IEVTCg==\n"
                u"intercoopVersion: '1.0'\n"
                )
            ])


    def test_activateService_receivesUrl(self):
        error = ns()
        error.type='BadPeer'
        error.message="The entity 'badpeer' is not a recognized one"
        error.arguments=['badpeer']

        with self.respondToPost(403,error.dump()) as m:
            with self.assertRaises(packaging.BadPeer) as ctx:
                url=self.client.activateService(
                    service=self.service,
                    personalData=self.personalData,
                    )

        self.assertEqual(str(ctx.exception),
            "The entity 'badpeer' is not a recognized one",
            )





# vim: ts=4 sw=4 et
