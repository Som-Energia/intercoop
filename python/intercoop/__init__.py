# -*- encoding: utf-8 -*-


from .crypto import *

from yamlns import namespace as ns

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

class BadSignature(Exception): pass

class Parser(object):

    # TODO: This should be a dict of public keys for peers
    def __init__(self, ownKeyPair):
        self.key = ownKeyPair

    def parse(self, message):
        package = ns.loads(message)
        valuesYaml = decode(package.payload)
        values = ns.loads(valuesYaml)
        # TODO: Choose key depending on originpeer
        if not isAuthentic(self.key, valuesYaml, package.signature):
            raise BadSignature("Signature didn't match the content, content modified")
        return values
        
        





# vim: ts=4 sw=4 et
