# -*- encoding: utf-8 -*-

from yamlns import namespace as ns
import os

class PeerDataStorage(object):
    
    def __init__(self,datadir):
        self.datadir=datadir

    def get(self,peername):
        filename = os.path.join(self.datadir, peername+'.yaml')
        try:
            return ns.load(filename)
        except IOError:
            raise Exception("Not such peer '{}'".format(peername))

    def __iter__(self):
        return (
            ns.load(os.path.join(self.datadir, i))
            for i in os.listdir(self.datadir) 
            if i.endswith(".yaml")
        )
            
                     

# vim: ts=4 sw=4 et
