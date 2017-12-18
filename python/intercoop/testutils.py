# -*- coding: utf-8 -*-

import unittest
from yamlns import namespace as ns

# Readable verbose testcase listing
unittest.TestCase.__str__ = unittest.TestCase.id

def assertNsEqual(self, dict1, dict2):
    def parseIfString(nsOrString):
        if isinstance(nsOrString, dict):
            return nsOrString
        return ns.loads(nsOrString)

    def sorteddict(d):
        if type(d) not in (dict, ns):
            return d
        return ns(sorted(
            (k, sorteddict(v))
            for k,v in d.items()
            ))
    dict1 = sorteddict(parseIfString(dict1))
    dict2 = sorteddict(parseIfString(dict2))

    return self.assertMultiLineEqual(dict1.dump(), dict2.dump())


# vim: ts=4 sw=4 et
