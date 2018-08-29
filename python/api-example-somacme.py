#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from intercoop import apiexample
from intercoop import remoteuserinfo
from intercoop import crypto
from intercoop import keyring
from intercoop import peerinfo
from intercoop import portalexample_test

import os

def write(filename, content):
	with open(filename,'wb') as f:
		f.write(content.encode('utf8'))

try: os.makedirs('instance/somacme/peers')
except: pass

with open('../peerdescriptor-example-somenergia.yaml','rb') as some:
	somenergiayaml = some.read().decode('utf8')

with open('../peerdescriptor-example-mesopcions.yaml','rb') as some:
	mesopcionsyaml = some.read().decode('utf8')

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

write('instance/somacme/peers/somillusio.yaml', somillusioyaml)
write('instance/somacme/peers/somenergia.yaml', somenergiayaml)
write('instance/somacme/peers/mesopcions.yaml', mesopcionsyaml)
write('instance/somacme/peers/sombogus.yaml', portalexample_test.sombogusyaml)
write('instance/somacme/peers/somacme.yaml', portalexample_test.somacmeyaml)

try: os.makedirs('instance/somacme/remoteusers')
except: pass

p = apiexample.IntercoopApi(
	'somacme',
	storage = remoteuserinfo.RemoteUserInfo('instance/somacme/remoteusers'),
    keyring = keyring.KeyRing(peers = peerinfo.PeerInfo('instance/somacme/peers')),
	continuationUrlTmpl = 'http://localhost:5001/continuation/{uuid}'
	)

p.run(
    debug=True,
    host='0.0.0.0',
    port=5001,
    )

# vim: ts=4 sw=4 et
