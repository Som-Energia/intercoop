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

def generateKeyPair(filename, publicfilename=None):
    key = _deps.RSA.generate(2048)
    with open(filename,'wb') as f:
        f.write(key.exportKey('PEM'))
    if publicfilename is None: return
    exportPublicKey(key, publicfilename)

def loadKeyPair(filename):
    with open(filename,'rb') as f:
        return _deps.RSA.importKey(f.read())

def exportPublicKey(key, filename):
    public = key.publickey()
    with open(filename,'wb') as f:
        f.write(public.exportKey('PEM'))

def sign(privatekey, payload):
    signer = _deps.PKCS1_v1_5.new(privatekey)
    return bencode(signer.sign(sha(payload)))

def isAuthentic(publickey, payload, signature):
    verifier = _deps.PKCS1_v1_5.new(publickey)
    decodedSignature = bdecode(signature)
    return verifier.verify(sha(payload), decodedSignature)

# vim: ts=4 sw=4 et
