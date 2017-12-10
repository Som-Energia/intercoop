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
        message=format(e),
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
        """
        Registers personal data of a member of a source entity to
        get a given service.
        Return the uuid of the registation, and the url the member
        browser should redirect to fully activate the service.
        Data is signed by the source entity and should conform specs.
        """
        values = packaging.parse(self.keyring, request.data)
        uuid = self.storage.store(values)
        # TODO: Validate fields for the service
        result = ns(uuid=uuid)
        if self.continuationUrlTmpl:
            result.update(
                continuationUrl=self.continuationUrlTmpl.format(uuid=uuid),
            )
        return result

    @route('/activateService/<uuid>', methods=['GET'])
    @yaml_response
    def activateService_get(self, uuid):
        # TODO: Caducar tokens
        values = self.storage.retrieve(uuid)
        return values

    @route('/continuation/<uuid>', methods=['GET'])
    def continuation(self, uuid):
        remoteUser = self.storage.retrieve(uuid)
        return self.fullPage(
            "<h1>Service form</h1>" +
            """<p>This continuation page is part of the api,
            just for demo purposes. The usual scenario is to
            redirect to a form at the destination entity portal,
            to complete the service order.
            Transferred data could be presented for further edition.
            </p>
            """
            "<p>Info retrieved from original entity:</p>"
            "<table>"+ ''.join(
            "<tr><th>{name}</th><td><input value='{value}' /></td></tr>".format(
                name=name,
                value=value,
                )
            for name, value in remoteUser.items()
            ) + "</table>"
        )

    def style(self):
        return ("""\
            body {
                background: #eee;
                padding-top: 2ex;
            }
            .head {
                padding: 1ex 15px;
                background-color: #a11;
                color: white;
                position: fixed;
                right: 0;
                top: 0;
                left: 0;
                text-align: left;
            }

            h1 {
                color: #a11;
            }
        """)

    def fullPage(self, content):
        return (
            "<html><head>"
            "<style>"
            + self.style() +
            "</style>"
            "</head><body>"
            "<div class='head'>{}</div>".format(self.name)
            + content +
            "</body><html>"
        )




if __name__ == '__main__':
    IntercoopApi().run()



# vim: ts=4 sw=4 et
