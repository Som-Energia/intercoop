# -*- encoding: utf-8 -*-

import unittest
from . import translation
from yamlns import namespace as ns


class Translator_Test(unittest.TestCase):

    def setUp(self):
        self.maxDiff=None


    def ns(self, content):
        return ns.loads(content)

    def assertTranslateEqual(self, lang, orig, expected):
        t = translation.Translator(lang)
        result = t(self.ns(orig))
        self.assertEqual(result, self.ns(expected))

    def test_plainString(self):
        self.assertTranslateEqual('es',
            "Untranslated string",
            "Untranslated string"
            )
 
    def test_translatedString(self):
        self.assertTranslateEqual('es',
            """\
            en: Translated string
            es: Texto traducido
            """,
            "Texto traducido"
            )

    def test_translatedString_otherLanguage(self):
        self.assertTranslateEqual('en',
            """\
            en: Translated string
            es: Texto traducido
            """,
            "Translated string"
            )
 
    def test_translatedString_missingLanguageTakesFallback(self):
        self.assertTranslateEqual('ca',
            """\
            en: Translated string
            es: Texto traducido
            """,
            "Texto traducido"
            )
 
    def test_translatedString_noFallbackKeyIgnored(self):
        self.assertTranslateEqual('eu',
            """\
            en: Translated string
            ca: Text traduït
            """,
            """\
            en: Translated string
            ca: Text traduït
            """,
            )
 
    def test_translatedString_languagePresent(self):
        self.assertTranslateEqual('ca',
            """\
            en: Translated string
            ca: Text traduït
            """,
            """\
            Text traduït
            """,
            )
 
    def test_insideADict(self):
        self.assertTranslateEqual('ca',
            """\
            key:
                en: Translated string
                ca: Text traduït
            """,
            """\
            key: Text traduït
            """,
            )
 
    def test_translate_multipleKeys(self):
        self.assertTranslateEqual('es',
            """\
            tree1:
                key1:
                    es: Mensaje en español
                    ca: Missatge en català
                key2:
                    es: En Español
                    ca: En Català
            """,
            """\
            tree1:
                key1: Mensaje en español
                key2: En Español
            """
            )

    def test_translate_insideList(self):
        self.assertTranslateEqual('es',
            """\
            listcontainer:
                - key:
                    es: Mensaje en español
                    ca: Missatge en català
            """, """\
            listcontainer:
                - key: Mensaje en español
            """
            )

    def test_languageList_single(self):
        self.assertTranslateEqual(['ca'],
            """\
            en: Translated string
            es: Texto traducido
            ca: Text traduït
            """,
            """\
            Text traduït
            """,
            )
 
    def test_languageList_multiple(self):
        self.assertTranslateEqual(['ca','en'],
            """\
            en: Translated string
            es: Texto traducido
            ca: Text traduït
            """,
            """\
            Text traduït
            """,
            )
 
    def test_languageList_multiple_missingFirst(self):
        self.assertTranslateEqual(['eu','en'],
            """\
            en: Translated string
            es: Texto traducido
            ca: Text traduït
            """,
            """\
            Translated string
            """,
            )

    def test_languageList_multiple_missingAll_takesFallback(self):
        self.assertTranslateEqual(['eu','gl'],
            """\
            en: Translated string
            es: Texto traducido
            ca: Text traduït
            """,
            """\
            Texto traducido
            """,
            )
 

# vim: ts=4 sw=4 et
