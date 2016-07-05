# -*- encoding: utf-8 -*-

import unittest
from . import translation
from yamlns import namespace as ns



notranslation=ns.loads("""\
description: This is a description
services:
  contract:
    fields:
       name: César
""")

i18n1stlevel=ns.loads("""\
description:
  es: Mensaje en español
""")

i18nfallback=ns.loads("""\
description:
  en: Message in English
""")

i18nmanylangs=ns.loads("""\
description:
  es: Mensaje en español
  en: Message in English
""")

i18nmanylevels=ns.loads("""\
services:
  anvil:
    name:
      es: Comprar yunques
    description:
      es: >
        Yunques garantizados, siempre caen en una cabeza
""")

class Portal_Test(unittest.TestCase):

    def setUp(self):
        self.maxDiff=None

    def test_fieldTranslation_existTranslationFirstLevel(self):
        data = i18n1stlevel
        t = translation.Translator()
        self.assertEqual(
            u"Mensaje en español",
            t.fieldTranslation(data,"description","es"))

    def test_fieldTranslation_fallbackTranslation(self):
        data = i18nfallback
        t = translation.Translator()
        self.assertEqual(
            "Message in English",
            t.fieldTranslation(data,"description","es","en"))

    def test_fieldTranslation_doesntExistFallback(self):
        data = i18nfallback
        t = translation.Translator()
        with self.assertRaises(Exception) as ctx:
            t.fieldTranslation(data,"description","fr","ca")
        self.assertEqual(str(ctx.exception),
            "None of the 'fr' or 'ca' translations exist for field 'description'")


    def test_fieldTranslation_fallbackLangTranslation(self):
        data = i18nmanylangs
        t = translation.Translator()
        self.assertEqual(
            u"Mensaje en español",
            t.fieldTranslation(data,"description","es","en"))

    def test_fieldTranslation_doesntExistFieldFirstLevel(self):
        data = i18n1stlevel
        t = translation.Translator()
        with self.assertRaises(Exception) as ctx:
            t.fieldTranslation(data,"badfield","es")
        self.assertEqual(str(ctx.exception),
            "Invalid field 'badfield'")

    def test_fieldTranslation_doesntExistTranslationFirstLevel(self):
        data = i18n1stlevel
        t = translation.Translator()
        with self.assertRaises(Exception) as ctx:
            t.fieldTranslation(data,"description","fr")
        self.assertEqual(str(ctx.exception),
            "Invalid translation 'fr' for field 'description'")

    def test_fieldTranslation_existTranslationManyLevels(self):
        data = i18nmanylevels
        t = translation.Translator()
        self.assertEqual(
            "Yunques garantizados, siempre caen en una cabeza\n",
            t.fieldTranslation(data,"services/anvil/description","es"))

    def test_translate_noTranslations(self):
        data = notranslation
        t = translation.Translator()
        self.assertEqual(
            data,
            t.translate(notranslation,"es"))

    def test_translate_firstLevel(self):
        data = i18n1stlevel
        t = translation.Translator()
        tree = ns(data)
        tree.description = tree.description.es
        self.assertEqual(
            tree,
            t.translate(data,"es"))

    def test_translate_manyLevels(self):
        data = i18nmanylevels
        t = translation.Translator()
        tree = ns(data)
        tree.services.anvil.name = tree.services.anvil.name.es
        tree.services.anvil.description = tree.services.anvil.description.es
        self.assertEqual(
            tree,
            t.translate(data,"es"))




# vim: ts=4 sw=4 et
