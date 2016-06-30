#!/usr/bin/env python

from intercoop import portal

from intercoop import portal_test

import os

try:
    os.makedirs('instance/peers')
except: pass
with open('instance/peers/sombogus.yaml','wb') as f:
    f.write(portal_test.sombogusyaml.encode('utf8'))
with open('instance/peers/somacme.yaml','wb') as f:
    f.write(portal_test.somacmeyaml.encode('utf8'))
with open('../peerdescriptor-example.yaml','rb') as some:
    with open('instance/peers/somenergia.yaml','wb') as f:
        f.write(some.read())

p = portal.Portal('Som Ilusio', 'instance/peers')

p.run()

