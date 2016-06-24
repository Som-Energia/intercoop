# -*- encoding: utf-8 -*-

class _deps:
    "Hides dependencies on external modules"
    import base64
    from Crypto.Hash import SHA
    from Crypto.PublicKey import RSA
    from Crypto.Signature import PKCS1_v1_5

def encode(payload):
    "Encode a unicode string into base64 (as unicode string)"
    return bencode(payload.encode('utf8'))

def decode(encodedPayload):
    "Decode utf8 base64 into unicode string"
    return bdecode(encodedPayload).decode('utf8')

def bencode(binaryPayload):
    "Encode bytes as base64 (as unicode string)"
    return _deps.base64.urlsafe_b64encode(binaryPayload).decode('utf8')

def bdecode(b64string):
    "Decode a unicode string representing base64 stream into bytes"
    return _deps.base64.urlsafe_b64decode(b64string.encode('utf8'))

def sha(payload):
    "Returns the SHA of an unicode string encoded as utf-8"
    return _deps.SHA.new(payload.encode('utf-8'))

def generateKeyPair(filename):
    key = _deps.RSA.generate(2048)
    with open(filename,'w') as f:
        f.write(key.exportKey('PEM'))

def loadKeyPair(filename):
    with open(filename,'r') as f:
        return _deps.RSA.importKey(f.read())

def sign(privatekey, payload):
    signer = _deps.PKCS1_v1_5.new(privatekey)
    return bencode(signer.sign(sha(payload)))

def isAuthentic(publickey, payload, signature):
    decodedSignature = bdecode(signature)
    verifier = _deps.PKCS1_v1_5.new(publickey)
    return verifier.verify(sha(payload), decodedSignature)

