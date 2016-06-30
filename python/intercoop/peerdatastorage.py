# -*- encoding: utf-8 -*-

from yamlns import namespace as ns
import os

class PeerDataStorage(object):
    
    def __init__(self,datadir):
        self.datadir=datadir

    def get(self,peername):
        return ns.load(os.path.join(self.datadir, peername+'.yaml'))


# vim: ts=4 sw=4 et
