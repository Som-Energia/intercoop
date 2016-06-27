# -*- encoding: utf-8 -*-


from flask import (
	make_response,
	request,
	)

from . import packaging
from .perfume import Perfume, route
from yamlns import namespace as ns
from functools import wraps


def yaml_response(f):
    def handle(e, status_code):
        response = make_response(ns(
            error=type(e).__name__,
            message=str(e),
            ).dump())
        response.mimetype='application/yaml'
        response.status_code = status_code
        return response
        

    @wraps(f)
    def wrapper(*args, **kwd):
        try:
            result = f(*args, **kwd)
        except (
                packaging.BadPeer,
                packaging.BadSignature,
                ) as e:
            return handle(e, 403) # Unauthorized
        except packaging.MessageError as e:
            return handle(e, 400) # Bad request
        response = make_response(ns(result).dump())
        response.mimetype='application/yaml'
        return response
    return wrapper


class IntercoopApi(Perfume):

    def __init__(self, name, storage, keyring):
        super(IntercoopApi, self).__init__(name)
        self.storage = storage
        self.keyring = keyring


    @route('/protocolVersion', methods=['GET'])
    @yaml_response
    def protocolVersion(self):
        return ns(
            protocolVersion = packaging.protocolVersion
            )

    @route('/peermember', methods=['POST'])
    @yaml_response
    def peermember_post(self):
        """Registers personal data of a member of a source entity to get a given service.
        Return the uuid of the registation, and the url the member
        browser should redirect to fully activate the service.
        Data is signed by the source entity and should conform specs.
        """
        p = packaging.Parser(self.keyring)
        values = p.parse(request.data)
        uuid = self.storage.store(values)
        return ns(
            uuid=uuid,
            )

if __name__ == '__main__':
    IntercoopApi().run()



# vim: ts=4 sw=4 et
