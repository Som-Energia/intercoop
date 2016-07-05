#!/usr/bin/env python

from intercoop import apiexample
from intercoop import remoteuserinfo
from intercoop import crypto

import os


try: os.makedirs('instance/somacme/peeruserdata')
except: pass


from intercoop.apiexample_test import KeyRingMock as KeyRing

keyring = KeyRing(dict(
	somillusio = crypto.loadKey('testkey-public.pem')
	))

p = apiexample.IntercoopApi(
	'intercoop',
	remoteuserinfo.DataStorage('instance/somacme/peeruserdata'),
	keyring,
	'http://localhost:5001/activateService/{uuid}'
	)

p.run(
    debug=True,
    host='0.0.0.0',
    port=5001,
    )

