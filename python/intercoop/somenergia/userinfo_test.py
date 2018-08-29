# -*- encoding: utf-8 -*-
from .userinfo import UserInfo, BadUser, BadField

import unittest
from yamlns import namespace as ns
try: import dbconfig
except ImportError:
    dbconfig =None

@unittest.skipIf(not dbconfig, "This requires erp access")
class UserInfo_Test(unittest.TestCase):
    def setup(self):
        self.personaldata = ns(dbconfig.personaldata)

    from intercoop.testutils import assertNsEqual

    def test_getFields_allFields(self):
        users = UserInfo(dbconfig.erppeek)
        data = users.getFields(self.personaldata.nif)

        self.assertNsEqual(data, """\
            originpeer: somenergia
            innerid: '{nsoci}'
            nif: '{nif}'
            name: "{surname}, {name}"
            email: '{email}'
            phone: '{phone}'
            country: ES
            state: {state_code}
            city: {city_code}
            address: {address}
            postalcode: '{postalcode}'
            peerroles:
            - member
            proxyname: TODO
            proxynif: TODO
            lang: {lang_subcode}
            """.format(
                lang_subcode=self.personaldata.lang[:2],
                **self.personaldata))

    def test_getFields_filtering(self):
        users = UserInfo(dbconfig.erppeek)
        data = users.getFields(self.personaldata.nif, [
            'nif',
            'name',
            ])

        self.assertNsEqual(data, """\
            nif: '{nif}'
            name: "{surname}, {name}"
            """.format(**self.personaldata))

    def test_getFields_nonMember(self):
        users = UserInfo(dbconfig.erppeek)
        data = users.getFields(self.personaldata.nonMemberNif,
            "originpeer innerid nif country "
            "state city postalcode peerroles"
            .split())

        self.assertNsEqual(data, """\
            originpeer: somenergia
            innerid: '---------'
            nif: '{nonMemberNif}'
            country: ES
            state: {state_code}
            city: {city_code}
            postalcode: '{postalcode}'
            peerroles: [] # TODO: should be client?
            """.format(
                lang_subcode=self.personaldata.lang[:2],
                **self.personaldata))

    def test_getFields_baduser(self):
        users = UserInfo(dbconfig.erppeek)
        with self.assertRaises(BadUser) as ctx:
            users.getFields('baduser', ['nif',])
        self.assertEqual(str(ctx.exception),
            "User not found 'baduser'")


    def test_getFields_badfield(self):
        users = UserInfo(dbconfig.erppeek)
        with self.assertRaises(BadField) as ctx:
            users.getFields(self.personaldata.nif, ['badfield',])
        self.assertEqual(str(ctx.exception),
            "Unrecognized user field 'badfield'")

    def test_language(self):
        users = UserInfo(dbconfig.erppeek)
        lang = users.language(self.personaldata.nif)
        self.assertEqual(lang, 'ca')




# vim: et ts=4 sw=4
