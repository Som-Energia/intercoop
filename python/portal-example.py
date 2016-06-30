#!/usr/bin/env python

from intercoop import portalexample

from intercoop import portalexample_test

import os

try:
    os.makedirs('instance/peers')
except: pass
with open('instance/peers/sombogus.yaml','wb') as f:
    f.write(portalexample_test.sombogusyaml.encode('utf8'))
with open('instance/peers/somacme.yaml','wb') as f:
    f.write(portalexample_test.somacmeyaml.encode('utf8'))
with open('../peerdescriptor-example.yaml','rb') as some:
    with open('instance/peers/somenergia.yaml','wb') as f:
        f.write(some.read())

p = portalexample.Portal('Som Ilusio', 'instance/peers')

p.run()

