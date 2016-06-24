# -*- encoding: utf-8 -*-



def encode(payload):
    "Encode a unicode string into base64 (as unicode string)"
    return bencode(payload.encode('utf8'))

def decode(encodedPayload):
    "Decode utf8 base64 into unicode string"
    return bdecode(encodedPayload).decode('utf8')

def bencode(binaryPayload):
    "Encode bytes as base64 (as unicode string)"
    import base64
    return base64.urlsafe_b64encode(binaryPayload).decode('utf8')

def bdecode(b64string):
    "Decode a unicode string representing base64 stream into bytes"
    import base64
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

