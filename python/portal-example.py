#!/usr/bin/env python

from intercoop import portalexample
from intercoop import portalexample_test
from intercoop import peerinfo
from intercoop import userinfo

import os

def write(filename, content):
	with open(filename,'wb') as f:
		f.write(content.encode('utf8'))

try: os.makedirs('instance/somillusio/users')
except: pass

try: os.makedirs('instance/somillusio/peers')
except: pass

with open('../peerdescriptor-example.yaml','rb') as some:
	somenergiayaml = some.read().decode('utf8')

write('instance/somillusio/peers/somenergia.yaml', somenergiayaml)
write('instance/somillusio/peers/sombogus.yaml', portalexample_test.sombogusyaml)
write('instance/somillusio/peers/somacme.yaml', portalexample_test.somacmeyaml)
write('instance/somillusio/users/_labels.yaml', portalexample_test.labelsyaml)
write('instance/somillusio/users/myuser.yaml', portalexample_test.myuseryaml)


p = portalexample.Portal(
	'intercoop',
	peerid='somillusio',
	keyfile='testkey.pem',
    peers = peerinfo.PeerInfo(
	    'instance/somillusio/peers'),
    users = userinfo.UserInfo(
        'instance/somillusio/users'),
	)

p.run(
    debug=True,
    host='0.0.0.0',
    )

