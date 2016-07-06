# -*- encoding: utf-8 -*-

from . import userinfo

import unittest
import shutil
import os

from yamlns import namespace as ns

useryaml = """\
name: de los Palotes, Perico
nif: 12345678Z
lang: ca
"""
labelsyaml=u"""\
originpeer:
    es: Entidad de procedencia
    ca: Entitat de provinença
    en: Source entity
lang:
    es: Idioma preferente
    ca: Idioma preferent
    en: Preferred language
nif:
    es: NIF
    ca: NIF
    en: NIF
name:
    es: Nombre
    ca: Nom
    en: Name
peerroles:
    es: Roles
    ca: Rols
    en: Roles
innerid:
    es: Número de socio/a
    ca: Número de soci/a
    en: Member number
address:
    es: Dirección
    ca: Adreça
    en: Address
city:
    es: Municipio
    ca: Municipi
    en: City
state:
    es: Província
    ca: Provincia
    en: State
postalcode:
    es: Código postal
    ca: Codi postal
    en: Postal code
country:
    es: Nacionalidad
    ca: Nacionalitat
    en: Country
email:
    es: Correo electrónico
    ca: Correu electrònic
    en: e-mail
phone:
    es: Teléfono
    ca: Telèfon
    en: Phone
proxynif:
    es: NIF del representante
    ca: NIF del representant
    en: Proxy NIF
proxyname:
    es: Nombre del representante
    ca: Nom del representant
    en: Proxy name
"""


class UserInfo_Test(unittest.TestCase):

    def setUp(self):
        self.datadir = 'userinfotestdir'
        self.cleanUp()
        os.makedirs(self.datadir)
        self.write('myuser.yaml', useryaml)
        self.write('_labels.yaml', labelsyaml)

    def write(self, filename, content):
        filename = os.path.join(self.datadir, filename)
        with open(filename, 'wb') as f:
            f.write(content.encode('utf8'))


    def cleanUp(self):
        try: shutil.rmtree(self.datadir)
        except: pass

    def tearDown(self):
        self.cleanUp()

    def test_getFields_allFields(self):
        storage = userinfo.UserInfo(self.datadir)
        data = storage.getFields('myuser', [
            'name',
            'nif',
            'lang',
            ])

        self.assertEqual(data, ns.loads("""\
            name: de los Palotes, Perico
            nif: 12345678Z
            lang: ca
            """
            ))

    def test_getFields_filtering(self):
        storage = userinfo.UserInfo(self.datadir)
        data = storage.getFields('myuser', [
            'nif',
            ])

        self.assertEqual(data, ns(
            nif = '12345678Z',
            ))

    def test_getFields_baduser(self):
        storage = userinfo.UserInfo(self.datadir)
        with self.assertRaises(userinfo.BadUser) as ctx:
            storage.getFields('baduser', ['nif',])
        self.assertEqual(str(ctx.exception),
            "User not found 'baduser'")


    def test_getFields_badfield(self):
        storage = userinfo.UserInfo(self.datadir)
        with self.assertRaises(userinfo.BadField) as ctx:
            storage.getFields('myuser', ['badfield',])
        self.assertEqual(str(ctx.exception),
            "Unrecognized user field 'badfield'")

    def test_language(self):
        storage = userinfo.UserInfo(self.datadir)
        lang = storage.language('myuser')
        self.assertEqual(lang, 'ca')

    def test_language_ifMissingLangEsDefault(self):
        useryaml = """\
        name: de los Palotes, Perico
        nif: 12345678Z
        """
        self.write('myuser.yaml', useryaml)
        storage = userinfo.UserInfo(self.datadir)
        lang = storage.language('myuser')
        self.assertEqual(lang, 'es')

    def test_fieldLabels(self):
        storage = userinfo.UserInfo(self.datadir)
        data = storage.fieldLabels([
            'proxyname',
            ])

        self.assertEqual(data, ns.loads(u"""\
            proxyname:
                es: Nombre del representante
                ca: Nom del representant
                en: Proxy name
            """
            ))

        


# vim: ts=4 sw=4 et
