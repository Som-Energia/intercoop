# -*- encoding: utf-8 -*-


from .crypto import *

from yamlns import namespace as ns

protocolVersion = '1.0'

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
    "Error while parsing message as YAML:\n{}"

class BadMessage(MessageError):
    "Malformed message: {}"

class WrongVersion(MessageError):
    "Wrong protocol version, expected {}, received {}"


class Generator(object):
    def __init__(self, ownKeyPair):
        self.key = ownKeyPair

    def produce(self, values):
        payload = ns(values).dump()
        signature = sign(self.key, payload)
        return ns(
            intercoopVersion = protocolVersion,
            payload = encode(payload),
            signature = signature,
            ).dump()

class Parser(object):

    def __init__(self, keyring):
        self.keyring = keyring

    def parse(self, message):
        def packageField(field):
            if field in package:
                return package[field]
            raise BadMessage("missing {}".format(field))

        try:
            package = ns.loads(message)
        except Exception as e:
            raise BadMessage("Bad message YAML format\n{}".format(e))

        version = packageField('intercoopVersion')
        if version != protocolVersion:
            raise WrongVersion(protocolVersion, version)

        valuesYaml = decode(packageField('payload'))
        signature = packageField('signature')

        try:
            values = ns.loads(valuesYaml)
        except Exception as e:
            raise BadFormat(e)

        try:
            peer = values.originpeer
        except AttributeError:
            raise MissingField('originpeer')

        try:
            pubkey = self.keyring.get(peer)
        except KeyError:
            raise BadPeer(peer)

        if not isAuthentic(pubkey, valuesYaml, signature):
            raise BadSignature()

        return values
        
        





# vim: ts=4 sw=4 et
