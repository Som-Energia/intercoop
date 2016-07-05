# -*- encoding: utf-8 -*-

import unittest
from . import translation
from yamlns import namespace as ns



notranslation=u"""\
description: This is a description
services:
  contract:
    fields:
       name: César
"""

i18n1stlevel=u"""\
description:
  es: La cooperativa para atrapar correcaminos
"""

i18nfallback=u"""\
description:
  en: The cooperative for catching roadrunners
"""

i18nmanylangs=u"""\
description:
  es: La cooperativa para atrapar correcaminos
  en: The cooperative for catching roadrunners
"""

i18nmanylevels=u"""\
services:
  anvil:
    name:
      es: Comprar yunques
    description:
      es: >
        Yunques garantizados, siempre caen en una cabeza
"""

class Portal_Test(unittest.TestCase):

    def setUp(self):
        self.maxDiff=None

    def test_fieldTranslation_existTranslationFirstLevel(self):
        data = ns.loads(i18n1stlevel)
        t = translation.TranslatePeers()
        self.assertEqual(
            "La cooperativa para atrapar correcaminos",
            t.fieldTranslation(data,"description","es"))

    def test_fieldTranslation_fallbackTranslation(self):
        data = ns.loads(i18nfallback)
        t = translation.TranslatePeers()
        self.assertEqual(
            "The cooperative for catching roadrunners",
            t.fieldTranslation(data,"description","es","en"))

    def test_fieldTranslation_doesntExistFallback(self):
        data = ns.loads(i18nfallback)
        t = translation.TranslatePeers()
        with self.assertRaises(Exception) as ctx:
            t.fieldTranslation(data,"description","fr","ca")
        self.assertEqual(str(ctx.exception),
            "None of the 'fr' or 'ca' translations exist for field 'description'")


    def test_fieldTranslation_fallbackLangTranslation(self):
        data = ns.loads(i18nmanylangs)
        t = translation.TranslatePeers()
        self.assertEqual(
            "La cooperativa para atrapar correcaminos",
            t.fieldTranslation(data,"description","es","en"))

    def test_fieldTranslation_doesntExistFieldFirstLevel(self):
        data = ns.loads(i18n1stlevel)
        t = translation.TranslatePeers()
        with self.assertRaises(Exception) as ctx:
            t.fieldTranslation(data,"badfield","es")
        self.assertEqual(str(ctx.exception),
            "Invalid field 'badfield'")

    def test_fieldTranslation_doesntExistTranslationFirstLevel(self):
        data = ns.loads(i18n1stlevel)
        t = translation.TranslatePeers()
        with self.assertRaises(Exception) as ctx:
            t.fieldTranslation(data,"description","fr")
        self.assertEqual(str(ctx.exception),
            "Invalid translation 'fr' for field 'description'")

    def test_fieldTranslation_existTranslationManyLevels(self):
        data = ns.loads(i18nmanylevels)
        t = translation.TranslatePeers()
        self.assertEqual(
            "Yunques garantizados, siempre caen en una cabeza\n",
            t.fieldTranslation(data,"services/anvil/description","es"))

    def test_translateTree_noTranslations(self):
        data = ns.loads(notranslation.encode('utf8'))
        t = translation.TranslatePeers()
        tree = ns(data)
        self.assertEqual(
            tree,
            t.translateTree(data,"es"))

    def test_translateTree_firstLevel(self):
        data = ns.loads(i18n1stlevel)
        t = translation.TranslatePeers()
        tree = ns(data)
        tree.description = tree.description.es
        self.assertEqual(
            tree,
            t.translateTree(data,"es"))

    def test_translateTree_manyLevels(self):
        data = ns.loads(i18nmanylevels)
        t = translation.TranslatePeers()
        tree = ns(data)
        tree.services.anvil.name = tree.services.anvil.name.es
        tree.services.anvil.description = tree.services.anvil.description.es
        self.assertEqual(
            tree,
            t.translateTree(data,"es"))


# vim: ts=4 sw=4 et
