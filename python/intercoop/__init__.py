# -*- encoding: utf-8 -*-


from yamlns import namespace as ns

import base64

# Crypto level

def encode(payload):
    "Encode a unicode string into base64 (as unicode string)"
    return bencode(payload.encode('utf8'))

def decode(encodedPayload):
    "Decode utf8 base64 into unicode string"
    return bdecode(encodedPayload).decode('utf8')

def bencode(binaryPayload):
    "Encode bytes as base64 (as unicode string)"
    return base64.urlsafe_b64encode(binaryPayload).decode('utf8')

def bdecode(b64string):
    "Decode a unicode string representing base64 stream into bytes"
    return base64.urlsafe_b64decode(b64string.encode('utf8'))

def sha(payload):
    "Returns the SHA of an unicode string encoded as utf-8"
    from Crypto.Hash import SHA
    return SHA.new(payload.encode('utf-8'))

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
    signer = PKCS1_v1_5.new(key)
    return bencode(signer.sign(sha(payload)))

def isAuthentic(key, payload, signature):
    from Crypto.Signature import PKCS1_v1_5
 
    decodedSignature = bdecode(signature)
    verifier = PKCS1_v1_5.new(key)
    return verifier.verify(sha(payload), decodedSignature)


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
