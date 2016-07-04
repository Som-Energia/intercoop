#!/usr/bin/env python

from intercoop import apiexample
from intercoop import unsecuredatastorage
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
	unsecuredatastorage.DataStorage('instance/somacme/peeruserdata'),
	keyring,
	)

p.run(debug=True, port=5001)

