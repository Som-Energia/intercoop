# -*- encoding: utf-8 -*-

import unittest
import os
import shutil
from . import catalog
from . import userinfo
from . import peerinfo
from yamlns import namespace as ns
import requests_mock
from .testutils import assertNsEqual

myuseryaml=u"""\
originpeer: somillusio
lang: es
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
targetUrl: https://api.somacme.coop/intercoop
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

class IntercoopCatalog_Test(unittest.TestCase):

    assertNsEqual = assertNsEqual

    def write(self, filename, content, folder=None):
        fullname = os.path.join(folder or self.peerdatadir,filename)
        with open(fullname, 'wb') as f:
            try:
                f.write(content.encode('utf-8'))
            except UnicodeDecodeError:
                f.write(content)

    def setUp(self):
        self.maxDiff=None
        self.peerid= 'somillusio'
        self.keyfile = 'testkey.pem'
        self.peerdatadir='peerdatadir'
        self.userdatadir='userdatadir'
        self.cleanUp()
        self.peers = peerinfo.PeerInfo(self.peerdatadir)
        self.users = userinfo.UserInfo(self.userdatadir)
        os.system("mkdir -p "+self.peerdatadir)
        os.system("mkdir -p "+self.userdatadir)
        self.write('myuser.yaml', myuseryaml, self.userdatadir)
        self.uuid = '01020304-0506-0708-090a-0b0c0d0e0f10'
        self.apiurl = "https://api.somacme.coop/intercoop"
        self.continuationUrl = 'https://somacme.coop/contract?token={}'.format(
            self.uuid)

    def respondToPost(self, status, text=None, mime='application/yaml'):
        text = text or ns(
            continuationUrl = self.continuationUrl
            ).dump()
        m = requests_mock.mock()
        m.post(
            self.apiurl+'/activateService',
            text = text,
            status_code = status,
            headers = {'content-type': mime},
            )
        return m

    def setupPortal(self):
        return catalog.IntercoopCatalog(
            #peerid = self.peerid,
            keyfile = self.keyfile,
            peers = self.peers,
            users = self.users,
            )

    def tearDown(self):
        self.cleanUp()

    def cleanUp(self):
        try: shutil.rmtree(self.peerdatadir)
        except: pass
        try: shutil.rmtree(self.userdatadir)
        except: pass

    def test_peers(self):
        self.write("sombogus.yaml",sombogusyaml)
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        self.assertNsEqual(ns(data=list(p)),ns(data=[
                ns.loads(somacmeyaml),
                ns.loads(sombogusyaml),
            ]).dump()
        )

    def test_peerInfo(self):
        self.write("sombogus.yaml",sombogusyaml)
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        info = p.peerInfo('somacme')
        self.assertNsEqual(info, somacmeyaml)

    def test_peerInfo_translated(self):
        self.write("sombogus.yaml",sombogusyaml)
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        info = p.peerInfo('sombogus', 'es')
        self.assertEqual(info.description,
            u"Productos inútiles pero muy éticos\n")

    def test_peers(self):
        self.write("sombogus.yaml",sombogusyaml)
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        self.assertMultiLineEqual(ns(data=list(p)).dump(),ns(data=[
                ns.loads(somacmeyaml),
                ns.loads(sombogusyaml),
            ]).dump()
        )

    def test_fieldValues(self):
        self.write("sombogus.yaml",sombogusyaml)
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        values = p.fieldValues('myuser', ['originpeer'])
        self.assertNsEqual(values, """\
            originpeer: somillusio
            """)

    def test_fieldValues_badUser(self): self.skipTest("Not yet implemented")
    def test_fieldValues_badField(self): self.skipTest("Not yet implemented")

    def test_fieldLabels(self):
        self.write("sombogus.yaml",sombogusyaml)
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        labels = p.fieldLabels(['originpeer'], 'ca')
        self.assertNsEqual(labels, """\
            originpeer: Entitat de provinença
            """)

    def test_fieldLabels_langNotFoundTakesEs(self):
        self.write("sombogus.yaml",sombogusyaml)
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        labels = p.fieldLabels(['originpeer'], 'qu')
        self.assertNsEqual(labels, """\
            originpeer: Entidad de procedencia
            """)

    def test_fieldLabels_noLanguage_returnsUntranslated(self):
        self.write("sombogus.yaml",sombogusyaml)
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        labels = p.fieldLabels(['proxyname'])
        self.assertNsEqual(labels, """\
            proxyname:
                es: Nombre del representante
                ca: Nom del representant
                en: Proxy name
            """)

    def test_fieldLabels_badField(self): self.skipTest("Not yet implemented")

    def test_requiredFields_badPeer(self):
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        with self.assertRaises(Exception) as ctx: # TODO: Maybe custom error
            p.requiredFields("badpeer","explosives")
        self.assertEqual(format(ctx.exception),
            "Not such peer 'badpeer'")

    def test_requiredFields_badService(self):
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        with self.assertRaises(Exception) as ctx: # TODO: Maybe custom error
            p.requiredFields("somacme","badservice")
        self.assertEqual(format(ctx.exception),
            "Not such service 'badservice' in peer 'somacme'")

    def test_requiredFields_justInService_useService(self):
        self.write("sombogus.yaml",sombogusyaml)
        p = self.setupPortal()
        self.assertEqual(
            ['originpeer','name'],
            p.requiredFields("sombogus","contract")
        )

    def test_requiredFields_justInPeer_usePeer(self):
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        self.assertEqual(
            ['originpeer','nif'],
            p.requiredFields("somacme","explosives")
        )

    def test_requiredFields_inServiceAndPeer_useService(self):
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        self.assertEqual(
            ['originpeer', 'innerid'],
            p.requiredFields("somacme","anvil")
        )

    def test_requiredFields_noFields(self):
        bogus = ns.loads(sombogusyaml)
        del bogus.services.contract.fields
        self.write("sombogus.yaml",bogus.dump())
        p = self.setupPortal()
        with self.assertRaises(Exception) as ctx:
            p.requiredFields("sombogus","contract")

        self.assertEqual(format(ctx.exception),
            "Peer 'sombogus' does not specify fields for service 'contract'")

    def test_activate_badPeer(self):
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        with self.assertRaises(Exception) as ctx: # TODO: Maybe custom error
            p.activate("badpeer","explosives","myuser")
        self.assertEqual(format(ctx.exception),
            "Not such peer 'badpeer'")

    def test_activate_badService(self):
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        with self.assertRaises(Exception) as ctx: # TODO: Maybe custom error
            p.activate("somacme","badservice","myuser")
        self.assertEqual(format(ctx.exception),
            "Not such service 'badservice' in peer 'somacme'")

    def test_activate_returnsContinuation(self):
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        with self.respondToPost(200) as m:
            url = p.activate("somacme","explosives","myuser")
        self.assertEqual(url,self.continuationUrl)

    def test_activate_doesPost(self):
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        with self.respondToPost(200) as m:
            url = p.activate("somacme","explosives","myuser")
        self.assertEqual([
            (h.method, h.url, h.text)
            for h in m.request_history], [
            ('POST', 'https://api.somacme.coop/intercoop/activateService',

                u"intercoopVersion: '1.0'\n"
                u"payload: b3JpZ2lucGVlcjogc29taWxsdXNpbwpuaWY6IDEyMzQ1Njc4Wgo=\n"
                u"signature: qlWZI8UbTaqzPwXsssPiVoaVTirrwuruFM3JjKiYofHSeZhn0B2vtIgXGBMUt15VzEH0__22QI9aeeSQF4AIHB_35QCq3bB85UMr8KS03BGbRXr36jVKYZ0M-csILl_uh9hGzCxFxlI5wzaOI82eYsYiu90MNOTdORyEKbqqt5meuMLcVKAemS_qfed85vUQAcX2_hf_CRZJo3QBRwjHOqUEZwzDoUd-EDFdHAm-ZbvukrKFPnnwGE0JldM30QNs1F0X-0iq-QwgV3fGlflAzTXIrLwkRPsM0RbMNEPWSmSrm_UjUtdPoYxd7HH7Qx1UhAHxU8_yXs5JIvD-63EN1A==\n"
                )
            ])

    def test_activate_badUser(self):
        self.skipTest("TODO: Not yet implemented")

    def test_activate_remoteFailure(self):
        self.skipTest("TODO: Not yet implemented")
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        response = 'caca'
        with self.respondToPost(200, response) as m:
            with self.assertRaises(Exception) as ctx: # TODO: Maybe custom error
                p.activate("somacme","explosives","myuser")
        self.assertEqual(format(ctx.exception),
            "CACa")


# vim: ts=4 sw=4 et
