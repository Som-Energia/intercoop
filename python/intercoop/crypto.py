# -*- encoding: utf-8 -*-

"""
Simple interface to common cryptographic actions.
"""

class _deps:
    "Hides dependencies on external modules"
    import uuid
    import base64
    from Crypto.Hash import SHA
    from Crypto.PublicKey import RSA
    from Crypto.Signature import PKCS1_v1_5

def uuid():
    """Generates an unique identifier in uuid4 format"""
    return str(_deps.uuid.uuid4())

def encode(text):
    "Encode text into base64 (as text)"
    if (hasattr(text, 'encode')):
        text = text.encode('utf8')
    else:
        text.decode('utf8') # just check
    return bencode(text)

def decode(b64string):
    "Decode base64 (as text) back into text"
    return bdecode(b64string).decode('utf8')

def bencode(binaryStream):
    "Encode bytes (binary) as base64 (as text)"
    return _deps.base64.urlsafe_b64encode(binaryStream).decode('utf8')

def bdecode(b64string):
    "Decode base64 (as text) back into bytes (binary)"
    return _deps.base64.urlsafe_b64decode(b64string.encode('utf8'))

def sha(text):
    "Returns the SHA of a text"
    return _deps.SHA.new(text.encode('utf-8'))

def generateKey(filename=None, publicfilename=None):
    """
    Generates a public/private key pair.
    Besides returning the key pair,
    if a filename is provided the key pair is stored in PEM format.
    If publicfilename is provided then an additional file will be generade with just the public key.

    WARNING: Exported key pairs are stored unencrypted, and
    they contain the private key which is sensible.
    """
    key = _deps.RSA.generate(2048)
    if filename:
        exportKey(key, filename, publicfilename)
    return key

def exportKey(key, filename, publicfilename=None):
    """
    Stores a key into a file in PEM format.
    If publicfilename is provided then an additional file will be generade with just the public key.

    WARNING: Exported key pairs are stored unencrypted, and
    they contain the private key which is sensible.
    """
    with open(filename,'wb') as f:
        f.write(key.exportKey('PEM'))
    if publicfilename is not None:
        exportPublicKey(key, publicfilename)

def exportPublicKey(key, filename):
    """
    Stores the public key of a key pair in PEM format.
    """
    public = key.publickey()
    with open(filename,'wb') as f:
        f.write(public.exportKey('PEM'))

def exportString(key):
    return u'{}'.format(key.exportKey('PEM'))

def loadKey(filename):
    """
    Loads stored key or key pair in PEM format.
    """
    with open(filename,'rb') as f:
        return loadKeyString(f.read())

def loadKeyString(string):
    """
    Load a string containing a PEM key or keypair.
    """
    return _deps.RSA.importKey(string)

def sign(privatekey, text):
    """
    Generates the signature of the text by using the privatekey.
    """
    signer = _deps.PKCS1_v1_5.new(privatekey)
    return bencode(signer.sign(sha(text)))

def isAuthentic(publickey, text, signature):
    """
    Returns true if the signature was generated for the text
    and the private signature paired with the provided public one.
    """
    verifier = _deps.PKCS1_v1_5.new(publickey)
    decodedSignature = bdecode(signature)
    return verifier.verify(sha(text), decodedSignature)


# vim: ts=4 sw=4 et
