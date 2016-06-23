# -*- encoding: utf-8 -*-


from yamlns import namespace as ns

import base64

# Crypto level

def encode(payload):
    return base64.b64encode(payload)

def decode(encodedPayload):
    return base64.b64decode(encodedPayload)

def generateKeyPair(filename):
    from Crypto.PublicKey import RSA
    key = RSA.generate(2048)
    with open(filename,'w') as f:
        f.write(key.exportKey('PEM'))

def loadKeyPair(filename):
    from Crypto.PublicKey import RSA
    with open(filename,'r') as f:
        return RSA.importKey(f.read())

def sign(key, payload):
    from Crypto.Signature import PKCS1_v1_5
    from Crypto.Hash import SHA
 
    h = SHA.new(payload)
    signer = PKCS1_v1_5.new(key)
    return encode(signer.sign(h))

def isAuthentic(key, payload, signature):
    from Crypto.Signature import PKCS1_v1_5
    from Crypto.Hash import SHA
 
    decodedSignature = decode(signature)
    h = SHA.new(payload)
    verifier = PKCS1_v1_5.new(key)
    return verifier.verify(h, decodedSignature)


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
        package = ns.loads(unicode(message))
        valuesYaml = decode(package.payload)
        values = ns.loads(unicode(valuesYaml))
        # TODO: Choose key depending on originpeer
        if not isAuthentic(self.key, valuesYaml, package.signature):
            raise BadSignature("Signature didn't match the content, content modified")
        return values
        
        





# vim: ts=4 sw=4 et
