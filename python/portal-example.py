#!/usr/bin/env python

from intercoop import portalexample

from intercoop import portalexample_test

import os

try: os.makedirs('instance/peers')
except: pass
try: os.makedirs('instance/users')
except: pass
with open('instance/peers/sombogus.yaml','wb') as f:
    f.write(portalexample_test.sombogusyaml.encode('utf8'))
with open('instance/peers/somacme.yaml','wb') as f:
    f.write(portalexample_test.somacmeyaml.encode('utf8'))
with open('../peerdescriptor-example.yaml','rb') as some:
    with open('instance/peers/somenergia.yaml','wb') as f:
        f.write(some.read())
with open('instance/users/myuser.yaml','wb') as f:
	f.write(portalexample_test.myuseryaml.encode('utf8'))

p = portalexample.Portal(
	'Som Ilusio',
	keyfile='testkey.pem',
	peerdatadir='instance/peers',
	userdatadir='instance/users',
	)

p.run(debug=True)

