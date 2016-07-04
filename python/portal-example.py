#!/usr/bin/env python

from intercoop import portalexample

from intercoop import portalexample_test

import os

def write(filename, content):
	with open(filename,'wb') as f:
		f.write(content.encode('utf8'))

try: os.makedirs('instance/users')
except: pass

try: os.makedirs('instance/peers')
except: pass

with open('../peerdescriptor-example.yaml','rb') as some:
	somenergiayaml = some.read().decode('utf8')

write('instance/peers/somenergia.yaml', somenergiayaml)
write('instance/peers/sombogus.yaml', portalexample_test.sombogusyaml)
write('instance/peers/somacme.yaml', portalexample_test.somacmeyaml)
write('instance/users/myuser.yaml', portalexample_test.myuseryaml)


p = portalexample.Portal(
	'intercoop',
	peerid='somillusio',
	keyfile='testkey.pem',
	peerdatadir='instance/peers',
	userdatadir='instance/users',
	)

p.run(debug=True)

