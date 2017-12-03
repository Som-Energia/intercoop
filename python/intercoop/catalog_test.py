# -*- encoding: utf-8 -*-

import unittest
import os
import shutil
from . import catalog
from . import userinfo
from . import peerinfo
from yamlns import namespace as ns
import requests_mock

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

    def respondToPost(self, status, text=None):
        text = text or ns(
            continuationUrl = self.continuationUrl
            ).dump()
        m = requests_mock.mock()
        m.post(
            self.apiurl+'/activateService',
            text = text,
            status_code = status,
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

    def test_requiredFields_badPeer(self):
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        with self.assertRaises(Exception) as ctx: # TODO: Maybe custom error
            p.requiredFields("badpeer","explosives")
        self.assertEqual(ctx.exception.message,
            "Not such peer 'badpeer'")

    def test_requiredFields_badService(self):
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        with self.assertRaises(Exception) as ctx: # TODO: Maybe custom error
            p.requiredFields("somacme","badservice")
        self.assertEqual(ctx.exception.message,
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
        bogus = ns.loads(sombogusyaml.encode('utf8'))
        del bogus.services.contract.fields
        self.write("sombogus.yaml",bogus.dump())
        p = self.setupPortal()
        with self.assertRaises(Exception) as ctx:
            p.requiredFields("sombogus","contract")

        self.assertEqual(ctx.exception.message,
            "Peer 'sombogus' does not specify fields for service 'contract'")

    def test_activate_badPeer(self):
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        with self.assertRaises(Exception) as ctx: # TODO: Maybe custom error
            p.activate("badpeer","explosives","myuser")
        self.assertEqual(ctx.exception.message,
            "Not such peer 'badpeer'")

    def test_activate_badService(self):
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        with self.assertRaises(Exception) as ctx: # TODO: Maybe custom error
            p.activate("somacme","badservice","myuser")
        self.assertEqual(ctx.exception.message,
            "Not such service 'badservice' in peer 'somacme'")

    def test_activate_returnsContinuation(self):
        self.write("somacme.yaml",somacmeyaml)
        p = self.setupPortal()
        with self.respondToPost(200) as m:
            url = p.activate("somacme","explosives","myuser")
        self.assertEqual(url,self.continuationUrl)


# vim: ts=4 sw=4 et
