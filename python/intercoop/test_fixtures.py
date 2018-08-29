# -*- encoding: utf-8 -*-
"""
Data for tests and demos
"""


myuseryaml=u"""\
originpeer: somillusio
lang: es
nif: 12345678Z
name: Bunny, Bugs
peerroles:
- member
- worker
innerid: 666
address: Golf Club, 5th hole
city: Murcia
state: Murcia
postalcode: '01022'
country: ES
email:
- bugsbunny@loonietoons.com
phone:
- '555121232'
proxynif:
proxyname:
"""

somacmeyaml=u"""\
intercoopVersion: "1.0"
peerVersion: 1
peerid: somacme
name: Som Acme, SCCL
url:
  es: http://somacme.coop/es
logo: http://www.linpictures.com/images/indevimgs/acme.jpg
privacyPolicyUrl:
  es: http://www.wallpapersonly.net/wallpapers/thats-all-folks-1680x1050.jpg
description:
  es: >
    La cooperativa para atrapar correcaminos
targetUrl: http://localhost:5001
services:
  explosives:
    name:
      es: Comprar explosivos
    description:
      es: >
        Puedes comprar explosivos éticos de la mejor calidad.
  anvil:
    name:
      es: Comprar yunques
    description:
      es: >
        Yunques garantizados, siempre caen en una cabeza
    fields:
    - originpeer
    - innerid
fields:
- originpeer
- nif
"""

sombogusyaml=u"""\
intercoopVersion: "1.0"
peerVersion: 1
peerid: sombogus
name: Som Bogus, SCCL
url:
  es: https://es.sombogus.coop
logo: http://xes.cat/wp-content/uploads/2017/05/logotip-xes.png
privacyPolicyUrl:
    es: http://www.wallpapersonly.net/wallpapers/thats-all-folks-1680x1050.jpg
description:
    es: >
      Productos inútiles pero muy éticos
targetUrl: http://localhost:5002/intercoop
services:
  contract:
    name:
        es: Contrata
    description:
        es: >
          Productos con marcas tipo Panone, Grifons, Pas Natural, Reacciona...
    fields:
    - originpeer
    - name
"""

somillusioyaml = u"""
intercoopVersion: "1.0"
peerVersion: 1
peerid: somillusio
name: Som Il·lusió, SCCL
url: https://es.somil·lusio.coop
logo: http://xes.cat/wp-content/uploads/2017/05/logotip-xes.png
privacyPolicyUrl: http://www.wallpapersonly.net/wallpapers/thats-all-folks-1680x1050.jpg
description:
  es: Coaching para cooperativas
publickey: | # testkey-public.pem
  -----BEGIN PUBLIC KEY-----
  MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6NNjLFEswRPwzTbuD1Oa
  H9eIVR3U/8iBxQR9jgExqCEI/4oBjBk/eZmYOVdygkZgTeU0TxD5NFd5Zd0Cewz3
  kTkUHJ9YLHSb2SClE6pYlocRYlrvPxEa0XIF+ujRcpKUk5UpEcFNzmNS0s7cUpB+
  UufeEUSyiETeMlu0pqhIXQZSQlgxBt3Fb4vUv8E2Jp1jb4b8A7iygN7oPE7800NX
  VqoCLTnoc3IPDTPugoxfH59rY7LZH0yCCFl5gIAmM1J+w6YFdfjSSwZyE4w/0aF8
  Y4CXTEOoo8f0vTnpN96or4ObdI1ZMwU8b7rpxEHmP2exAul9FnoEZytVtteAYpIt
  QwIDAQAB
  -----END PUBLIC KEY-----
"""

def read(filename):
    with open(filename,'rb') as _f:
        return _f.read().decode('utf8')

def mkdir(dirname):
    import os
    try: os.makedirs(dirname)
    except: pass

def write(filename, content):
    import os
    mkdir(os.path.dirname(filename))
    with open(filename,'wb') as f:
        f.write(content.encode('utf8'))

somenergiayaml = read('../peerdescriptor-example-somenergia.yaml')
mesopcionsyaml = read('../peerdescriptor-example-mesopcions.yaml')


# vim: ts=4 sw=4 et
