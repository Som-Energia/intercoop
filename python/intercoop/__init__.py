# -*- encoding: utf-8 -*-


from .crypto import *

from yamlns import namespace as ns

class MessageError(Exception):
    def __init__(self, *args, **kwds):
        super(MessageError,self).__init__(
            self.__doc__.format(*args, **kwds))

class MissingField(MessageError):
    "Required field '{}' missing on the payload"

class BadPeer(MessageError):
    "The entity '{}' is not a recognized one"

class BadSignature(MessageError):
    "Signature verification failed, untrusted content"

class BadFormat(MessageError):
    "Error while parsing message as YAML: {}"



class Generator(object):
    def __init__(self, ownKeyPair):
        self.key = ownKeyPair

    def produce(self, values):
        payload = ns(values).dump()
        signature = sign(self.key, payload)
        return ns(
            intercoopVersion = '1.0',
            payload = encode(payload),
            signature = signature,
            ).dump()

class Parser(object):

    # TODO: This should be a dict of public keys for peers
    def __init__(self, keyring):
        self.keyring = keyring

    def parse(self, message):
        package = ns.loads(message)
        valuesYaml = decode(package.payload)
        values = ns.loads(valuesYaml)
        # TODO: Choose key depending on originpeer
        if not isAuthentic(self.keyring.get('testpeer'), valuesYaml, package.signature):
            raise BadSignature()
        return values
        
        





# vim: ts=4 sw=4 et
