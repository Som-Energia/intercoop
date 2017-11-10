# -*- encoding: utf-8 -*-

from yamlns import namespace as ns
import requests
from . import packaging

class BackendError(packaging.MessageError):
    "Error comunicating with the other entity\n{}"

class ApiClient(object):

    def __init__(self, apiurl, key):
        self.apiurl = apiurl
        self.key = key

    def activateService(self, service, personalData):
        package = packaging.generate(self.key,personalData)
        response = requests.post(self.apiurl+'/activateService', data=package)
        r = ns.loads(response.text)
        if response.status_code == 200:
            return r.continuationUrl
        print ("API call failed\n{}".format(response.text))
        if 'type' in r and 'arguments' in r:
            raise packaging.error(r.type, *r.arguments)
        raise BackendError(response.text)


# vim: ts=4 sw=4 et
