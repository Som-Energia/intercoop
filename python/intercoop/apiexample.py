# -*- encoding: utf-8 -*-


from flask import (
	make_response,
	request,
    Response,
	)

from . import packaging
from .perfume import Perfume, route
from yamlns import namespace as ns
from functools import wraps


def handle(e, status_code):
    response = make_response(ns(
        error=type(e).__name__,
        message=str(e),
        arguments=e.arguments if hasattr(e,'arguments') else []
        ).dump())
    response.mimetype='application/yaml'
    response.status_code = status_code
    return response
        

def yaml_response(f):
    @wraps(f)
    def wrapper(*args, **kwd):
        try:
            result = f(*args, **kwd)
        except packaging.BadPeer as e:
            return handle(e, 403) # Unauthorized

        except packaging.BadSignature as e:
            return handle(e, 403) # Unauthorized

        except packaging.NoSuchUuid as e:
            return handle(e, 404) # Not found

        except packaging.MessageError as e:
            return handle(e, 400) # Bad request

        if type(result) is Response:
            return result

        response = make_response(ns(result).dump())
        response.mimetype='application/yaml'
        return response
    return wrapper


class IntercoopApi(Perfume):

    def __init__(self, name, storage, keyring, continuationUrlTmpl=None):
        super(IntercoopApi, self).__init__(name)
        self.name = name
        self.storage = storage
        self.keyring = keyring
        self.continuationUrlTmpl = continuationUrlTmpl


    @route('/protocolVersion', methods=['GET'])
    @yaml_response
    def protocolVersion(self):
        return ns(
            protocolVersion = packaging.protocolVersion
            )

    @route('/activateService', methods=['POST'])
    @yaml_response
    def activateService_post(self):
        """Registers personal data of a member of a source entity to get a given service.
        Return the uuid of the registation, and the url the member
        browser should redirect to fully activate the service.
        Data is signed by the source entity and should conform specs.
        """
        values = packaging.parse(self.keyring, request.data)
        uuid = self.storage.store(values)
        result = ns(uuid=uuid)
        if self.continuationUrlTmpl:
            result.update(
                continuationUrl=self.continuationUrlTmpl.format(uuid=uuid),
            )
        return result

    @route('/activateService/<uuid>', methods=['GET'])
    @yaml_response
    def activateService_get(self, uuid):
        values = self.storage.retrieve(uuid)
        return values

    @route('/continuation/<uuid>', methods=['GET'])
    def continuation(self, uuid):
        return (
            "<h1>Portal de contración de {}</h1>".format(self.name) +
            """<p>For demo purposes. Continuation page should be
            a page at the destination entity portal, not part of the API.
            Usually a form asking for more information that is
            required to proceed with the service.
            Maybe presenting the transfered data for further edition.
            </p>
            """
            "<p>Info retrieved from original entity:</p>"
            "<table>"+ ''.join(
            "<tr><th>{name}</th><td>{value}</td></tr>".format(
                name=name,
                value=value,
                )
            for name, value in self.storage.retrieve(uuid).items()
            ) + "</table>"
        )




if __name__ == '__main__':
    IntercoopApi().run()



# vim: ts=4 sw=4 et
