# -*- encoding: utf-8 -*-

from intercoop.catalog import labelsyaml, BadField, BadUser
from erppeek import Client
from yamlns import namespace as ns

class UserInfo(object):

    def __init__(self, config):
        self.config = config
        self.supportedFields = ns.loads(labelsyaml).keys()

    def language(self, user):
        return self.getFields(user, ['lang']).lang

    def getFields(self, user, fields=None):
        if fields is not None:
            for field in fields:
                if field not in self.supportedFields:
                    raise BadField(field)
            return ns((
                (key, value)
                for key, value in self.getFields(user).items()
                if key in fields
            ))

        O = Client(**self.config)
        ids = O.ResPartner.search([
			('vat', '=', 'ES' + user),
		])
        if not ids:
            raise BadUser(user)
        partner_id = ids[0]
        partner = O.ResPartner.browse(partner_id)
        address_id = O.ResPartnerAddress.search([
            ('partner_id','=',partner_id),
        ])
        return ns(
            originpeer='somenergia',
            nif=user,
            lang=partner.lang[:2],
            name=partner.name,
            innerid=partner.www_soci,
            peerroles=['member'] if partner.www_soci != '---------' else [],
            address=partner.www_street,
            city=partner.www_municipi.ine,
            state=partner.www_provincia.code,
            postalcode=partner.www_zip,
            country='ES', # TODO: Take it from the ERP
            email=partner.www_email,
            phone=partner.www_phone or partner.www_mobile,
            proxynif='TODO',
            proxyname='TODO',
        )

# vim: et ts=4 sw=4
