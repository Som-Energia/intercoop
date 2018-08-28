#!/usr/bin/env python

from intercoop import apiexample
from intercoop import remoteuserinfo
from intercoop import crypto

import os


try: os.makedirs('instance/somacme/remoteusers')
except: pass


from intercoop.packaging import KeyRingMock as KeyRing


p = apiexample.IntercoopApi(
	'somacme',
	storage = remoteuserinfo.RemoteUserInfo('instance/somacme/remoteusers'),
    keyring = KeyRing(dict(
        somillusio = crypto.loadKey('testkey-public.pem')
        )),
	continuationUrlTmpl = 'http://localhost:5001/continuation/{uuid}'
	)

p.run(
    debug=True,
    host='0.0.0.0',
    port=5001,
    )

