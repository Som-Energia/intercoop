# -*- encoding: utf-8 -*-

import unittest
from . import apiclient
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
        self.continuationUrl = 'https://somacme.coop/contract?token={}'
        self.uuid = '01020304-0506-0708-090a-0b0c0d0e0f10'


    def test_getProtocolVersion(self):

        continuationUrl = "https://somacme.coop/contract?01020304-0506-0708-090a-0b0c0d0e0f10"
        client = apiclient.ApiClient(
            apiurl=self.apiurl,
            key=self.key,
        )
        with requests_mock.mock() as m:
            m.get('http://test.com', text='data')
            url=client.activateService(
                service='contract', 
                personalData=self.personalData,
                )
        self.assertEqual(url,self.continuationUrl.format(self.uuid))
                



# vim: ts=4 sw=4 et
