# -*- encoding: utf-8 -*-

from yamlns import namespace as ns
import os
from .catalog import (
    BadUser,
    BadField,
    )

class UserInfo(object):
    """This mock object returns user info related to provided keys.
    In your system the substitute of this object should use the ERP
    to get such information.
    """

    def __init__(self, datadir):
        self.datadir = datadir

    def _userData(self, user):
        try:
            return ns.load(os.path.join(self.datadir, user+'.yaml'))
        except Exception:
            raise BadUser(user)

    def language(self, user):
        userdata = self._userData(user)
        try:
            return userdata.lang
        except AttributeError:
            return 'es'

    def getFields(self, user, fields):
        userdata = self._userData(user)

        for field in fields:
            if field not in userdata:
                raise BadField(field)

        return ns([
            (key, value)
            for key,value in userdata.items()
            if key in fields
            ])


# vim: ts=4 sw=4 et
