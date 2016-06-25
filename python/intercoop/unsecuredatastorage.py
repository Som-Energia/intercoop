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

    def _tokenfile(self, token):
        import re
        if not re.match(
            '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
            token,
            ):
            raise Exception("Bad token '{}'".format(token))
        return os.path.join(self.folder, token+'.yaml')

    def store(self, data=None, **kwds):
        token = crypto.uuid()
        filename = self._tokenfile(token)
        content = ns(data or kwds).dump()
        # TODO: use dump with filename when yamlns fixes Py2 issues
        with open(filename, 'wb') as f:
            f.write(content.encode('utf-8'))
        return token

    def retrieve(self, token):
        filename = self._tokenfile(token)
        return ns.load(filename)


# vim: ts=4 sw=4 et
