#!/usr/bin/env python
#-*- encoding: utf-8 -*-

from intercoop import apiexample
from intercoop import remoteuserinfo
from intercoop import crypto
from intercoop import keyring
from intercoop import peerinfo
from intercoop import test_fixtures
from intercoop.test_fixtures import write, mkdir

import os

mkdir('instance/somacme/remoteusers')
write('instance/somacme/peers/somillusio.yaml', test_fixtures.somillusioyaml)
write('instance/somacme/peers/somenergia.yaml', test_fixtures.somenergiayaml)
write('instance/somacme/peers/mesopcions.yaml', test_fixtures.mesopcionsyaml)
write('instance/somacme/peers/sombogus.yaml', test_fixtures.sombogusyaml)
write('instance/somacme/peers/somacme.yaml', test_fixtures.somacmeyaml)

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
