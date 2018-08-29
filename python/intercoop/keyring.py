#!/usr/bin/env python

from intercoop import crypto

class KeyRing(object):

	def __init__(self, peers):
		self._peers = peers

	def get(self, key):
		peerinfo = self._peers.get(key)
		return crypto.loadKeyString(peerinfo.publickey)


# vim: ts=4 sw=4 et
