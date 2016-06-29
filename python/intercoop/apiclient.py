# -*- encoding: utf-8 -*-
from yamlns import namespace as ns
import requests
from . import packaging

class ApiClient(object):

    def __init__(self, apiurl, key):
        self.apiurl = apiurl
        self.key = key

    def activateService(self, service, personalData):
        package = packaging.Generator(self.key).produce(personalData)
        response = requests.post(self.apiurl+"/"+service+'/activateService', data=package)
        r = ns.loads(response.text)
        return r.continuationUrl


# vim: ts=4 sw=4 et
