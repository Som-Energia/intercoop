# -*- encoding: utf-8 -*-

from . import crypto
from . import apiclient
from . import translation
from . import packaging
from yamlns import namespace as ns


class IntercoopCatalog(object):
    """
    Provides common functionality to navigate peer
    services and activate them for a user.
    """

    def __init__(self, keyfile, peers, users):
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

    def activate(self, peer, service, user):
        """
        Sends to the peer a request to activate the service for the user.
        It returns the continuation url, where the user should be redirected
        in order to complete the service activation.

        IMPORTANT: Calling this function without an explicit consent
        of the user to send the peer the personal information 
        or without acceptance of the peer privacy policy
        should be considered a privacy violation.
        """
        fields = self.requiredFields(peer, service)
        peerData = self.peers.get(peer)
        serviceData = peerData.services[service]
        data = self.users.getFields(user, fields)
        api = apiclient.ApiClient(peerData.targetUrl, self.key)
        return api.activateService(service, data)
        return 'https://somacme.coop/contract?token=01020304-0506-0708-090a-0b0c0d0e0f10'

        # code copied from Portal
        # TODO: Not under test!!
        _ = self._translator()
        peerData = _(self.peers.get(peer))
        # TODO: augment personal data keys with source ones
        # TODO: handle errors
        try:
            continuationUrl = api.activateService(service, data)
        except Exception as e:
            print(type(e).__name__, e) 
            # TODO: Log the error
            return "Error comunicando con la entidad"
        return redirect(continuationUrl, 302)



# vim: ts=4 sw=4 et
