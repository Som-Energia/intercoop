# -*- encoding: utf-8 -*-

from yamlns import namespace as ns
import os

"""
# TODO:

- [ ] process differently unsupported and not pressent fields
"""

class BadUser(Exception):
    def __init__(self, user):
        super(BadUser, self).__init__(
            "User not found '{}'".format(user))

class BadField(Exception):
    def __init__(self, field):
        super(BadField, self).__init__(
            "Unrecognized user field '{}'".format(field))

class UserInfo(object):
    """This mock object returns user info related to provided keys.
    In your system the substitute of this object should use the ERP
    to get such information.
    """

    def __init__(self, datadir):
        self.datadir = datadir

    def getFields(self, user, fields):
        try:
            userdata = ns.load(os.path.join(self.datadir, user+'.yaml'))
        except Exception:
            raise BadUser(user)

        for field in fields:
            if field not in userdata:
                raise BadField(field)

        return ns([
            (key, value)
            for key,value in userdata.iteritems()
            if key in fields
            ])



# vim: ts=4 sw=4 et
