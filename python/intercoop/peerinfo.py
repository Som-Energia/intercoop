# -*- encoding: utf-8 -*-

from yamlns import namespace as ns
import os
import glob

class PeerInfo(object):
    
    def __init__(self,datadir):
        self.datadir=datadir

    def get(self,peername):
        import re
        if not re.match('^\\w+$', peername):
            raise Exception("Invalid peer '{}'".format(peername))

        filename = os.path.join(self.datadir, peername+'.yaml')
        try:
            return ns.load(filename)
        except IOError:
            raise Exception("Not such peer '{}'".format(peername))

    def __iter__(self):
        wildcard = os.path.join(self.datadir, '*.yaml')
        return (
            ns.load(filename)
            for filename in sorted(glob.glob(wildcard))
        )
            
                     

# vim: ts=4 sw=4 et
