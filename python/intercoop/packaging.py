# -*- encoding: utf-8 -*-

from .crypto import *
from yamlns import namespace as ns

protocolVersion = u'1.0'

class MessageError(Exception):
    def __init__(self, *args, **kwds):
        super(MessageError,self).__init__(
            self.__doc__.format(*args, **kwds))
        self.arguments=args

class NoSuchUuid(MessageError):
    "No personal data available for uuid '{}'"

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


def error(exceptionType, *args):
    if exceptionType not in globals():
        return Exception(exceptionType, *args)

    ExceptionClass = globals()[exceptionType]

    if type(ExceptionClass) != type:
        return Exception(exceptionType, *args)

    if not issubclass(ExceptionClass, MessageError):
        return Exception(exceptionType, *args)

    return ExceptionClass(*args)


def generate(ownKeyPair, values):
    payload = ns(values).dump()
    signature = sign(ownKeyPair, payload)
    result = ns()
    result.intercoopVersion = protocolVersion
    result.payload = encode(payload)
    result.signature = signature
    return result.dump()

def parse(keyring, message):
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

    payload = packageField('payload')
    signature = packageField('signature')

    try:
        valuesYaml = decode(payload)
    except UnicodeError:
        raise BadMessage("Payload is not base64 coded UTF8")
    except Exception as e:
        raise BadMessage(
            "Payload is invalid Base64: {}".format(e))

    try:
        values = ns.loads(valuesYaml)
    except Exception as e:
        raise BadFormat(e)

    try:
        peer = values.originpeer
    except AttributeError:
        raise MissingField('originpeer')

    try:
        pubkey = keyring.get(peer)
    except KeyError:
        raise BadPeer(peer)

    if not isAuthentic(pubkey, valuesYaml, signature):
        raise BadSignature()

    return values

 

class Generator(object):
    "deprecated"

    def __init__(self, ownKeyPair):
        self.key = ownKeyPair

    def produce(self, values):
        return generate(self.key, values)

class Parser(object):
    "deprecated"

    def __init__(self, keyring):
        self.keyring = keyring

    def parse(self, message):
        return parse(self.keyring, message)





# vim: ts=4 sw=4 et

