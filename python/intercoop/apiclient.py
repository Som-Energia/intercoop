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
        mime = response.headers.get('content_type', None) or 'Unspecified'
        if mime != 'application/yaml':
            raise BackendError("Wrong mime type received: {}".format(mime))
        r = ns.loads(response.text)
        if response.status_code == 200:
            return r.continuationUrl
        print ("API call failed\n{}".format(response.text))
        if 'error' in r and 'arguments' in r:
            raise packaging.error(r.error, *r.arguments)
        raise BackendError(response.text)


# vim: ts=4 sw=4 et
