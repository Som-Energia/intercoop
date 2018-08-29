# -*- encoding: utf-8 -*-

from yamlns import namespace as ns
import requests
from . import packaging

class BackendError(packaging.MessageError):
    "Error comunicating with the other entity\n{}"

class ApiClient(object):
    """Proxies the web API of a remote service provider"""

    def __init__(self, apiurl, key):
        self.apiurl = apiurl
        self.key = key

    def activateService(self, service, personalData):
        package = packaging.generate(self.key,personalData)
        response = requests.post(self.apiurl+'/activateService', data=package)

        mime = response.headers.get('content-type', None) or 'Unspecified'
        if mime != 'application/yaml':
            raise BackendError("Wrong mime type received: {}".format(mime))

        try:
            r = ns.loads(response.text)
        except Exception as e:
            raise BackendError("Bad yaml response\n{}".format(e))

        if type(r) != ns:
            raise BackendError("Wrong content format")

        if response.status_code == 200:
            try:
                return r.continuationUrl
            except AttributeError:
                raise BackendError("Wrong content format")
                
        print ("API call failed\n{}".format(response.text))
        if 'error' in r and 'arguments' in r:
            raise packaging.error(r.error, *r.arguments)
        raise BackendError(response.text)


# vim: ts=4 sw=4 et
