# -*- encoding: utf-8 -*-

import unittest
import os
import shutil
from . import portalexample
from . import peerdatastorage
from . import translation
from yamlns import namespace as ns


myuseryaml=u"""\
originpeer: somillusio
nif: 12345678Z
name: Bunny, Bugs
peerroles:
- member
- worker
innerid: 666
address: Golf Club, 5th hole
city: Murcia
state: Murcia
postalcode: '01022'
country: ES
email:
- bugsbunny@loonietoons.com
phone:
- '555121232'
proxynif:
proxyname:
"""

somacmeyaml=u"""\
intercoopVersion: 1.0
peerVersion: 1
peerid: somacme
name: Som Acme, SCCL
url:
  es: http://somacme.coop/es
logo: http://www.linpictures.com/images/indevimgs/acme.jpg
privacyPolicyUrl:
  es: http://www.wallpapersonly.net/wallpapers/thats-all-folks-1680x1050.jpg
description:
  es: >
    La cooperativa para atrapar correcaminos
targetUrl: http://localhost:5001
services:
  explosives:
    name:
      es: Comprar explosivos
    description:
      es: >
        Puedes comprar explosivos éticos de la mejor calidad.
  anvil:
    name:
      es: Comprar yunques
    description:
      es: >
        Yunques garantizados, siempre caen en una cabeza
    fields:
    - originpeer
    - innerid
fields:
- originpeer
- nif
"""

sombogusyaml=u"""\
intercoopVersion: 1.0
peerVersion: 1
peerid: sombogus
name: Som Bogus, SCCL
url:
  es: https://es.sombogus.coop
logo: http://www.linpictures.com/images/indevimgs/acme.jpg
privacyPolicyUrl:
    es: http://www.wallpapersonly.net/wallpapers/thats-all-folks-1680x1050.jpg
description:
    es: >
      Productos inútiles pero muy éticos
targetUrl: http://localhost:5002/intercoop
services:
  contract:
    name:
        es: Contrata
    description:
        es: >
          Productos con marcas tipo Panone, Grifons, Pas Natural, Reacciona...
    fields:
    - originpeer
    - name
"""

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
header= u"""\
<html>
<head>
<meta encoding='utf-8' />
<title>Example Portal</title>
<link rel="stylesheet" type="text/css" href="/intercoop.css">
</head>
<body>
<h1>Intercooperación</h1>
<ul>
"""

footer = u"""\
</ul>
</body>
</html>
"""

acmePeerHeader = """\
<div class='peer'>
<div class='peerlogo'><img src='http://www.linpictures.com/images/indevimgs/acme.jpg' /></div>
<div class='peerheader'><a href='http://somacme.coop/es'>Som Acme, SCCL</a></div>
<div class='peerdescription'>La cooperativa para atrapar correcaminos
</div>
<div class='services'>
"""

acmeService = u"""\
<div class='service'>
<div class='service_header'>Comprar explosivos</div>
<div class='service_description'>Puedes comprar explosivos éticos de la mejor calidad.
</div>
<a class='service_activation_bt' href='activateservice/somacme/explosives'>Activa</a>
</div>
"""

acmeService2 = u"""\
<div class='service'>
<div class='service_header'>Comprar yunques</div>
<div class='service_description'>Yunques garantizados, siempre caen en una cabeza
</div>
<a class='service_activation_bt' href='activateservice/somacme/anvil'>Activa</a>
</div>
"""

bogusPeerHeader = u"""\
<div class='peer'>
<div class='peerlogo'><img src='http://www.linpictures.com/images/indevimgs/acme.jpg' /></div>
<div class='peerheader'><a href='https://es.sombogus.coop'>Som Bogus, SCCL</a></div>
<div class='peerdescription'>Productos inútiles pero muy éticos
</div>
<div class='services'>
"""

bogusService = u"""\
<div class='service'>
<div class='service_header'>Contrata</div>
<div class='service_description'>Productos con marcas tipo Panone, Grifons, Pas Natural, Reacciona...
</div>
<a class='service_activation_bt' href='activateservice/sombogus/contract'>Activa</a>
</div>
"""

peerFooter = u"""\
</div>
</div>
"""

acmeExplosivesHeader = u"""\
<html>
<head>
<meta encoding='utf-8' />
<title>Activación del servicio 'Comprar explosivos' en 'Som Acme, SCCL'</title>
<link rel="stylesheet" type="text/css" href="/intercoop.css">
</head>
<body>
<h1>Autorización de transferencia de datos personales a <em>Som Acme, SCCL</em></h1>
<div class='privacywarning'>
Para activar el servicio <em>Comprar explosivos</em>
en <em>Som Acme, SCCL</em>,
transferiremos a dicha entidad los siguientes datos:
<div class='transferfields'>
"""


acmeExplosivesFooter = u"""\
</div>
Dicha entidad tratar\xe1 dichos datos seg\xfan su propia
<a href='http://www.wallpapersonly.net/wallpapers/thats-all-folks-1680x1050.jpg' target='_blank'>pol\xedtica de privacidad</a>.
</div>
<a class='privacy_accept_bt' href='/confirmactivateservice/somacme/explosives'>
Acepto
</a>
</body>
</html>
"""

nameField = u"""\
<div class='field'>
<div class='fieldheader'>nif:</div>
<div class='fieldvalue'>12345678Z</div>
</div>
"""
originField = u"""\
<div class='field'>
<div class='fieldheader'>originpeer:</div>
<div class='fieldvalue'>somillusio</div>
</div>
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
