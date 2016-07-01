# -*- encoding: utf-8 -*-

from yamlns import namespace as ns
import os

class UserInfo(object):
	"""This mock object returns user info related to provided keys.
	In your system the substitute of this object should use the ERP
	to get such information.
	"""

	def __init__(self, datadir):
		self.datadir = datadir

	def getFields(self, user, fields):
		return ns.load(os.path.join(self.datadir, user+'.yaml'))



# vim: ts=4 sw=4 et
