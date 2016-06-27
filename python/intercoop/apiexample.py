# -*- encoding: utf-8 -*-


from flask import (
	Flask,
	make_response,
	request,
	)

from . import crypto
from . import packaging
from . import unsecuredatastorage
import os

app = Flask(__name__)

storageFolder='apiexamplestorage'
try:
	os.makedirs(storageFolder)
except: pass
storage = unsecuredatastorage.DataStorage(storageFolder)
keyring = {}
keyfile = 'testkey.pem'
pubfile = 'testkey-public.pem'
if not os.access(keyfile, os.F_OK):
	crypto.generateKey(keyfile, pubfile)
key = crypto.loadKey(keyfile)
public = crypto.loadKey(pubfile)


@app.route('/intercoop/protocolVersion', methods=['GET'])
def protocolVersion_get():
	response = make_response(
		packaging.protocolVersion,
		)
	response.mimetype='application/yaml'
	return response


@app.route('/intercoop/peermember', methods=['POST'])
def peermember_post():
	p = packaging.Parser(keyring)
	values = p.parse(request.data)
	return storage.store(values)




# vim: ts=4 sw=4 et

