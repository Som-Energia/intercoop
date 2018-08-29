# -*- encoding: utf-8 -*-

from . import crypto
from . import apiclient
from . import translation
from . import packaging
from yamlns import namespace as ns

class BadUser(Exception):
    def __init__(self, user):
        super(BadUser, self).__init__(
            "User not found '{}'".format(user))

class BadField(Exception):
    def __init__(self, field):
        super(BadField, self).__init__(
            "Unrecognized user field '{}'".format(field))

labelsyaml=u"""\
originpeer:
    es: Entidad de procedencia
    ca: Entitat de provinença
    en: Source entity
lang:
    es: Idioma preferente
    ca: Idioma preferent
    en: Preferred language
nif:
    es: NIF
    ca: NIF
    en: NIF
name:
    es: Nombre
    ca: Nom
    en: Name
peerroles:
    es: Roles
    ca: Rols
    en: Roles
innerid:
    es: Número de socio/a
    ca: Número de soci/a
    en: Member number
address:
    es: Dirección
    ca: Adreça
    en: Address
city:
    es: Municipio
    ca: Municipi
    en: City
state:
    es: Província
    ca: Provincia
    en: State
postalcode:
    es: Código postal
    ca: Codi postal
    en: Postal code
country:
    es: Nacionalidad
    ca: Nacionalitat
    en: Country
email:
    es: Correo electrónico
    ca: Correu electrònic
    en: e-mail
phone:
    es: Teléfono
    ca: Telèfon
    en: Phone
proxynif:
    es: NIF del representante
    ca: NIF del representant
    en: Proxy NIF
proxyname:
    es: Nombre del representante
    ca: Nom del representant
    en: Proxy name
"""


class IntercoopCatalog(object):
    """
    Provides common functionality to navigate peer
    services and activate them for a user.

    The constructor receives the following objects
    you may want to implement your own custom implementation.
    """

    def __init__(self, keyfile, peers, users):
        """
        - keyfile: file path to private key file in pem format
        - peers: an object following the PeerInfo interface
        - users: an object following the UserInfo interface

        Library just provides Implementation
        """
        self.peers = peers
        self.users = users
        self.key = crypto.loadKey(keyfile)

    def requiredFields(self, peer, service):
        """
        Returns the keys of the required fields to transfer
        the peer to activate the service
        """
        peerData = self.peers.get(peer)
        if service not in peerData.services:
            raise Exception("Not such service '{service}' in peer '{peer}'"
                .format(service=service, peer=peer))
        serviceData = peerData.services[service]

        if 'fields' in serviceData:
            return list(serviceData.fields)

        if 'fields' in peerData:
            return list(peerData.fields)

        raise Exception("Peer '{}' does not specify fields for service '{}'"
            .format(peer, service))

    def fieldValues(self, user, fields):
        return self.users.getFields(user, fields)

    def fieldLabels(self, fields, lang=None):
        if lang:
            _ = translation.Translator(lang)
            return _(self.fieldLabels(fields))

        labels = ns.loads(labelsyaml)

        for field in fields:
            if field not in labels:
                raise BadField(field)

        return ns([
            (key, value)
            for key,value in labels.items()
            if key in fields
            ])

        return self.users.fieldLabels(fields)

    def peerInfo(self, peer, lang=None):
        if lang:
            _ = translation.Translator(lang)
            return _(self.peerInfo(peer))
        return self.peers.get(peer)

    def __iter__(self):
        return self.peers.__iter__()

    def activate(self, peer, service, user):
        """
        Sends to the peer a request to activate the service for the user.
        It returns the continuation url, where the user should be redirected
        in order to complete the service activation.

        IMPORTANT: Calling this function requires an explicit consent
        of the user to send the peer the personal information 
        or without acceptance of the peer privacy policy
        or it would be a privacy violation.
        """
        fields = self.requiredFields(peer, service)
        peerData = self.peers.get(peer)
        serviceData = peerData.services[service]
        data = self.users.getFields(user, fields)
        api = apiclient.ApiClient(peerData.targetUrl, self.key)
        continuationUrl = api.activateService(service, data)
        return continuationUrl



# vim: ts=4 sw=4 et
