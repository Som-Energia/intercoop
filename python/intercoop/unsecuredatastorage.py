# -*- encoding: utf-8 -*-

from yamlns import namespace as ns
import os
from . import crypto

class DataStorage(object):
    """
    DO NOT USE THIS IN PRODUCTION.
    This class is a simple testing purpose data storage.
    Since it would contain personal data, do not use
    this in production deployments.
    """
    def __init__(self, folder):
        self.folder = folder
        if not os.path.exists(folder):
            raise Exception("Storage folder '{}' should exist"
                .format(folder))

    def store(self, **kwds):
        uuid = crypto.uuid()
        filename = os.path.join(self.folder, uuid+'.yaml')
        content = ns(kwds).dump()
        # use dump with filename when yamlns fixes Py2 issues
        with open(filename, 'wb') as f:
            f.write(content.encode('utf-8'))
        return uuid


# vim: ts=4 sw=4 et
